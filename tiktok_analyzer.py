#!/usr/bin/env python3
"""
TikTok Profile Analyzer
======================

Enhanced TikTok profile analysis tool that respects platform guidelines
and focuses on publicly available information.

IMPORTANT: This tool uses legitimate methods and respects TikTok's terms of service.
"""

import requests
import json
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import quote, urljoin
import logging
from bs4 import BeautifulSoup
import cloudscraper

logger = logging.getLogger(__name__)

class TikTokAnalyzer:
    """Enhanced TikTok profile analyzer"""
    
    def __init__(self):
        # Use cloudscraper to handle basic anti-bot measures
        self.scraper = cloudscraper.create_scraper()
        self.base_url = "https://www.tiktok.com"
        self.rate_limit = 3  # seconds between requests
        
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
            logger.info(f"TikTok request to {url} - Status: {response.status_code}")
            return response
            
        except Exception as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
    
    def extract_profile_data(self, username: str) -> Dict[str, Any]:
        """
        Extract profile data from TikTok profile page
        """
        username = username.replace('@', '').strip()
        url = f"{self.base_url}/@{username}"
        
        logger.info(f"Analyzing TikTok profile: @{username}")
        
        response = self._make_request(url)
        if not response or response.status_code != 200:
            logger.warning(f"Could not access TikTok profile: @{username}")
            return {}
        
        try:
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract JSON data from script tags
            profile_data = {}
            
            # Look for SIGI_STATE or __DEFAULT_SCOPE__ data
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and ('window["SIGI_STATE"]' in script.string or '__DEFAULT_SCOPE__' in script.string):
                    try:
                        # Extract JSON data
                        script_content = script.string
                        
                        # Try to find user data
                        if 'userDetail' in script_content:
                            # Extract user detail information
                            user_match = re.search(r'"userDetail":\s*({[^}]+})', script_content)
                            if user_match:
                                user_data = json.loads(user_match.group(1))
                                profile_data.update(user_data)
                        
                        # Try to find stats data
                        if 'stats' in script_content:
                            stats_match = re.search(r'"stats":\s*({[^}]+})', script_content)
                            if stats_match:
                                stats_data = json.loads(stats_match.group(1))
                                profile_data['stats'] = stats_data
                                
                    except (json.JSONDecodeError, AttributeError) as e:
                        logger.debug(f"Could not parse script data: {e}")
                        continue
            
            # Fallback: Extract data from meta tags and visible elements
            if not profile_data:
                profile_data = self._extract_fallback_data(soup, username)
            
            # Add timestamp
            profile_data['extracted_at'] = datetime.now().isoformat()
            profile_data['profile_url'] = url
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error extracting profile data for @{username}: {e}")
            return {}
    
    def _extract_fallback_data(self, soup: BeautifulSoup, username: str) -> Dict[str, Any]:
        """Extract basic profile data using fallback methods"""
        data = {
            'username': username,
            'display_name': '',
            'bio': '',
            'follower_count': 0,
            'following_count': 0,
            'video_count': 0,
            'verified': False,
            'private': False
        }
        
        try:
            # Extract from meta tags
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text()
                # Extract display name from title
                if '(@' in title:
                    display_name = title.split('(@')[0].strip()
                    data['display_name'] = display_name
            
            # Look for description meta tag
            desc_tag = soup.find('meta', {'name': 'description'})
            if desc_tag:
                description = desc_tag.get('content', '')
                # Extract follower info from description
                follower_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s*Followers', description, re.IGNORECASE)
                if follower_match:
                    data['follower_count'] = self._parse_count(follower_match.group(1))
                
                following_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s*Following', description, re.IGNORECASE)
                if following_match:
                    data['following_count'] = self._parse_count(following_match.group(1))
            
            # Look for structured data
            json_ld = soup.find('script', {'type': 'application/ld+json'})
            if json_ld:
                try:
                    ld_data = json.loads(json_ld.string)
                    if isinstance(ld_data, dict):
                        data['display_name'] = ld_data.get('name', data['display_name'])
                        data['bio'] = ld_data.get('description', data['bio'])
                except json.JSONDecodeError:
                    pass
            
        except Exception as e:
            logger.debug(f"Error in fallback extraction: {e}")
        
        return data
    
    def _parse_count(self, count_str: str) -> int:
        """Parse count strings like '1.2M', '500K', etc."""
        try:
            count_str = count_str.upper().replace(',', '')
            
            if 'K' in count_str:
                return int(float(count_str.replace('K', '')) * 1000)
            elif 'M' in count_str:
                return int(float(count_str.replace('M', '')) * 1000000)
            elif 'B' in count_str:
                return int(float(count_str.replace('B', '')) * 1000000000)
            else:
                return int(count_str)
        except (ValueError, TypeError):
            return 0
    
    def search_username_variations(self, base_username: str) -> List[Dict[str, Any]]:
        """
        Search for variations of a username on TikTok
        """
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
            f"{base_username}official"
        ]
        
        results = []
        
        for variation in variations:
            logger.info(f"Checking variation: @{variation}")
            profile_data = self.extract_profile_data(variation)
            
            if profile_data and profile_data.get('username'):
                results.append(profile_data)
                logger.info(f"Found profile: @{variation}")
            
            # Respect rate limits
            time.sleep(2)
        
        return results
    
    def analyze_profile_activity(self, username: str) -> Dict[str, Any]:
        """
        Analyze profile activity patterns (public information only)
        """
        profile_data = self.extract_profile_data(username)
        
        if not profile_data:
            return {}
        
        analysis = {
            'username': username,
            'profile_exists': True,
            'account_type': 'private' if profile_data.get('private') else 'public',
            'verification_status': 'verified' if profile_data.get('verified') else 'unverified',
            'engagement_estimate': self._estimate_engagement(profile_data),
            'account_age_estimate': self._estimate_account_age(profile_data),
            'content_analysis': self._analyze_content_patterns(profile_data),
            'extracted_at': datetime.now().isoformat()
        }
        
        return analysis
    
    def _estimate_engagement(self, profile_data: Dict[str, Any]) -> str:
        """Estimate engagement level based on follower/following ratio"""
        followers = profile_data.get('follower_count', 0)
        following = profile_data.get('following_count', 0)
        
        if followers == 0 and following == 0:
            return 'unknown'
        elif followers > following * 10:
            return 'high_influence'
        elif followers > following:
            return 'moderate_influence'
        elif followers < following:
            return 'follower_focused'
        else:
            return 'balanced'
    
    def _estimate_account_age(self, profile_data: Dict[str, Any]) -> str:
        """Estimate account age based on available metrics"""
        video_count = profile_data.get('video_count', 0)
        followers = profile_data.get('follower_count', 0)
        
        if video_count > 100 or followers > 10000:
            return 'established'
        elif video_count > 10 or followers > 100:
            return 'moderate'
        else:
            return 'new_or_inactive'
    
    def _analyze_content_patterns(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content patterns from available data"""
        return {
            'video_count': profile_data.get('video_count', 0),
            'bio_length': len(profile_data.get('bio', '')),
            'has_bio': bool(profile_data.get('bio', '').strip()),
            'display_name_set': bool(profile_data.get('display_name', '').strip()),
            'profile_complete': self._assess_profile_completeness(profile_data)
        }
    
    def _assess_profile_completeness(self, profile_data: Dict[str, Any]) -> float:
        """Assess how complete a profile is (0.0 to 1.0)"""
        score = 0.0
        
        if profile_data.get('display_name', '').strip():
            score += 0.3
        if profile_data.get('bio', '').strip():
            score += 0.3
        if profile_data.get('video_count', 0) > 0:
            score += 0.4
        
        return round(score, 2)

def main():
    """Main function for TikTok analysis"""
    print("🎵 TikTok Profile Analyzer")
    print("=" * 30)
    print()
    
    username = input("Enter TikTok username (without @): ").strip()
    
    if not username:
        print("❌ Please enter a valid username")
        return
    
    analyzer = TikTokAnalyzer()
    
    print(f"\n🔍 Analyzing @{username}...")
    
    # Basic profile analysis
    profile_data = analyzer.extract_profile_data(username)
    
    if profile_data:
        print(f"\n✅ Profile found: @{username}")
        print(f"Display Name: {profile_data.get('display_name', 'N/A')}")
        print(f"Bio: {profile_data.get('bio', 'N/A')}")
        print(f"Followers: {profile_data.get('follower_count', 0):,}")
        print(f"Following: {profile_data.get('following_count', 0):,}")
        print(f"Videos: {profile_data.get('video_count', 0):,}")
        print(f"Verified: {'✅' if profile_data.get('verified') else '❌'}")
        print(f"Private: {'🔒' if profile_data.get('private') else '🔓'}")
    else:
        print(f"❌ Profile not found or inaccessible: @{username}")
    
    # Search for variations
    search_variations = input("\nSearch for username variations? (y/n): ").lower().strip()
    if search_variations == 'y':
        print(f"\n🔍 Searching for variations of '{username}'...")
        variations = analyzer.search_username_variations(username)
        
        if variations:
            print(f"\n📋 Found {len(variations)} profile variations:")
            for i, variation in enumerate(variations, 1):
                print(f"{i}. @{variation.get('username', 'unknown')}")
                print(f"   Display: {variation.get('display_name', 'N/A')}")
                print(f"   Followers: {variation.get('follower_count', 0):,}")
        else:
            print("❌ No variations found")
    
    print("\n✅ Analysis completed!")

if __name__ == "__main__":
    main()