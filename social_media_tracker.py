#!/usr/bin/env python3
"""
Social Media Account Tracker
Program untuk melacak akun sosial media dan mengumpulkan informasi publik
"""

import requests
import json
import time
import re
from datetime import datetime
from urllib.parse import quote
import os
from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SocialMediaTracker:
    def __init__(self, username: str):
        self.username = username
        self.results = {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'platforms': {}
        }
        
        # Headers untuk menghindari deteksi bot
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def check_tiktok(self) -> Dict:
        """Cek akun TikTok"""
        logger.info(f"Checking TikTok account: {self.username}")
        
        try:
            # TikTok Web API (menggunakan endpoint publik)
            url = f"https://www.tiktok.com/@{self.username}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parse data dari HTML response
                content = response.text
                
                # Cari informasi profil
                profile_data = self._extract_tiktok_profile(content)
                
                return {
                    'status': 'found',
                    'url': url,
                    'profile_data': profile_data,
                    'last_checked': datetime.now().isoformat()
                }
            else:
                return {'status': 'not_found', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Error checking TikTok: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def check_instagram(self) -> Dict:
        """Cek akun Instagram"""
        logger.info(f"Checking Instagram account: {self.username}")
        
        try:
            url = f"https://www.instagram.com/{self.username}/"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                profile_data = self._extract_instagram_profile(content)
                
                return {
                    'status': 'found',
                    'url': url,
                    'profile_data': profile_data,
                    'last_checked': datetime.now().isoformat()
                }
            else:
                return {'status': 'not_found', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Error checking Instagram: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def check_twitter(self) -> Dict:
        """Cek akun Twitter/X"""
        logger.info(f"Checking Twitter account: {self.username}")
        
        try:
            url = f"https://twitter.com/{self.username}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                profile_data = self._extract_twitter_profile(content)
                
                return {
                    'status': 'found',
                    'url': url,
                    'profile_data': profile_data,
                    'last_checked': datetime.now().isoformat()
                }
            else:
                return {'status': 'not_found', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Error checking Twitter: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def check_youtube(self) -> Dict:
        """Cek akun YouTube"""
        logger.info(f"Checking YouTube account: {self.username}")
        
        try:
            # YouTube channel URL
            url = f"https://www.youtube.com/@{self.username}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                profile_data = self._extract_youtube_profile(content)
                
                return {
                    'status': 'found',
                    'url': url,
                    'profile_data': profile_data,
                    'last_checked': datetime.now().isoformat()
                }
            else:
                return {'status': 'not_found', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Error checking YouTube: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def check_facebook(self) -> Dict:
        """Cek akun Facebook"""
        logger.info(f"Checking Facebook account: {self.username}")
        
        try:
            url = f"https://www.facebook.com/{self.username}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                profile_data = self._extract_facebook_profile(content)
                
                return {
                    'status': 'found',
                    'url': url,
                    'profile_data': profile_data,
                    'last_checked': datetime.now().isoformat()
                }
            else:
                return {'status': 'not_found', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Error checking Facebook: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _extract_tiktok_profile(self, content: str) -> Dict:
        """Extract profile data dari TikTok HTML"""
        profile_data = {}
        
        try:
            # Cari data JSON di dalam script tag
            json_match = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', content)
            if json_match:
                data = json.loads(json_match.group(1))
                # Parse data struktur TikTok
                if 'defaultScope' in data:
                    user_info = data['defaultScope'].get('webapp.user-detail', {})
                    if 'userInfo' in user_info:
                        user = user_info['userInfo']['user']
                        profile_data = {
                            'display_name': user.get('nickname', ''),
                            'username': user.get('uniqueId', ''),
                            'follower_count': user.get('followerCount', 0),
                            'following_count': user.get('followingCount', 0),
                            'video_count': user.get('videoCount', 0),
                            'verified': user.get('verified', False),
                            'bio': user.get('signature', ''),
                            'avatar_url': user.get('avatarLarger', '')
                        }
        except Exception as e:
            logger.error(f"Error parsing TikTok data: {e}")
        
        return profile_data
    
    def _extract_instagram_profile(self, content: str) -> Dict:
        """Extract profile data dari Instagram HTML"""
        profile_data = {}
        
        try:
            # Cari data JSON di dalam script tag
            json_match = re.search(r'window\._sharedData = (.*?);</script>', content)
            if json_match:
                data = json.loads(json_match.group(1))
                if 'entry_data' in data and 'ProfilePage' in data['entry_data']:
                    user_info = data['entry_data']['ProfilePage'][0]['graphql']['user']
                    profile_data = {
                        'display_name': user_info.get('full_name', ''),
                        'username': user_info.get('username', ''),
                        'follower_count': user_info.get('edge_followed_by', {}).get('count', 0),
                        'following_count': user_info.get('edge_follow', {}).get('count', 0),
                        'post_count': user_info.get('edge_owner_to_timeline_media', {}).get('count', 0),
                        'verified': user_info.get('is_verified', False),
                        'bio': user_info.get('biography', ''),
                        'avatar_url': user_info.get('profile_pic_url_hd', ''),
                        'is_private': user_info.get('is_private', False)
                    }
        except Exception as e:
            logger.error(f"Error parsing Instagram data: {e}")
        
        return profile_data
    
    def _extract_twitter_profile(self, content: str) -> Dict:
        """Extract profile data dari Twitter HTML"""
        profile_data = {}
        
        try:
            # Twitter menggunakan structured data
            json_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content)
            if json_match:
                data = json.loads(json_match.group(1))
                if isinstance(data, dict) and data.get('@type') == 'Person':
                    profile_data = {
                        'display_name': data.get('name', ''),
                        'username': data.get('alternateName', ''),
                        'bio': data.get('description', ''),
                        'verified': 'verified' in str(data)
                    }
        except Exception as e:
            logger.error(f"Error parsing Twitter data: {e}")
        
        return profile_data
    
    def _extract_youtube_profile(self, content: str) -> Dict:
        """Extract profile data dari YouTube HTML"""
        profile_data = {}
        
        try:
            # YouTube menggunakan structured data
            json_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content)
            if json_match:
                data = json.loads(json_match.group(1))
                if isinstance(data, dict) and data.get('@type') == 'Person':
                    profile_data = {
                        'display_name': data.get('name', ''),
                        'username': data.get('alternateName', ''),
                        'description': data.get('description', ''),
                        'verified': 'verified' in str(data)
                    }
        except Exception as e:
            logger.error(f"Error parsing YouTube data: {e}")
        
        return profile_data
    
    def _extract_facebook_profile(self, content: str) -> Dict:
        """Extract profile data dari Facebook HTML"""
        profile_data = {}
        
        try:
            # Facebook menggunakan og:meta tags
            title_match = re.search(r'<meta property="og:title" content="(.*?)"', content)
            description_match = re.search(r'<meta property="og:description" content="(.*?)"', content)
            
            if title_match:
                profile_data['display_name'] = title_match.group(1)
            if description_match:
                profile_data['description'] = description_match.group(1)
                
        except Exception as e:
            logger.error(f"Error parsing Facebook data: {e}")
        
        return profile_data
    
    def search_comments(self, platform: str) -> List[Dict]:
        """Cari komentar dari username di platform tertentu"""
        logger.info(f"Searching comments on {platform} for {self.username}")
        
        comments = []
        
        try:
            if platform == 'tiktok':
                # Implementasi pencarian komentar TikTok
                comments = self._search_tiktok_comments()
            elif platform == 'instagram':
                # Implementasi pencarian komentar Instagram
                comments = self._search_instagram_comments()
            elif platform == 'twitter':
                # Implementasi pencarian komentar Twitter
                comments = self._search_twitter_comments()
            elif platform == 'youtube':
                # Implementasi pencarian komentar YouTube
                comments = self._search_youtube_comments()
                
        except Exception as e:
            logger.error(f"Error searching comments on {platform}: {e}")
        
        return comments
    
    def _search_tiktok_comments(self) -> List[Dict]:
        """Cari komentar di TikTok"""
        # Implementasi pencarian komentar TikTok
        # Note: TikTok memiliki API yang terbatas untuk komentar
        return []
    
    def _search_instagram_comments(self) -> List[Dict]:
        """Cari komentar di Instagram"""
        # Implementasi pencarian komentar Instagram
        return []
    
    def _search_twitter_comments(self) -> List[Dict]:
        """Cari komentar di Twitter"""
        # Implementasi pencarian komentar Twitter
        return []
    
    def _search_youtube_comments(self) -> List[Dict]:
        """Cari komentar di YouTube"""
        # Implementasi pencarian komentar YouTube
        return []
    
    def run_full_scan(self) -> Dict:
        """Jalankan scan lengkap di semua platform"""
        logger.info(f"Starting full scan for username: {self.username}")
        
        platforms = ['tiktok', 'instagram', 'twitter', 'youtube', 'facebook']
        
        for platform in platforms:
            logger.info(f"Scanning {platform}...")
            
            if platform == 'tiktok':
                self.results['platforms']['tiktok'] = self.check_tiktok()
            elif platform == 'instagram':
                self.results['platforms']['instagram'] = self.check_instagram()
            elif platform == 'twitter':
                self.results['platforms']['twitter'] = self.check_twitter()
            elif platform == 'youtube':
                self.results['platforms']['youtube'] = self.check_youtube()
            elif platform == 'facebook':
                self.results['platforms']['facebook'] = self.check_facebook()
            
            # Delay untuk menghindari rate limiting
            time.sleep(2)
        
        # Cari komentar di setiap platform
        for platform in platforms:
            if platform in self.results['platforms'] and self.results['platforms'][platform]['status'] == 'found':
                comments = self.search_comments(platform)
                if comments:
                    self.results['platforms'][platform]['comments'] = comments
        
        return self.results
    
    def save_results(self, filename: str = None) -> str:
        """Simpan hasil ke file JSON"""
        if filename is None:
            filename = f"tracking_results_{self.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {filename}")
        return filename
    
    def print_summary(self):
        """Cetak ringkasan hasil"""
        print(f"\n{'='*50}")
        print(f"TRACKING RESULTS FOR: {self.username.upper()}")
        print(f"{'='*50}")
        print(f"Scan completed at: {self.results['timestamp']}")
        print()
        
        for platform, data in self.results['platforms'].items():
            print(f"📱 {platform.upper()}:")
            if data['status'] == 'found':
                print(f"   ✅ Account found: {data['url']}")
                if 'profile_data' in data and data['profile_data']:
                    profile = data['profile_data']
                    if 'display_name' in profile:
                        print(f"   👤 Display Name: {profile['display_name']}")
                    if 'follower_count' in profile:
                        print(f"   👥 Followers: {profile['follower_count']:,}")
                    if 'bio' in profile:
                        print(f"   📝 Bio: {profile['bio'][:100]}...")
                    if 'verified' in profile and profile['verified']:
                        print(f"   ✅ Verified Account")
            elif data['status'] == 'not_found':
                print(f"   ❌ Account not found")
            else:
                print(f"   ⚠️  Error: {data.get('error', 'Unknown error')}")
            print()

def main():
    """Main function"""
    print("🔍 Social Media Account Tracker")
    print("=" * 40)
    
    # Username yang akan dilacak
    username = "gnkihhhhf"
    
    print(f"Tracking username: {username}")
    print("Starting scan...")
    
    # Buat tracker instance
    tracker = SocialMediaTracker(username)
    
    # Jalankan scan lengkap
    results = tracker.run_full_scan()
    
    # Cetak ringkasan
    tracker.print_summary()
    
    # Simpan hasil
    filename = tracker.save_results()
    print(f"\n📄 Detailed results saved to: {filename}")
    
    print("\n⚠️  DISCLAIMER:")
    print("- This tool only collects publicly available information")
    print("- Respect privacy and platform terms of service")
    print("- Use responsibly and legally")

if __name__ == "__main__":
    main()