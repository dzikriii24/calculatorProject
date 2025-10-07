#!/usr/bin/env python3
"""
Advanced Social Media Tracker
Menggunakan library khusus untuk scraping yang lebih efektif
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
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedSocialMediaTracker:
    def __init__(self, username: str, use_selenium: bool = True):
        self.username = username
        self.results = {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'platforms': {},
            'comments': {},
            'cross_references': []
        }
        
        self.use_selenium = use_selenium
        self.driver = None
        
        if self.use_selenium:
            self._setup_selenium()
    
    def _setup_selenium(self):
        """Setup Selenium WebDriver"""
        try:
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = uc.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
        except Exception as e:
            logger.error(f"Error setting up Selenium: {e}")
            self.use_selenium = False
    
    def check_tiktok_advanced(self) -> Dict:
        """Cek akun TikTok dengan metode advanced"""
        logger.info(f"Advanced TikTok check for: {self.username}")
        
        try:
            if self.use_selenium and self.driver:
                return self._check_tiktok_selenium()
            else:
                return self._check_tiktok_requests()
        except Exception as e:
            logger.error(f"Error in advanced TikTok check: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _check_tiktok_selenium(self) -> Dict:
        """Cek TikTok menggunakan Selenium"""
        try:
            url = f"https://www.tiktok.com/@{self.username}"
            self.driver.get(url)
            
            # Tunggu halaman load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll untuk load konten
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            # Ambil data profil
            profile_data = {}
            
            try:
                # Cari elemen profil
                display_name = self.driver.find_element(By.CSS_SELECTOR, "[data-e2e='user-title']").text
                profile_data['display_name'] = display_name
            except:
                pass
            
            try:
                # Cari follower count
                follower_elem = self.driver.find_element(By.CSS_SELECTOR, "[data-e2e='followers-count']")
                follower_text = follower_elem.text
                profile_data['follower_count'] = self._parse_count(follower_text)
            except:
                pass
            
            try:
                # Cari following count
                following_elem = self.driver.find_element(By.CSS_SELECTOR, "[data-e2e='following-count']")
                following_text = following_elem.text
                profile_data['following_count'] = self._parse_count(following_text)
            except:
                pass
            
            try:
                # Cari bio
                bio_elem = self.driver.find_element(By.CSS_SELECTOR, "[data-e2e='user-bio']")
                profile_data['bio'] = bio_elem.text
            except:
                pass
            
            # Cari video count
            try:
                video_elem = self.driver.find_element(By.CSS_SELECTOR, "[data-e2e='video-count']")
                video_text = video_elem.text
                profile_data['video_count'] = self._parse_count(video_text)
            except:
                pass
            
            return {
                'status': 'found',
                'url': url,
                'profile_data': profile_data,
                'method': 'selenium',
                'last_checked': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _check_tiktok_requests(self) -> Dict:
        """Cek TikTok menggunakan requests"""
        try:
            url = f"https://www.tiktok.com/@{self.username}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                profile_data = {}
                
                # Parse data dari HTML
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.text
                    if self.username.lower() in title.lower():
                        profile_data['page_title'] = title
                
                # Cari meta tags
                meta_description = soup.find('meta', {'name': 'description'})
                if meta_description:
                    profile_data['description'] = meta_description.get('content', '')
                
                return {
                    'status': 'found',
                    'url': url,
                    'profile_data': profile_data,
                    'method': 'requests',
                    'last_checked': datetime.now().isoformat()
                }
            else:
                return {'status': 'not_found', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def check_instagram_advanced(self) -> Dict:
        """Cek akun Instagram dengan metode advanced"""
        logger.info(f"Advanced Instagram check for: {self.username}")
        
        try:
            if self.use_selenium and self.driver:
                return self._check_instagram_selenium()
            else:
                return self._check_instagram_requests()
        except Exception as e:
            logger.error(f"Error in advanced Instagram check: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _check_instagram_selenium(self) -> Dict:
        """Cek Instagram menggunakan Selenium"""
        try:
            url = f"https://www.instagram.com/{self.username}/"
            self.driver.get(url)
            
            # Tunggu halaman load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            profile_data = {}
            
            try:
                # Cari display name
                display_name = self.driver.find_element(By.CSS_SELECTOR, "h2").text
                profile_data['display_name'] = display_name
            except:
                pass
            
            try:
                # Cari bio
                bio_elem = self.driver.find_element(By.CSS_SELECTOR, "div[data-testid='user-bio']")
                profile_data['bio'] = bio_elem.text
            except:
                pass
            
            try:
                # Cari follower count
                follower_elem = self.driver.find_element(By.CSS_SELECTOR, "a[href*='/followers/'] span")
                follower_text = follower_elem.text
                profile_data['follower_count'] = self._parse_count(follower_text)
            except:
                pass
            
            try:
                # Cari following count
                following_elem = self.driver.find_element(By.CSS_SELECTOR, "a[href*='/following/'] span")
                following_text = following_elem.text
                profile_data['following_count'] = self._parse_count(following_text)
            except:
                pass
            
            try:
                # Cari post count
                post_elem = self.driver.find_element(By.CSS_SELECTOR, "div[data-testid='user-post-count'] span")
                post_text = post_elem.text
                profile_data['post_count'] = self._parse_count(post_text)
            except:
                pass
            
            return {
                'status': 'found',
                'url': url,
                'profile_data': profile_data,
                'method': 'selenium',
                'last_checked': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _check_instagram_requests(self) -> Dict:
        """Cek Instagram menggunakan requests"""
        try:
            url = f"https://www.instagram.com/{self.username}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                profile_data = {}
                
                # Parse title
                title_tag = soup.find('title')
                if title_tag:
                    profile_data['page_title'] = title_tag.text
                
                return {
                    'status': 'found',
                    'url': url,
                    'profile_data': profile_data,
                    'method': 'requests',
                    'last_checked': datetime.now().isoformat()
                }
            else:
                return {'status': 'not_found', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def search_comments_advanced(self, platform: str, max_posts: int = 10) -> List[Dict]:
        """Cari komentar dengan metode advanced"""
        logger.info(f"Advanced comment search on {platform} for {self.username}")
        
        comments = []
        
        try:
            if platform == 'tiktok':
                comments = self._search_tiktok_comments_advanced(max_posts)
            elif platform == 'instagram':
                comments = self._search_instagram_comments_advanced(max_posts)
            elif platform == 'twitter':
                comments = self._search_twitter_comments_advanced(max_posts)
            elif platform == 'youtube':
                comments = self._search_youtube_comments_advanced(max_posts)
                
        except Exception as e:
            logger.error(f"Error searching comments on {platform}: {e}")
        
        return comments
    
    def _search_tiktok_comments_advanced(self, max_posts: int) -> List[Dict]:
        """Cari komentar di TikTok dengan metode advanced"""
        comments = []
        
        if not self.use_selenium or not self.driver:
            return comments
        
        try:
            url = f"https://www.tiktok.com/@{self.username}"
            self.driver.get(url)
            
            # Tunggu halaman load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll untuk load lebih banyak konten
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Cari komentar
            comment_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-e2e='comment-item']")
            
            for comment_elem in comment_elements[:max_posts]:
                try:
                    comment_text = comment_elem.find_element(By.CSS_SELECTOR, "[data-e2e='comment-level1']").text
                    comments.append({
                        'text': comment_text,
                        'platform': 'tiktok',
                        'timestamp': datetime.now().isoformat()
                    })
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"Error searching TikTok comments: {e}")
        
        return comments
    
    def _search_instagram_comments_advanced(self, max_posts: int) -> List[Dict]:
        """Cari komentar di Instagram dengan metode advanced"""
        comments = []
        
        if not self.use_selenium or not self.driver:
            return comments
        
        try:
            url = f"https://www.instagram.com/{self.username}/"
            self.driver.get(url)
            
            # Tunggu halaman load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll untuk load konten
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Cari komentar
            comment_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='comment']")
            
            for comment_elem in comment_elements[:max_posts]:
                try:
                    comment_text = comment_elem.text
                    comments.append({
                        'text': comment_text,
                        'platform': 'instagram',
                        'timestamp': datetime.now().isoformat()
                    })
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"Error searching Instagram comments: {e}")
        
        return comments
    
    def _search_twitter_comments_advanced(self, max_posts: int) -> List[Dict]:
        """Cari komentar di Twitter dengan metode advanced"""
        comments = []
        
        if not self.use_selenium or not self.driver:
            return comments
        
        try:
            url = f"https://twitter.com/{self.username}"
            self.driver.get(url)
            
            # Tunggu halaman load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll untuk load konten
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Cari tweet
            tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='tweet']")
            
            for tweet_elem in tweet_elements[:max_posts]:
                try:
                    tweet_text = tweet_elem.find_element(By.CSS_SELECTOR, "[data-testid='tweetText']").text
                    comments.append({
                        'text': tweet_text,
                        'platform': 'twitter',
                        'timestamp': datetime.now().isoformat()
                    })
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"Error searching Twitter comments: {e}")
        
        return comments
    
    def _search_youtube_comments_advanced(self, max_posts: int) -> List[Dict]:
        """Cari komentar di YouTube dengan metode advanced"""
        comments = []
        
        if not self.use_selenium or not self.driver:
            return comments
        
        try:
            url = f"https://www.youtube.com/@{self.username}"
            self.driver.get(url)
            
            # Tunggu halaman load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll untuk load konten
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Cari komentar
            comment_elements = self.driver.find_elements(By.CSS_SELECTOR, "#content-text")
            
            for comment_elem in comment_elements[:max_posts]:
                try:
                    comment_text = comment_elem.text
                    comments.append({
                        'text': comment_text,
                        'platform': 'youtube',
                        'timestamp': datetime.now().isoformat()
                    })
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"Error searching YouTube comments: {e}")
        
        return comments
    
    def _parse_count(self, count_text: str) -> int:
        """Parse count text menjadi angka"""
        try:
            count_text = count_text.replace(',', '').replace('.', '')
            
            if 'K' in count_text.upper():
                return int(float(count_text.upper().replace('K', '')) * 1000)
            elif 'M' in count_text.upper():
                return int(float(count_text.upper().replace('M', '')) * 1000000)
            elif 'B' in count_text.upper():
                return int(float(count_text.upper().replace('B', '')) * 1000000000)
            else:
                return int(count_text)
        except:
            return 0
    
    def run_advanced_scan(self) -> Dict:
        """Jalankan scan advanced di semua platform"""
        logger.info(f"Starting advanced scan for username: {self.username}")
        
        platforms = ['tiktok', 'instagram', 'twitter', 'youtube']
        
        for platform in platforms:
            logger.info(f"Advanced scanning {platform}...")
            
            if platform == 'tiktok':
                self.results['platforms']['tiktok'] = self.check_tiktok_advanced()
            elif platform == 'instagram':
                self.results['platforms']['instagram'] = self.check_instagram_advanced()
            elif platform == 'twitter':
                self.results['platforms']['twitter'] = self.check_twitter_advanced()
            elif platform == 'youtube':
                self.results['platforms']['youtube'] = self.check_youtube_advanced()
            
            # Delay untuk menghindari rate limiting
            time.sleep(3)
        
        # Cari komentar di setiap platform
        for platform in platforms:
            if platform in self.results['platforms'] and self.results['platforms'][platform]['status'] == 'found':
                comments = self.search_comments_advanced(platform)
                if comments:
                    self.results['comments'][platform] = comments
        
        return self.results
    
    def check_twitter_advanced(self) -> Dict:
        """Cek Twitter dengan metode advanced"""
        # Implementasi serupa dengan TikTok dan Instagram
        return {'status': 'not_implemented', 'error': 'Twitter advanced check not implemented yet'}
    
    def check_youtube_advanced(self) -> Dict:
        """Cek YouTube dengan metode advanced"""
        # Implementasi serupa dengan TikTok dan Instagram
        return {'status': 'not_implemented', 'error': 'YouTube advanced check not implemented yet'}
    
    def save_results(self, filename: str = None) -> str:
        """Simpan hasil ke file JSON"""
        if filename is None:
            filename = f"advanced_tracking_results_{self.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Advanced results saved to {filename}")
        return filename
    
    def print_advanced_summary(self):
        """Cetak ringkasan hasil advanced"""
        print(f"\n{'='*60}")
        print(f"ADVANCED TRACKING RESULTS FOR: {self.username.upper()}")
        print(f"{'='*60}")
        print(f"Scan completed at: {self.results['timestamp']}")
        print(f"Method: {'Selenium + Requests' if self.use_selenium else 'Requests Only'}")
        print()
        
        for platform, data in self.results['platforms'].items():
            print(f"📱 {platform.upper()}:")
            if data['status'] == 'found':
                print(f"   ✅ Account found: {data['url']}")
                print(f"   🔧 Method: {data.get('method', 'unknown')}")
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
        
        # Tampilkan komentar yang ditemukan
        if self.results['comments']:
            print(f"💬 COMMENTS FOUND:")
            for platform, comments in self.results['comments'].items():
                if comments:
                    print(f"   📱 {platform.upper()}: {len(comments)} comments found")
                    for i, comment in enumerate(comments[:3]):  # Tampilkan 3 komentar pertama
                        print(f"      {i+1}. {comment['text'][:100]}...")
            print()
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()

def main():
    """Main function untuk advanced tracker"""
    print("🔍 Advanced Social Media Account Tracker")
    print("=" * 50)
    
    # Username yang akan dilacak
    username = "gnkihhhhf"
    
    print(f"Tracking username: {username}")
    print("Starting advanced scan...")
    
    # Buat tracker instance
    tracker = AdvancedSocialMediaTracker(username, use_selenium=True)
    
    try:
        # Jalankan scan advanced
        results = tracker.run_advanced_scan()
        
        # Cetak ringkasan
        tracker.print_advanced_summary()
        
        # Simpan hasil
        filename = tracker.save_results()
        print(f"\n📄 Advanced results saved to: {filename}")
        
    finally:
        # Cleanup
        tracker.cleanup()
    
    print("\n⚠️  DISCLAIMER:")
    print("- This tool only collects publicly available information")
    print("- Respect privacy and platform terms of service")
    print("- Use responsibly and legally")
    print("- Some features may require additional setup (Chrome driver)")

if __name__ == "__main__":
    main()