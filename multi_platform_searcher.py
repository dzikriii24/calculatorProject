#!/usr/bin/env python3
"""
Multi-Platform Social Media Searcher
====================================

Comprehensive tool for searching across multiple social media platforms
for a specific username. This tool aggregates results from various platforms
and provides detailed analysis.

IMPORTANT: This tool is for legitimate research purposes only.
Always respect platform terms of service and privacy rights.
"""

import asyncio
import concurrent.futures
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import logging
from dataclasses import dataclass, asdict
import os
import sys

# Import our specialized analyzers
from social_media_tracker import SocialMediaTracker, ProfileInfo
from tiktok_analyzer import TikTokAnalyzer
from instagram_analyzer import InstagramAnalyzer
from twitter_analyzer import TwitterAnalyzer

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Comprehensive search result for a platform"""
    platform: str
    username: str
    found: bool
    profile_data: Dict[str, Any]
    analysis: Dict[str, Any]
    variations_found: List[Dict[str, Any]]
    search_timestamp: str
    error_message: str = ""

class MultiPlatformSearcher:
    """Main class for multi-platform social media searching"""
    
    def __init__(self):
        self.platforms = {
            'tiktok': TikTokAnalyzer(),
            'instagram': InstagramAnalyzer(),
            'twitter': TwitterAnalyzer()
        }
        self.results = {}
        
    def search_all_platforms(self, username: str, include_variations: bool = True) -> Dict[str, SearchResult]:
        """
        Search for a username across all supported platforms
        """
        logger.info(f"Starting comprehensive search for username: {username}")
        
        results = {}
        
        # Search each platform
        for platform_name, analyzer in self.platforms.items():
            try:
                logger.info(f"Searching {platform_name}...")
                result = self._search_single_platform(
                    platform_name, analyzer, username, include_variations
                )
                results[platform_name] = result
                
                # Add delay between platforms to be respectful
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"Error searching {platform_name}: {e}")
                results[platform_name] = SearchResult(
                    platform=platform_name,
                    username=username,
                    found=False,
                    profile_data={},
                    analysis={},
                    variations_found=[],
                    search_timestamp=datetime.now().isoformat(),
                    error_message=str(e)
                )
        
        self.results[username] = results
        return results
    
    def _search_single_platform(self, platform: str, analyzer: Any, username: str, 
                               include_variations: bool) -> SearchResult:
        """Search a single platform for the username"""
        
        search_timestamp = datetime.now().isoformat()
        
        try:
            # Extract basic profile data
            if hasattr(analyzer, 'extract_profile_data'):
                profile_data = analyzer.extract_profile_data(username)
            else:
                profile_data = {}
            
            found = bool(profile_data and profile_data.get('username'))
            
            # Perform analysis if profile found
            analysis = {}
            if found:
                if hasattr(analyzer, 'analyze_profile_patterns'):
                    analysis = analyzer.analyze_profile_patterns(username)
                elif hasattr(analyzer, 'analyze_profile_activity'):
                    analysis = analyzer.analyze_profile_activity(username)
                elif hasattr(analyzer, 'analyze_account_patterns'):
                    analysis = analyzer.analyze_account_patterns(username)
            
            # Search for variations if requested
            variations_found = []
            if include_variations and hasattr(analyzer, 'search_username_variations'):
                try:
                    variations_found = analyzer.search_username_variations(username)
                except Exception as e:
                    logger.warning(f"Could not search variations on {platform}: {e}")
            
            return SearchResult(
                platform=platform,
                username=username,
                found=found,
                profile_data=profile_data,
                analysis=analysis,
                variations_found=variations_found,
                search_timestamp=search_timestamp
            )
            
        except Exception as e:
            logger.error(f"Error searching {platform} for {username}: {e}")
            return SearchResult(
                platform=platform,
                username=username,
                found=False,
                profile_data={},
                analysis={},
                variations_found=[],
                search_timestamp=search_timestamp,
                error_message=str(e)
            )
    
    def generate_comprehensive_report(self, username: str) -> str:
        """Generate a comprehensive report across all platforms"""
        
        if username not in self.results:
            return f"No search results found for username: {username}"
        
        results = self.results[username]
        
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE SOCIAL MEDIA SEARCH REPORT")
        report.append("=" * 80)
        report.append(f"Target Username: {username}")
        report.append(f"Search Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Platforms Searched: {', '.join(results.keys())}")
        report.append("=" * 80)
        report.append("")
        
        # Executive Summary
        found_platforms = [name for name, result in results.items() if result.found]
        total_variations = sum(len(result.variations_found) for result in results.values())
        
        report.append("📊 EXECUTIVE SUMMARY")
        report.append("-" * 40)
        report.append(f"✅ Profiles Found: {len(found_platforms)}/{len(results)} platforms")
        report.append(f"🔍 Total Variations Found: {total_variations}")
        report.append(f"🎯 Primary Matches: {', '.join(found_platforms) if found_platforms else 'None'}")
        report.append("")
        
        # Detailed Results by Platform
        for platform_name, result in results.items():
            report.append(f"🔍 {platform_name.upper()} ANALYSIS")
            report.append("-" * 50)
            
            if result.error_message:
                report.append(f"❌ Error: {result.error_message}")
                report.append("")
                continue
            
            if result.found:
                profile = result.profile_data
                report.append(f"✅ Profile Found: @{profile.get('username', username)}")
                report.append(f"📝 Display Name: {profile.get('display_name', 'N/A')}")
                
                # Platform-specific metrics
                if platform_name == 'tiktok':
                    report.append(f"👥 Followers: {profile.get('follower_count', 0):,}")
                    report.append(f"➡️ Following: {profile.get('following_count', 0):,}")
                    report.append(f"🎬 Videos: {profile.get('video_count', 0):,}")
                elif platform_name == 'instagram':
                    report.append(f"👥 Followers: {profile.get('follower_count', 0):,}")
                    report.append(f"➡️ Following: {profile.get('following_count', 0):,}")
                    report.append(f"📸 Posts: {profile.get('posts_count', 0):,}")
                    report.append(f"💼 Business: {'Yes' if profile.get('business_account') else 'No'}")
                elif platform_name == 'twitter':
                    report.append(f"👥 Followers: {profile.get('follower_count', 0):,}")
                    report.append(f"➡️ Following: {profile.get('following_count', 0):,}")
                    report.append(f"🐦 Tweets: {profile.get('tweets_count', 0):,}")
                
                report.append(f"✅ Verified: {'Yes' if profile.get('verified') else 'No'}")
                report.append(f"🔒 Private: {'Yes' if profile.get('private', profile.get('protected')) else 'No'}")
                
                # Bio information
                bio = profile.get('bio', '')
                if bio:
                    report.append(f"📄 Bio: {bio[:200]}{'...' if len(bio) > 200 else ''}")
                
                # External links
                external_url = profile.get('external_url', profile.get('website', ''))
                if external_url:
                    report.append(f"🔗 External Link: {external_url}")
                
                # Analysis results
                if result.analysis and 'error' not in result.analysis:
                    analysis = result.analysis
                    report.append(f"📊 Account Type: {analysis.get('account_type', 'N/A')}")
                    
                    # Platform-specific analysis
                    if 'engagement_potential' in analysis:
                        engagement = analysis['engagement_potential']
                        report.append(f"📈 Engagement Level: {engagement.get('engagement_category', 'N/A')}")
                    
                    if 'authenticity_score' in analysis:
                        score = analysis['authenticity_score']
                        report.append(f"🎯 Authenticity Score: {score}/1.0")
                
            else:
                report.append("❌ No profile found with this exact username")
            
            # Username variations
            if result.variations_found:
                report.append(f"\n🔄 SIMILAR USERNAMES FOUND ({len(result.variations_found)}):")
                for i, variation in enumerate(result.variations_found[:5], 1):  # Limit to top 5
                    var_username = variation.get('username', 'unknown')
                    var_display = variation.get('display_name', 'N/A')
                    var_followers = variation.get('follower_count', 0)
                    report.append(f"   {i}. @{var_username} - {var_display} ({var_followers:,} followers)")
            
            report.append("")
        
        # Cross-Platform Analysis
        if len(found_platforms) > 1:
            report.append("🔗 CROSS-PLATFORM ANALYSIS")
            report.append("-" * 40)
            
            # Compare follower counts across platforms
            follower_data = {}
            for platform in found_platforms:
                result = results[platform]
                followers = result.profile_data.get('follower_count', 0)
                follower_data[platform] = followers
            
            if follower_data:
                sorted_platforms = sorted(follower_data.items(), key=lambda x: x[1], reverse=True)
                report.append("👥 Follower Comparison:")
                for platform, followers in sorted_platforms:
                    report.append(f"   {platform.capitalize()}: {followers:,}")
            
            # Check for consistent display names
            display_names = set()
            for platform in found_platforms:
                result = results[platform]
                display_name = result.profile_data.get('display_name', '').strip()
                if display_name:
                    display_names.add(display_name.lower())
            
            if len(display_names) == 1:
                report.append("✅ Consistent display name across platforms")
            elif len(display_names) > 1:
                report.append("⚠️ Different display names across platforms")
            
            report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 40)
        
        if not found_platforms:
            report.append("• No profiles found with this exact username")
            report.append("• Consider checking variations or alternative spellings")
            report.append("• The user might be using different usernames on different platforms")
        else:
            report.append(f"• Active presence confirmed on: {', '.join(found_platforms)}")
            if total_variations > 0:
                report.append(f"• {total_variations} similar usernames found - check for related accounts")
            
            # Check for potential impersonation indicators
            verification_status = {}
            for platform in found_platforms:
                result = results[platform]
                verified = result.profile_data.get('verified', False)
                verification_status[platform] = verified
            
            verified_count = sum(verification_status.values())
            if verified_count > 0:
                report.append(f"• Verified on {verified_count} platform(s)")
            else:
                report.append("• No verified accounts found - be cautious of impersonation")
        
        report.append("")
        
        # Legal Disclaimer
        report.append("⚖️ LEGAL DISCLAIMER")
        report.append("-" * 40)
        report.append("• This report contains only publicly available information")
        report.append("• All data was collected in compliance with platform terms of service")
        report.append("• Do not use this information for harassment or illegal activities")
        report.append("• Respect privacy rights and applicable laws")
        report.append("• Information accuracy is not guaranteed")
        
        return "\n".join(report)
    
    def save_report(self, username: str, format: str = 'txt') -> str:
        """Save the comprehensive report to a file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format.lower() == 'json':
            filename = f"social_search_{username}_{timestamp}.json"
            
            # Convert results to JSON-serializable format
            json_data = {}
            if username in self.results:
                for platform, result in self.results[username].items():
                    json_data[platform] = asdict(result)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
                
        else:  # Default to text format
            filename = f"social_search_{username}_{timestamp}.txt"
            report = self.generate_comprehensive_report(username)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
        
        logger.info(f"Report saved to: {filename}")
        return filename
    
    def search_with_progress(self, username: str, include_variations: bool = True):
        """Search with progress updates"""
        
        print(f"\n🔍 Starting comprehensive search for: {username}")
        print("=" * 60)
        
        total_platforms = len(self.platforms)
        current_platform = 0
        
        results = {}
        
        for platform_name, analyzer in self.platforms.items():
            current_platform += 1
            progress = (current_platform / total_platforms) * 100
            
            print(f"\n[{current_platform}/{total_platforms}] Searching {platform_name.upper()}... ({progress:.0f}%)")
            
            try:
                result = self._search_single_platform(
                    platform_name, analyzer, username, include_variations
                )
                results[platform_name] = result
                
                if result.found:
                    print(f"✅ Found profile on {platform_name}")
                    profile = result.profile_data
                    print(f"   Display: {profile.get('display_name', 'N/A')}")
                    
                    # Show key metrics
                    if platform_name == 'tiktok':
                        followers = profile.get('follower_count', 0)
                        videos = profile.get('video_count', 0)
                        print(f"   Stats: {followers:,} followers, {videos:,} videos")
                    elif platform_name == 'instagram':
                        followers = profile.get('follower_count', 0)
                        posts = profile.get('posts_count', 0)
                        print(f"   Stats: {followers:,} followers, {posts:,} posts")
                    elif platform_name == 'twitter':
                        followers = profile.get('follower_count', 0)
                        tweets = profile.get('tweets_count', 0)
                        print(f"   Stats: {followers:,} followers, {tweets:,} tweets")
                    
                    if result.variations_found:
                        print(f"   Variations: {len(result.variations_found)} similar usernames found")
                else:
                    print(f"❌ No profile found on {platform_name}")
                
            except Exception as e:
                print(f"❌ Error searching {platform_name}: {e}")
                results[platform_name] = SearchResult(
                    platform=platform_name,
                    username=username,
                    found=False,
                    profile_data={},
                    analysis={},
                    variations_found=[],
                    search_timestamp=datetime.now().isoformat(),
                    error_message=str(e)
                )
            
            # Progress delay
            if current_platform < total_platforms:
                print("   Waiting before next platform...")
                time.sleep(3)
        
        self.results[username] = results
        
        print(f"\n✅ Search completed!")
        
        # Summary
        found_count = sum(1 for result in results.values() if result.found)
        total_variations = sum(len(result.variations_found) for result in results.values())
        
        print(f"\n📊 SUMMARY:")
        print(f"   Profiles found: {found_count}/{total_platforms}")
        print(f"   Total variations: {total_variations}")
        
        return results

def main():
    """Main function for multi-platform search"""
    print("🌐 Multi-Platform Social Media Searcher")
    print("=" * 50)
    print()
    
    # Important disclaimer
    print("⚠️  IMPORTANT LEGAL NOTICE:")
    print("This tool is for educational and legitimate research purposes only.")
    print("Always respect platform terms of service and privacy rights.")
    print("Do not use for harassment, stalking, or illegal activities.")
    print()
    
    # Get search parameters
    username = input("Enter username to search across all platforms: ").strip()
    
    if not username:
        print("❌ Please enter a valid username")
        return
    
    include_variations = input("Search for username variations? (y/n): ").lower().strip() == 'y'
    
    # Initialize searcher
    searcher = MultiPlatformSearcher()
    
    # Perform search with progress
    results = searcher.search_with_progress(username, include_variations)
    
    # Generate and display report
    print("\n" + "=" * 80)
    print("GENERATING COMPREHENSIVE REPORT")
    print("=" * 80)
    
    report = searcher.generate_comprehensive_report(username)
    print(report)
    
    # Save report option
    save_report = input("\nSave detailed report to file? (y/n): ").lower().strip()
    if save_report == 'y':
        format_choice = input("Format (txt/json): ").lower().strip()
        if format_choice not in ['txt', 'json']:
            format_choice = 'txt'
        
        filename = searcher.save_report(username, format_choice)
        print(f"📄 Report saved as: {filename}")
    
    print("\n✅ Multi-platform search completed!")

if __name__ == "__main__":
    main()