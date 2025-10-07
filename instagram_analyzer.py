#!/usr/bin/env python3
"""
Instagram Profile Analyzer
==========================

Instagram profile analysis tool that works with publicly available information
and respects Instagram's terms of service.

Note: Instagram has strict anti-scraping measures. This tool focuses on
legitimate methods and publicly accessible data only.
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

class InstagramAnalyzer:
    """Instagram profile analyzer using legitimate methods"""
    
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.base_url = "https://www.instagram.com"
        self.rate_limit = 5  # Instagram is more strict
        
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Make a request with proper headers and rate limiting"""
        try:
            time.sleep(self.rate_limit)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = self.scraper.get(url, headers=headers, timeout=15)
            logger.info(f"Instagram request to {url} - Status: {response.status_code}")
            return response
            
        except Exception as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
    
    def extract_profile_data(self, username: str) -> Dict[str, Any]:
        """
        Extract basic profile data from Instagram profile page
        """
        username = username.replace('@', '').strip()
        url = f"{self.base_url}/{username}/"
        
        logger.info(f"Analyzing Instagram profile: @{username}")
        
        response = self._make_request(url)
        if not response or response.status_code != 200:
            logger.warning(f"Could not access Instagram profile: @{username}")
            return {}
        
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            profile_data = {
                'username': username,
                'profile_url': url,
                'extracted_at': datetime.now().isoformat()
            }
            
            # Extract data from meta tags
            self._extract_meta_data(soup, profile_data)
            
            # Extract data from JSON-LD
            self._extract_json_ld_data(soup, profile_data)
            
            # Extract from page content
            self._extract_page_content(soup, profile_data)
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error extracting Instagram profile data for @{username}: {e}")
            return {}
    
    def _extract_meta_data(self, soup: BeautifulSoup, profile_data: Dict[str, Any]):
        """Extract data from meta tags"""
        try:
            # Title tag
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text()
                if '(@' in title:
                    display_name = title.split('(@')[0].strip()
                    profile_data['display_name'] = display_name
            
            # Description meta tag
            desc_tag = soup.find('meta', {'name': 'description'})
            if desc_tag:
                description = desc_tag.get('content', '')
                profile_data['meta_description'] = description
                
                # Extract follower count from description
                follower_match = re.search(r'(\d+(?:,\d+)*)\s*Followers', description)
                if follower_match:
                    followers_str = follower_match.group(1).replace(',', '')
                    profile_data['follower_count'] = int(followers_str)
                
                # Extract following count
                following_match = re.search(r'(\d+(?:,\d+)*)\s*Following', description)
                if following_match:
                    following_str = following_match.group(1).replace(',', '')
                    profile_data['following_count'] = int(following_str)
                
                # Extract posts count
                posts_match = re.search(r'(\d+(?:,\d+)*)\s*Posts', description)
                if posts_match:
                    posts_str = posts_match.group(1).replace(',', '')
                    profile_data['posts_count'] = int(posts_str)
            
            # Open Graph tags
            og_title = soup.find('meta', {'property': 'og:title'})
            if og_title:
                profile_data['og_title'] = og_title.get('content', '')
            
            og_description = soup.find('meta', {'property': 'og:description'})
            if og_description:
                profile_data['og_description'] = og_description.get('content', '')
            
            og_image = soup.find('meta', {'property': 'og:image'})
            if og_image:
                profile_data['profile_image_url'] = og_image.get('content', '')
                
        except Exception as e:
            logger.debug(f"Error extracting meta data: {e}")
    
    def _extract_json_ld_data(self, soup: BeautifulSoup, profile_data: Dict[str, Any]):
        """Extract structured data from JSON-LD"""
        try:
            json_scripts = soup.find_all('script', {'type': 'application/ld+json'})
            
            for script in json_scripts:
                if script.string:
                    try:
                        data = json.loads(script.string)
                        
                        if isinstance(data, dict):
                            # Extract person/profile data
                            if data.get('@type') == 'Person':
                                profile_data['display_name'] = data.get('name', profile_data.get('display_name', ''))
                                profile_data['bio'] = data.get('description', '')
                                profile_data['website'] = data.get('url', '')
                            
                            # Extract additional metadata
                            if 'mainEntity' in data:
                                entity = data['mainEntity']
                                if isinstance(entity, dict):
                                    profile_data['display_name'] = entity.get('name', profile_data.get('display_name', ''))
                                    
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            logger.debug(f"Error extracting JSON-LD data: {e}")
    
    def _extract_page_content(self, soup: BeautifulSoup, profile_data: Dict[str, Any]):
        """Extract data from page content"""
        try:
            # Look for shared data in script tags
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and 'window._sharedData' in script.string:
                    try:
                        # Extract shared data
                        script_content = script.string
                        
                        # Find the JSON data
                        start = script_content.find('{')
                        end = script_content.rfind('}') + 1
                        
                        if start != -1 and end != -1:
                            json_str = script_content[start:end]
                            shared_data = json.loads(json_str)
                            
                            # Navigate through the data structure
                            entry_data = shared_data.get('entry_data', {})
                            profile_page = entry_data.get('ProfilePage', [])
                            
                            if profile_page and len(profile_page) > 0:
                                user_data = profile_page[0].get('graphql', {}).get('user', {})
                                
                                if user_data:
                                    profile_data.update({
                                        'display_name': user_data.get('full_name', ''),
                                        'bio': user_data.get('biography', ''),
                                        'follower_count': user_data.get('edge_followed_by', {}).get('count', 0),
                                        'following_count': user_data.get('edge_follow', {}).get('count', 0),
                                        'posts_count': user_data.get('edge_owner_to_timeline_media', {}).get('count', 0),
                                        'verified': user_data.get('is_verified', False),
                                        'private': user_data.get('is_private', False),
                                        'business_account': user_data.get('is_business_account', False),
                                        'external_url': user_data.get('external_url', ''),
                                        'profile_pic_url': user_data.get('profile_pic_url', '')
                                    })
                        
                        break  # Found shared data, no need to continue
                        
                    except (json.JSONDecodeError, KeyError, IndexError) as e:
                        logger.debug(f"Could not parse shared data: {e}")
                        continue
                        
        except Exception as e:
            logger.debug(f"Error extracting page content: {e}")
    
    def search_username_variations(self, base_username: str) -> List[Dict[str, Any]]:
        """Search for variations of a username on Instagram"""
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
            f"{base_username}.official",
            f"the{base_username}",
            f"{base_username}gram"
        ]
        
        results = []
        
        for variation in variations:
            logger.info(f"Checking Instagram variation: @{variation}")
            profile_data = self.extract_profile_data(variation)
            
            if profile_data and profile_data.get('username'):
                results.append(profile_data)
                logger.info(f"Found Instagram profile: @{variation}")
            
            # Respect Instagram's stricter rate limits
            time.sleep(3)
        
        return results
    
    def analyze_profile_patterns(self, username: str) -> Dict[str, Any]:
        """Analyze profile patterns and characteristics"""
        profile_data = self.extract_profile_data(username)
        
        if not profile_data:
            return {'error': 'Profile not found or inaccessible'}
        
        analysis = {
            'username': username,
            'profile_exists': True,
            'account_type': self._determine_account_type(profile_data),
            'engagement_potential': self._estimate_engagement_potential(profile_data),
            'authenticity_indicators': self._analyze_authenticity(profile_data),
            'content_strategy': self._analyze_content_strategy(profile_data),
            'extracted_at': datetime.now().isoformat()
        }
        
        return analysis
    
    def _determine_account_type(self, profile_data: Dict[str, Any]) -> str:
        """Determine the type of Instagram account"""
        if profile_data.get('business_account'):
            return 'business'
        elif profile_data.get('verified'):
            return 'verified_personal'
        elif profile_data.get('private'):
            return 'private_personal'
        else:
            return 'public_personal'
    
    def _estimate_engagement_potential(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate engagement potential based on metrics"""
        followers = profile_data.get('follower_count', 0)
        following = profile_data.get('following_count', 0)
        posts = profile_data.get('posts_count', 0)
        
        # Calculate ratios
        follower_following_ratio = followers / max(following, 1)
        posts_per_follower = posts / max(followers, 1) * 1000  # posts per 1k followers
        
        return {
            'follower_following_ratio': round(follower_following_ratio, 2),
            'posts_per_1k_followers': round(posts_per_follower, 2),
            'engagement_category': self._categorize_engagement(follower_following_ratio, posts),
            'activity_level': self._assess_activity_level(posts, followers)
        }
    
    def _categorize_engagement(self, ff_ratio: float, posts: int) -> str:
        """Categorize engagement level"""
        if ff_ratio > 10 and posts > 50:
            return 'high_influence'
        elif ff_ratio > 1 and posts > 10:
            return 'moderate_influence'
        elif ff_ratio < 0.1:
            return 'follower_focused'
        else:
            return 'balanced'
    
    def _assess_activity_level(self, posts: int, followers: int) -> str:
        """Assess account activity level"""
        if posts == 0:
            return 'inactive'
        elif posts < 10:
            return 'low_activity'
        elif posts < 100:
            return 'moderate_activity'
        else:
            return 'high_activity'
    
    def _analyze_authenticity(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze authenticity indicators"""
        indicators = {
            'has_profile_picture': bool(profile_data.get('profile_pic_url')),
            'has_bio': bool(profile_data.get('bio', '').strip()),
            'has_display_name': bool(profile_data.get('display_name', '').strip()),
            'has_external_link': bool(profile_data.get('external_url', '').strip()),
            'is_verified': profile_data.get('verified', False),
            'is_business': profile_data.get('business_account', False)
        }
        
        # Calculate authenticity score
        score = sum([
            indicators['has_profile_picture'] * 0.2,
            indicators['has_bio'] * 0.3,
            indicators['has_display_name'] * 0.2,
            indicators['has_external_link'] * 0.1,
            indicators['is_verified'] * 0.2
        ])
        
        indicators['authenticity_score'] = round(score, 2)
        
        return indicators
    
    def _analyze_content_strategy(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content strategy indicators"""
        bio = profile_data.get('bio', '')
        
        return {
            'bio_length': len(bio),
            'has_hashtags_in_bio': '#' in bio,
            'has_mentions_in_bio': '@' in bio,
            'has_emoji_in_bio': any(ord(char) > 127 for char in bio),
            'external_link_present': bool(profile_data.get('external_url')),
            'business_indicators': self._detect_business_indicators(bio)
        }
    
    def _detect_business_indicators(self, bio: str) -> List[str]:
        """Detect business-related indicators in bio"""
        indicators = []
        bio_lower = bio.lower()
        
        business_keywords = [
            'dm for', 'contact', 'email', 'business', 'shop', 'store',
            'brand', 'agency', 'service', 'booking', 'collaboration',
            'partnership', 'sponsor', 'ambassador'
        ]
        
        for keyword in business_keywords:
            if keyword in bio_lower:
                indicators.append(keyword)
        
        return indicators

def main():
    """Main function for Instagram analysis"""
    print("📸 Instagram Profile Analyzer")
    print("=" * 32)
    print()
    
    username = input("Enter Instagram username (without @): ").strip()
    
    if not username:
        print("❌ Please enter a valid username")
        return
    
    analyzer = InstagramAnalyzer()
    
    print(f"\n🔍 Analyzing @{username}...")
    print("Note: Instagram has strict anti-scraping measures.")
    print("This analysis uses only publicly available information.")
    
    # Basic profile analysis
    profile_data = analyzer.extract_profile_data(username)
    
    if profile_data and profile_data.get('username'):
        print(f"\n✅ Profile found: @{username}")
        print(f"Display Name: {profile_data.get('display_name', 'N/A')}")
        print(f"Bio: {profile_data.get('bio', 'N/A')[:100]}{'...' if len(profile_data.get('bio', '')) > 100 else ''}")
        print(f"Followers: {profile_data.get('follower_count', 0):,}")
        print(f"Following: {profile_data.get('following_count', 0):,}")
        print(f"Posts: {profile_data.get('posts_count', 0):,}")
        print(f"Verified: {'✅' if profile_data.get('verified') else '❌'}")
        print(f"Private: {'🔒' if profile_data.get('private') else '🔓'}")
        print(f"Business: {'💼' if profile_data.get('business_account') else '👤'}")
        
        if profile_data.get('external_url'):
            print(f"Website: {profile_data.get('external_url')}")
    else:
        print(f"❌ Profile not found or inaccessible: @{username}")
    
    # Advanced analysis
    if profile_data and profile_data.get('username'):
        do_analysis = input("\nPerform detailed analysis? (y/n): ").lower().strip()
        if do_analysis == 'y':
            print("\n📊 Performing detailed analysis...")
            analysis = analyzer.analyze_profile_patterns(username)
            
            if 'error' not in analysis:
                print(f"\nAccount Type: {analysis.get('account_type', 'unknown')}")
                
                engagement = analysis.get('engagement_potential', {})
                print(f"Engagement Category: {engagement.get('engagement_category', 'unknown')}")
                print(f"Activity Level: {engagement.get('activity_level', 'unknown')}")
                
                authenticity = analysis.get('authenticity_indicators', {})
                print(f"Authenticity Score: {authenticity.get('authenticity_score', 0)}/1.0")
    
    print("\n✅ Analysis completed!")

if __name__ == "__main__":
    main()