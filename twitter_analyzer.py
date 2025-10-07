#!/usr/bin/env python3
"""
Twitter/X Profile Analyzer
==========================

Twitter/X profile analysis tool that works with publicly available information.
Note: Twitter's API requires authentication for most operations.
"""

import requests
import json
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import quote
import logging
from bs4 import BeautifulSoup
import cloudscraper

logger = logging.getLogger(__name__)

class TwitterAnalyzer:
    """Twitter/X profile analyzer"""
    
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.base_url = "https://twitter.com"
        self.rate_limit = 3
        
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Make a request with proper headers"""
        try:
            time.sleep(self.rate_limit)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
            }
            
            response = self.scraper.get(url, headers=headers, timeout=15)
            logger.info(f"Twitter request to {url} - Status: {response.status_code}")
            return response
            
        except Exception as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
    
    def extract_profile_data(self, username: str) -> Dict[str, Any]:
        """Extract profile data from Twitter profile page"""
        username = username.replace('@', '').strip()
        url = f"{self.base_url}/{username}"
        
        logger.info(f"Analyzing Twitter profile: @{username}")
        
        response = self._make_request(url)
        if not response or response.status_code != 200:
            logger.warning(f"Could not access Twitter profile: @{username}")
            return {}
        
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            profile_data = {
                'username': username,
                'profile_url': url,
                'extracted_at': datetime.now().isoformat()
            }
            
            # Extract from meta tags
            self._extract_meta_data(soup, profile_data)
            
            # Extract from JSON data in scripts
            self._extract_script_data(soup, profile_data)
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error extracting Twitter profile data for @{username}: {e}")
            return {}
    
    def _extract_meta_data(self, soup: BeautifulSoup, profile_data: Dict[str, Any]):
        """Extract data from meta tags"""
        try:
            # Title
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text()
                profile_data['page_title'] = title
                
                # Extract display name from title
                if '(@' in title:
                    display_name = title.split('(@')[0].strip()
                    profile_data['display_name'] = display_name
            
            # Description
            desc_tag = soup.find('meta', {'name': 'description'})
            if desc_tag:
                description = desc_tag.get('content', '')
                profile_data['meta_description'] = description
            
            # Open Graph data
            og_tags = {
                'og:title': 'og_title',
                'og:description': 'og_description',
                'og:image': 'profile_image_url',
                'og:url': 'canonical_url'
            }
            
            for og_property, data_key in og_tags.items():
                og_tag = soup.find('meta', {'property': og_property})
                if og_tag:
                    profile_data[data_key] = og_tag.get('content', '')
            
            # Twitter Card data
            twitter_tags = {
                'twitter:title': 'twitter_title',
                'twitter:description': 'twitter_description',
                'twitter:image': 'twitter_image'
            }
            
            for twitter_name, data_key in twitter_tags.items():
                twitter_tag = soup.find('meta', {'name': twitter_name})
                if twitter_tag:
                    profile_data[data_key] = twitter_tag.get('content', '')
                    
        except Exception as e:
            logger.debug(f"Error extracting Twitter meta data: {e}")
    
    def _extract_script_data(self, soup: BeautifulSoup, profile_data: Dict[str, Any]):
        """Extract data from script tags"""
        try:
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and ('window.__INITIAL_STATE__' in script.string or 
                                    'window.__data' in script.string):
                    try:
                        script_content = script.string
                        
                        # Try to extract JSON data
                        json_match = re.search(r'({.*})', script_content)
                        if json_match:
                            json_str = json_match.group(1)
                            data = json.loads(json_str)
                            
                            # Navigate through Twitter's data structure
                            if isinstance(data, dict):
                                self._parse_twitter_data(data, profile_data)
                        
                    except (json.JSONDecodeError, AttributeError) as e:
                        logger.debug(f"Could not parse Twitter script data: {e}")
                        continue
                        
        except Exception as e:
            logger.debug(f"Error extracting Twitter script data: {e}")
    
    def _parse_twitter_data(self, data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Parse Twitter's internal data structure"""
        try:
            # Twitter's data structure can vary, so we'll look for common patterns
            
            # Look for user data in various possible locations
            user_data = None
            
            # Common paths where user data might be found
            possible_paths = [
                ['users', 'entities'],
                ['entities', 'users'],
                ['globalObjects', 'users'],
                ['user']
            ]
            
            for path in possible_paths:
                current = data
                for key in path:
                    if isinstance(current, dict) and key in current:
                        current = current[key]
                    else:
                        break
                else:
                    # If we made it through the whole path
                    if isinstance(current, dict):
                        # Find the user data (usually keyed by user ID)
                        for user_id, user_info in current.items():
                            if isinstance(user_info, dict) and user_info.get('screen_name'):
                                if user_info['screen_name'].lower() == profile_data['username'].lower():
                                    user_data = user_info
                                    break
                    break
            
            # If we found user data, extract relevant information
            if user_data:
                profile_data.update({
                    'display_name': user_data.get('name', ''),
                    'bio': user_data.get('description', ''),
                    'follower_count': user_data.get('followers_count', 0),
                    'following_count': user_data.get('friends_count', 0),
                    'tweets_count': user_data.get('statuses_count', 0),
                    'verified': user_data.get('verified', False),
                    'protected': user_data.get('protected', False),
                    'created_at': user_data.get('created_at', ''),
                    'location': user_data.get('location', ''),
                    'website': user_data.get('url', ''),
                    'profile_banner_url': user_data.get('profile_banner_url', ''),
                    'profile_image_url_https': user_data.get('profile_image_url_https', '')
                })
                
        except Exception as e:
            logger.debug(f"Error parsing Twitter user data: {e}")
    
    def search_username_variations(self, base_username: str) -> List[Dict[str, Any]]:
        """Search for variations of a username on Twitter"""
        variations = [
            base_username,
            base_username.lower(),
            base_username.upper(),
            f"{base_username}_",
            f"_{base_username}",
            f"{base_username}1",
            f"{base_username}2",
            f"{base_username}3",
            f"real{base_username}",
            f"{base_username}real",
            f"official{base_username}",
            f"{base_username}official",
            f"the{base_username}",
            f"{base_username}x"
        ]
        
        results = []
        
        for variation in variations:
            logger.info(f"Checking Twitter variation: @{variation}")
            profile_data = self.extract_profile_data(variation)
            
            if profile_data and profile_data.get('username'):
                results.append(profile_data)
                logger.info(f"Found Twitter profile: @{variation}")
            
            time.sleep(2)  # Respect rate limits
        
        return results
    
    def analyze_account_patterns(self, username: str) -> Dict[str, Any]:
        """Analyze Twitter account patterns"""
        profile_data = self.extract_profile_data(username)
        
        if not profile_data:
            return {'error': 'Profile not found or inaccessible'}
        
        analysis = {
            'username': username,
            'account_type': self._determine_account_type(profile_data),
            'activity_analysis': self._analyze_activity(profile_data),
            'influence_metrics': self._calculate_influence_metrics(profile_data),
            'authenticity_score': self._calculate_authenticity_score(profile_data),
            'extracted_at': datetime.now().isoformat()
        }
        
        return analysis
    
    def _determine_account_type(self, profile_data: Dict[str, Any]) -> str:
        """Determine Twitter account type"""
        if profile_data.get('verified'):
            return 'verified'
        elif profile_data.get('protected'):
            return 'protected'
        else:
            return 'public'
    
    def _analyze_activity(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze account activity patterns"""
        tweets = profile_data.get('tweets_count', 0)
        followers = profile_data.get('follower_count', 0)
        following = profile_data.get('following_count', 0)
        
        # Calculate activity metrics
        tweets_per_follower = tweets / max(followers, 1) * 1000
        follow_ratio = followers / max(following, 1)
        
        return {
            'tweets_count': tweets,
            'tweets_per_1k_followers': round(tweets_per_follower, 2),
            'follower_following_ratio': round(follow_ratio, 2),
            'activity_level': self._categorize_activity_level(tweets),
            'engagement_type': self._categorize_engagement_type(follow_ratio)
        }
    
    def _categorize_activity_level(self, tweets: int) -> str:
        """Categorize activity level based on tweet count"""
        if tweets == 0:
            return 'inactive'
        elif tweets < 100:
            return 'low'
        elif tweets < 1000:
            return 'moderate'
        elif tweets < 10000:
            return 'high'
        else:
            return 'very_high'
    
    def _categorize_engagement_type(self, follow_ratio: float) -> str:
        """Categorize engagement type based on follow ratio"""
        if follow_ratio > 10:
            return 'influencer'
        elif follow_ratio > 1:
            return 'content_creator'
        elif follow_ratio > 0.1:
            return 'balanced'
        else:
            return 'follower_focused'
    
    def _calculate_influence_metrics(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate influence metrics"""
        followers = profile_data.get('follower_count', 0)
        following = profile_data.get('following_count', 0)
        tweets = profile_data.get('tweets_count', 0)
        
        # Simple influence score calculation
        if followers == 0:
            influence_score = 0
        else:
            # Weighted score based on followers, engagement ratio, and content
            follower_score = min(followers / 1000, 100)  # Cap at 100
            ratio_score = min(followers / max(following, 1), 10)  # Cap at 10
            content_score = min(tweets / 100, 10)  # Cap at 10
            
            influence_score = (follower_score * 0.5 + ratio_score * 0.3 + content_score * 0.2)
        
        return {
            'influence_score': round(influence_score, 2),
            'follower_tier': self._get_follower_tier(followers),
            'engagement_potential': self._assess_engagement_potential(followers, following, tweets)
        }
    
    def _get_follower_tier(self, followers: int) -> str:
        """Get follower tier classification"""
        if followers < 100:
            return 'nano'
        elif followers < 1000:
            return 'micro'
        elif followers < 10000:
            return 'mid_tier'
        elif followers < 100000:
            return 'macro'
        else:
            return 'mega'
    
    def _assess_engagement_potential(self, followers: int, following: int, tweets: int) -> str:
        """Assess engagement potential"""
        if followers > 10000 and tweets > 1000:
            return 'high'
        elif followers > 1000 and tweets > 100:
            return 'moderate'
        elif followers > 100 or tweets > 10:
            return 'low'
        else:
            return 'minimal'
    
    def _calculate_authenticity_score(self, profile_data: Dict[str, Any]) -> float:
        """Calculate authenticity score"""
        score = 0.0
        
        # Check for profile completeness
        if profile_data.get('display_name', '').strip():
            score += 0.2
        if profile_data.get('bio', '').strip():
            score += 0.3
        if profile_data.get('profile_image_url_https'):
            score += 0.2
        if profile_data.get('location', '').strip():
            score += 0.1
        if profile_data.get('website', '').strip():
            score += 0.1
        if profile_data.get('verified'):
            score += 0.1
        
        return round(score, 2)

def main():
    """Main function for Twitter analysis"""
    print("🐦 Twitter/X Profile Analyzer")
    print("=" * 30)
    print()
    
    username = input("Enter Twitter username (without @): ").strip()
    
    if not username:
        print("❌ Please enter a valid username")
        return
    
    analyzer = TwitterAnalyzer()
    
    print(f"\n🔍 Analyzing @{username}...")
    
    # Basic profile analysis
    profile_data = analyzer.extract_profile_data(username)
    
    if profile_data and profile_data.get('username'):
        print(f"\n✅ Profile found: @{username}")
        print(f"Display Name: {profile_data.get('display_name', 'N/A')}")
        print(f"Bio: {profile_data.get('bio', 'N/A')[:100]}{'...' if len(profile_data.get('bio', '')) > 100 else ''}")
        print(f"Followers: {profile_data.get('follower_count', 0):,}")
        print(f"Following: {profile_data.get('following_count', 0):,}")
        print(f"Tweets: {profile_data.get('tweets_count', 0):,}")
        print(f"Verified: {'✅' if profile_data.get('verified') else '❌'}")
        print(f"Protected: {'🔒' if profile_data.get('protected') else '🔓'}")
        
        if profile_data.get('location'):
            print(f"Location: {profile_data.get('location')}")
        if profile_data.get('website'):
            print(f"Website: {profile_data.get('website')}")
    else:
        print(f"❌ Profile not found or inaccessible: @{username}")
    
    print("\n✅ Analysis completed!")

if __name__ == "__main__":
    main()