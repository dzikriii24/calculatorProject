#!/usr/bin/env python3
"""
Social Media Profile Tracker
============================

A comprehensive tool for monitoring public social media profiles across multiple platforms.
This tool respects platform terms of service and focuses on publicly available information.

IMPORTANT LEGAL NOTICE:
- This tool is for educational and legitimate monitoring purposes only
- Always respect platform terms of service and rate limits
- Do not use for harassment, stalking, or illegal activities
- Ensure you have proper authorization before monitoring accounts
- Be aware of local privacy laws and regulations

Author: Social Media Monitoring Tool
Version: 1.0.0
"""

import requests
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import quote
import logging
from dataclasses import dataclass
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('social_media_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ProfileInfo:
    """Data class for storing profile information"""
    platform: str
    username: str
    display_name: str = ""
    bio: str = ""
    followers: int = 0
    following: int = 0
    posts_count: int = 0
    verified: bool = False
    profile_pic_url: str = ""
    external_links: List[str] = None
    last_post_date: str = ""
    account_created: str = ""
    is_private: bool = False
    additional_info: Dict[str, Any] = None

    def __post_init__(self):
        if self.external_links is None:
            self.external_links = []
        if self.additional_info is None:
            self.additional_info = {}

class SocialMediaTracker:
    """Main class for tracking social media profiles"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.rate_limit_delay = 2  # seconds between requests
        self.results = {}
        
    def _make_request(self, url: str, headers: Dict = None) -> Optional[requests.Response]:
        """Make a rate-limited request"""
        try:
            time.sleep(self.rate_limit_delay)
            response = self.session.get(url, headers=headers or {}, timeout=10)
            logger.info(f"Request to {url} - Status: {response.status_code}")
            return response
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None

    def check_tiktok_profile(self, username: str) -> Optional[ProfileInfo]:
        """
        Check TikTok profile information
        Note: This uses publicly available information only
        """
        logger.info(f"Checking TikTok profile: {username}")
        
        # Clean username
        username = username.replace('@', '').strip()
        
        try:
            # Try to access public profile page
            url = f"https://www.tiktok.com/@{username}"
            response = self._make_request(url)
            
            if not response or response.status_code != 200:
                logger.warning(f"TikTok profile not found or inaccessible: {username}")
                return None
            
            # Basic profile info extraction (this is a simplified version)
            profile = ProfileInfo(
                platform="TikTok",
                username=username,
                display_name="",
                bio="",
                followers=0,
                following=0,
                posts_count=0,
                verified=False,
                is_private=False
            )
            
            # Note: Real implementation would need proper HTML parsing
            # and respect to TikTok's robots.txt and terms of service
            
            return profile
            
        except Exception as e:
            logger.error(f"Error checking TikTok profile {username}: {e}")
            return None

    def check_instagram_profile(self, username: str) -> Optional[ProfileInfo]:
        """
        Check Instagram profile information
        Note: Instagram has strict anti-scraping measures
        """
        logger.info(f"Checking Instagram profile: {username}")
        
        username = username.replace('@', '').strip()
        
        try:
            # Instagram requires proper authentication for most data
            # This is a placeholder for legitimate API usage
            url = f"https://www.instagram.com/{username}/"
            response = self._make_request(url)
            
            if not response:
                return None
                
            profile = ProfileInfo(
                platform="Instagram",
                username=username,
                display_name="",
                bio="",
                followers=0,
                following=0,
                posts_count=0,
                verified=False,
                is_private=True  # Assume private by default
            )
            
            # Note: Real implementation would require Instagram Basic Display API
            # or Instagram Graph API for legitimate access
            
            return profile
            
        except Exception as e:
            logger.error(f"Error checking Instagram profile {username}: {e}")
            return None

    def check_twitter_profile(self, username: str) -> Optional[ProfileInfo]:
        """
        Check Twitter/X profile information
        Note: Twitter API v2 requires authentication
        """
        logger.info(f"Checking Twitter profile: {username}")
        
        username = username.replace('@', '').strip()
        
        try:
            # Twitter requires API keys for most operations
            # This is a placeholder for legitimate API usage
            url = f"https://twitter.com/{username}"
            response = self._make_request(url)
            
            if not response:
                return None
                
            profile = ProfileInfo(
                platform="Twitter/X",
                username=username,
                display_name="",
                bio="",
                followers=0,
                following=0,
                posts_count=0,
                verified=False,
                is_private=False
            )
            
            # Note: Real implementation would use Twitter API v2
            # with proper authentication and rate limiting
            
            return profile
            
        except Exception as e:
            logger.error(f"Error checking Twitter profile {username}: {e}")
            return None

    def check_youtube_channel(self, username: str) -> Optional[ProfileInfo]:
        """
        Check YouTube channel information
        """
        logger.info(f"Checking YouTube channel: {username}")
        
        try:
            # Try both username and channel ID formats
            urls = [
                f"https://www.youtube.com/@{username}",
                f"https://www.youtube.com/c/{username}",
                f"https://www.youtube.com/user/{username}"
            ]
            
            for url in urls:
                response = self._make_request(url)
                if response and response.status_code == 200:
                    profile = ProfileInfo(
                        platform="YouTube",
                        username=username,
                        display_name="",
                        bio="",
                        followers=0,  # subscribers
                        following=0,
                        posts_count=0,  # videos
                        verified=False,
                        is_private=False
                    )
                    
                    # Note: Real implementation would use YouTube Data API v3
                    # for detailed channel information
                    
                    return profile
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking YouTube channel {username}: {e}")
            return None

    def search_across_platforms(self, username: str) -> Dict[str, ProfileInfo]:
        """
        Search for a username across multiple social media platforms
        """
        logger.info(f"Starting comprehensive search for username: {username}")
        
        results = {}
        
        # Check each platform
        platforms = [
            ("TikTok", self.check_tiktok_profile),
            ("Instagram", self.check_instagram_profile),
            ("Twitter", self.check_twitter_profile),
            ("YouTube", self.check_youtube_channel),
        ]
        
        for platform_name, check_function in platforms:
            try:
                logger.info(f"Checking {platform_name}...")
                profile = check_function(username)
                if profile:
                    results[platform_name] = profile
                    logger.info(f"Found profile on {platform_name}")
                else:
                    logger.info(f"No profile found on {platform_name}")
            except Exception as e:
                logger.error(f"Error checking {platform_name}: {e}")
        
        self.results[username] = results
        return results

    def generate_report(self, username: str) -> str:
        """
        Generate a comprehensive report for a username
        """
        if username not in self.results:
            return f"No data found for username: {username}"
        
        report = []
        report.append("=" * 60)
        report.append(f"SOCIAL MEDIA PROFILE REPORT")
        report.append(f"Username: {username}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)
        report.append("")
        
        results = self.results[username]
        
        if not results:
            report.append("❌ No profiles found on any platform")
            return "\n".join(report)
        
        for platform, profile in results.items():
            report.append(f"🔍 {platform}")
            report.append("-" * 30)
            report.append(f"Username: @{profile.username}")
            report.append(f"Display Name: {profile.display_name or 'N/A'}")
            report.append(f"Bio: {profile.bio[:100] + '...' if len(profile.bio) > 100 else profile.bio or 'N/A'}")
            report.append(f"Followers: {profile.followers:,}")
            report.append(f"Following: {profile.following:,}")
            report.append(f"Posts: {profile.posts_count:,}")
            report.append(f"Verified: {'✅' if profile.verified else '❌'}")
            report.append(f"Private: {'🔒' if profile.is_private else '🔓'}")
            
            if profile.external_links:
                report.append(f"External Links: {', '.join(profile.external_links)}")
            
            report.append("")
        
        # Add disclaimer
        report.append("⚠️  IMPORTANT DISCLAIMER:")
        report.append("This information is based on publicly available data only.")
        report.append("Always respect privacy rights and platform terms of service.")
        report.append("Do not use this information for harassment or illegal activities.")
        
        return "\n".join(report)

    def save_report(self, username: str, filename: str = None):
        """Save the report to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"social_media_report_{username}_{timestamp}.txt"
        
        report = self.generate_report(username)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved to: {filename}")
        return filename

def main():
    """Main function to run the social media tracker"""
    print("🔍 Social Media Profile Tracker")
    print("=" * 40)
    print()
    
    # Important disclaimer
    print("⚠️  IMPORTANT LEGAL NOTICE:")
    print("This tool is for educational and legitimate purposes only.")
    print("Always respect platform terms of service and privacy rights.")
    print("Do not use for harassment, stalking, or illegal activities.")
    print()
    
    # Get username from user
    username = input("Enter username to search: ").strip()
    
    if not username:
        print("❌ Please enter a valid username")
        return
    
    # Initialize tracker
    tracker = SocialMediaTracker()
    
    print(f"\n🔍 Searching for '{username}' across social media platforms...")
    print("This may take a few minutes due to rate limiting...")
    print()
    
    # Perform search
    results = tracker.search_across_platforms(username)
    
    # Display results
    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)
    
    if results:
        for platform, profile in results.items():
            print(f"\n✅ Found on {platform}:")
            print(f"   Username: @{profile.username}")
            print(f"   Display Name: {profile.display_name or 'N/A'}")
            print(f"   Private Account: {'Yes' if profile.is_private else 'No'}")
    else:
        print("\n❌ No profiles found on any platform")
    
    # Generate and save report
    if results:
        save_report = input("\nSave detailed report to file? (y/n): ").lower().strip()
        if save_report == 'y':
            filename = tracker.save_report(username)
            print(f"📄 Report saved as: {filename}")
    
    print("\n✅ Search completed!")

if __name__ == "__main__":
    main()