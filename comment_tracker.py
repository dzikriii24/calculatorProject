#!/usr/bin/env python3
"""
Comment and Interaction Tracker
Melacak komentar dan interaksi dari username di berbagai platform
"""

import requests
import json
import time
import re
from datetime import datetime, timedelta
from urllib.parse import quote, urljoin
import os
from typing import Dict, List, Optional
import logging
from bs4 import BeautifulSoup
import sqlite3
from dataclasses import dataclass

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Comment:
    platform: str
    content: str
    timestamp: str
    post_url: str
    author: str
    likes: int = 0
    replies: int = 0

class CommentTracker:
    def __init__(self, username: str):
        self.username = username
        self.comments_db = f"comments_{username}.db"
        self.setup_database()
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def setup_database(self):
        """Setup SQLite database untuk menyimpan komentar"""
        conn = sqlite3.connect(self.comments_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                post_url TEXT,
                author TEXT NOT NULL,
                likes INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_comment(self, comment: Comment):
        """Simpan komentar ke database"""
        conn = sqlite3.connect(self.comments_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO comments (platform, content, timestamp, post_url, author, likes, replies)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (comment.platform, comment.content, comment.timestamp, comment.post_url, comment.author, comment.likes, comment.replies))
        
        conn.commit()
        conn.close()
    
    def get_existing_comments(self) -> List[Comment]:
        """Ambil komentar yang sudah ada dari database"""
        conn = sqlite3.connect(self.comments_db)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM comments ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        comments = []
        for row in rows:
            comment = Comment(
                platform=row[1],
                content=row[2],
                timestamp=row[3],
                post_url=row[4],
                author=row[5],
                likes=row[6],
                replies=row[7]
            )
            comments.append(comment)
        
        conn.close()
        return comments
    
    def search_tiktok_comments(self, max_pages: int = 5) -> List[Comment]:
        """Cari komentar di TikTok"""
        logger.info(f"Searching TikTok comments for {self.username}")
        comments = []
        
        try:
            # TikTok search URL
            search_url = f"https://www.tiktok.com/search?q={quote(self.username)}"
            
            response = requests.get(search_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                logger.error(f"TikTok search failed: HTTP {response.status_code}")
                return comments
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari video links
            video_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/video/' in href and href not in video_links:
                    video_links.append(href)
            
            # Cek setiap video untuk komentar
            for video_link in video_links[:max_pages]:
                try:
                    video_url = urljoin('https://www.tiktok.com', video_link)
                    video_comments = self._extract_tiktok_video_comments(video_url)
                    comments.extend(video_comments)
                    time.sleep(2)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error processing TikTok video {video_link}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error searching TikTok comments: {e}")
        
        return comments
    
    def _extract_tiktok_video_comments(self, video_url: str) -> List[Comment]:
        """Extract komentar dari video TikTok"""
        comments = []
        
        try:
            response = requests.get(video_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                return comments
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari komentar yang mengandung username
            comment_elements = soup.find_all('div', class_='comment-item')
            
            for comment_elem in comment_elements:
                try:
                    comment_text = comment_elem.get_text(strip=True)
                    if self.username.lower() in comment_text.lower():
                        comment = Comment(
                            platform='tiktok',
                            content=comment_text,
                            timestamp=datetime.now().isoformat(),
                            post_url=video_url,
                            author=self.username
                        )
                        comments.append(comment)
                except Exception as e:
                    continue
            
        except Exception as e:
            logger.error(f"Error extracting TikTok video comments: {e}")
        
        return comments
    
    def search_instagram_comments(self, max_posts: int = 10) -> List[Comment]:
        """Cari komentar di Instagram"""
        logger.info(f"Searching Instagram comments for {self.username}")
        comments = []
        
        try:
            # Instagram search URL
            search_url = f"https://www.instagram.com/explore/tags/{quote(self.username)}/"
            
            response = requests.get(search_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                logger.error(f"Instagram search failed: HTTP {response.status_code}")
                return comments
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari post links
            post_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/p/' in href and href not in post_links:
                    post_links.append(href)
            
            # Cek setiap post untuk komentar
            for post_link in post_links[:max_posts]:
                try:
                    post_url = urljoin('https://www.instagram.com', post_link)
                    post_comments = self._extract_instagram_post_comments(post_url)
                    comments.extend(post_comments)
                    time.sleep(2)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error processing Instagram post {post_link}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error searching Instagram comments: {e}")
        
        return comments
    
    def _extract_instagram_post_comments(self, post_url: str) -> List[Comment]:
        """Extract komentar dari post Instagram"""
        comments = []
        
        try:
            response = requests.get(post_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                return comments
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari komentar yang mengandung username
            comment_elements = soup.find_all('span', class_='comment')
            
            for comment_elem in comment_elements:
                try:
                    comment_text = comment_elem.get_text(strip=True)
                    if self.username.lower() in comment_text.lower():
                        comment = Comment(
                            platform='instagram',
                            content=comment_text,
                            timestamp=datetime.now().isoformat(),
                            post_url=post_url,
                            author=self.username
                        )
                        comments.append(comment)
                except Exception as e:
                    continue
            
        except Exception as e:
            logger.error(f"Error extracting Instagram post comments: {e}")
        
        return comments
    
    def search_twitter_comments(self, max_tweets: int = 20) -> List[Comment]:
        """Cari komentar di Twitter"""
        logger.info(f"Searching Twitter comments for {self.username}")
        comments = []
        
        try:
            # Twitter search URL
            search_url = f"https://twitter.com/search?q={quote(self.username)}&src=typed_query"
            
            response = requests.get(search_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                logger.error(f"Twitter search failed: HTTP {response.status_code}")
                return comments
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari tweet elements
            tweet_elements = soup.find_all('div', {'data-testid': 'tweet'})
            
            for tweet_elem in tweet_elements[:max_tweets]:
                try:
                    tweet_text = tweet_elem.get_text(strip=True)
                    if self.username.lower() in tweet_text.lower():
                        comment = Comment(
                            platform='twitter',
                            content=tweet_text,
                            timestamp=datetime.now().isoformat(),
                            post_url=search_url,
                            author=self.username
                        )
                        comments.append(comment)
                except Exception as e:
                    continue
            
        except Exception as e:
            logger.error(f"Error searching Twitter comments: {e}")
        
        return comments
    
    def search_youtube_comments(self, max_videos: int = 10) -> List[Comment]:
        """Cari komentar di YouTube"""
        logger.info(f"Searching YouTube comments for {self.username}")
        comments = []
        
        try:
            # YouTube search URL
            search_url = f"https://www.youtube.com/results?search_query={quote(self.username)}"
            
            response = requests.get(search_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                logger.error(f"YouTube search failed: HTTP {response.status_code}")
                return comments
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari video links
            video_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/watch?v=' in href and href not in video_links:
                    video_links.append(href)
            
            # Cek setiap video untuk komentar
            for video_link in video_links[:max_videos]:
                try:
                    video_url = urljoin('https://www.youtube.com', video_link)
                    video_comments = self._extract_youtube_video_comments(video_url)
                    comments.extend(video_comments)
                    time.sleep(2)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error processing YouTube video {video_link}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error searching YouTube comments: {e}")
        
        return comments
    
    def _extract_youtube_video_comments(self, video_url: str) -> List[Comment]:
        """Extract komentar dari video YouTube"""
        comments = []
        
        try:
            response = requests.get(video_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                return comments
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari komentar yang mengandung username
            comment_elements = soup.find_all('div', {'id': 'content-text'})
            
            for comment_elem in comment_elements:
                try:
                    comment_text = comment_elem.get_text(strip=True)
                    if self.username.lower() in comment_text.lower():
                        comment = Comment(
                            platform='youtube',
                            content=comment_text,
                            timestamp=datetime.now().isoformat(),
                            post_url=video_url,
                            author=self.username
                        )
                        comments.append(comment)
                except Exception as e:
                    continue
            
        except Exception as e:
            logger.error(f"Error extracting YouTube video comments: {e}")
        
        return comments
    
    def search_reddit_comments(self, max_posts: int = 15) -> List[Comment]:
        """Cari komentar di Reddit"""
        logger.info(f"Searching Reddit comments for {self.username}")
        comments = []
        
        try:
            # Reddit search URL
            search_url = f"https://www.reddit.com/search/?q={quote(self.username)}"
            
            response = requests.get(search_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                logger.error(f"Reddit search failed: HTTP {response.status_code}")
                return comments
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari post links
            post_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/r/' in href and '/comments/' in href and href not in post_links:
                    post_links.append(href)
            
            # Cek setiap post untuk komentar
            for post_link in post_links[:max_posts]:
                try:
                    post_url = urljoin('https://www.reddit.com', post_link)
                    post_comments = self._extract_reddit_post_comments(post_url)
                    comments.extend(post_comments)
                    time.sleep(2)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error processing Reddit post {post_link}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error searching Reddit comments: {e}")
        
        return comments
    
    def _extract_reddit_post_comments(self, post_url: str) -> List[Comment]:
        """Extract komentar dari post Reddit"""
        comments = []
        
        try:
            response = requests.get(post_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                return comments
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari komentar yang mengandung username
            comment_elements = soup.find_all('div', {'data-testid': 'comment'})
            
            for comment_elem in comment_elements:
                try:
                    comment_text = comment_elem.get_text(strip=True)
                    if self.username.lower() in comment_text.lower():
                        comment = Comment(
                            platform='reddit',
                            content=comment_text,
                            timestamp=datetime.now().isoformat(),
                            post_url=post_url,
                            author=self.username
                        )
                        comments.append(comment)
                except Exception as e:
                    continue
            
        except Exception as e:
            logger.error(f"Error extracting Reddit post comments: {e}")
        
        return comments
    
    def run_full_comment_search(self) -> Dict:
        """Jalankan pencarian komentar lengkap di semua platform"""
        logger.info(f"Starting full comment search for username: {self.username}")
        
        all_comments = []
        platforms = ['tiktok', 'instagram', 'twitter', 'youtube', 'reddit']
        
        for platform in platforms:
            logger.info(f"Searching comments on {platform}...")
            
            if platform == 'tiktok':
                comments = self.search_tiktok_comments()
            elif platform == 'instagram':
                comments = self.search_instagram_comments()
            elif platform == 'twitter':
                comments = self.search_twitter_comments()
            elif platform == 'youtube':
                comments = self.search_youtube_comments()
            elif platform == 'reddit':
                comments = self.search_reddit_comments()
            
            # Simpan komentar ke database
            for comment in comments:
                self.save_comment(comment)
            
            all_comments.extend(comments)
            
            # Delay untuk menghindari rate limiting
            time.sleep(3)
        
        # Buat ringkasan hasil
        results = {
            'username': self.username,
            'timestamp': datetime.now().isoformat(),
            'total_comments': len(all_comments),
            'platforms': {},
            'comments': []
        }
        
        # Kelompokkan komentar berdasarkan platform
        for platform in platforms:
            platform_comments = [c for c in all_comments if c.platform == platform]
            results['platforms'][platform] = {
                'count': len(platform_comments),
                'comments': [
                    {
                        'content': c.content,
                        'timestamp': c.timestamp,
                        'post_url': c.post_url,
                        'likes': c.likes,
                        'replies': c.replies
                    } for c in platform_comments
                ]
            }
        
        return results
    
    def generate_comment_report(self) -> str:
        """Generate laporan komentar dalam format HTML"""
        comments = self.get_existing_comments()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Comment Report for {self.username}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .platform {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .comment {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; border-left: 3px solid #007bff; }}
                .timestamp {{ color: #666; font-size: 0.9em; }}
                .content {{ margin: 5px 0; }}
                .url {{ color: #007bff; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Comment Report for {self.username}</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Total comments found: {len(comments)}</p>
            </div>
        """
        
        # Kelompokkan komentar berdasarkan platform
        platforms = {}
        for comment in comments:
            if comment.platform not in platforms:
                platforms[comment.platform] = []
            platforms[comment.platform].append(comment)
        
        # Tampilkan komentar per platform
        for platform, platform_comments in platforms.items():
            html += f"""
            <div class="platform">
                <h2>{platform.upper()} ({len(platform_comments)} comments)</h2>
            """
            
            for comment in platform_comments:
                html += f"""
                <div class="comment">
                    <div class="content">{comment.content}</div>
                    <div class="timestamp">{comment.timestamp}</div>
                    <a href="{comment.post_url}" class="url" target="_blank">View Post</a>
                </div>
                """
            
            html += "</div>"
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def save_comment_report(self, filename: str = None) -> str:
        """Simpan laporan komentar ke file HTML"""
        if filename is None:
            filename = f"comment_report_{self.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_content = self.generate_comment_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Comment report saved to {filename}")
        return filename

def main():
    """Main function untuk comment tracker"""
    print("💬 Comment and Interaction Tracker")
    print("=" * 40)
    
    # Username yang akan dilacak
    username = "gnkihhhhf"
    
    print(f"Tracking comments for username: {username}")
    print("Starting comment search...")
    
    # Buat tracker instance
    tracker = CommentTracker(username)
    
    # Jalankan pencarian komentar lengkap
    results = tracker.run_full_comment_search()
    
    # Tampilkan ringkasan
    print(f"\n{'='*50}")
    print(f"COMMENT SEARCH RESULTS FOR: {username.upper()}")
    print(f"{'='*50}")
    print(f"Total comments found: {results['total_comments']}")
    print()
    
    for platform, data in results['platforms'].items():
        print(f"📱 {platform.upper()}: {data['count']} comments")
        if data['count'] > 0:
            for i, comment in enumerate(data['comments'][:3]):  # Tampilkan 3 komentar pertama
                print(f"   {i+1}. {comment['content'][:100]}...")
            if data['count'] > 3:
                print(f"   ... and {data['count'] - 3} more comments")
        print()
    
    # Simpan laporan
    report_filename = tracker.save_comment_report()
    print(f"📄 Detailed comment report saved to: {report_filename}")
    
    print("\n⚠️  DISCLAIMER:")
    print("- This tool only searches for publicly available comments")
    print("- Respect privacy and platform terms of service")
    print("- Use responsibly and legally")

if __name__ == "__main__":
    main()