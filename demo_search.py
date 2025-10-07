#!/usr/bin/env python3
"""
Demo Script for Social Media Tracking Tools
===========================================

This script demonstrates how to use the social media tracking tools
to search for the username "gnkihhhhf" across multiple platforms.

IMPORTANT: This is for educational purposes only.
"""

import sys
import os
from datetime import datetime

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from multi_platform_searcher import MultiPlatformSearcher
    from tiktok_analyzer import TikTokAnalyzer
    from instagram_analyzer import InstagramAnalyzer
    from twitter_analyzer import TwitterAnalyzer
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all required dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def demo_single_platform_search():
    """Demonstrate searching on individual platforms"""
    
    username = "gnkihhhhf"
    
    print("🎯 SINGLE PLATFORM DEMO")
    print("=" * 40)
    print(f"Searching for: {username}")
    print()
    
    # TikTok Demo
    print("🎵 TikTok Analysis:")
    print("-" * 20)
    try:
        tiktok_analyzer = TikTokAnalyzer()
        tiktok_data = tiktok_analyzer.extract_profile_data(username)
        
        if tiktok_data and tiktok_data.get('username'):
            print(f"✅ Found TikTok profile: @{tiktok_data.get('username')}")
            print(f"   Display Name: {tiktok_data.get('display_name', 'N/A')}")
            print(f"   Followers: {tiktok_data.get('follower_count', 0):,}")
            print(f"   Videos: {tiktok_data.get('video_count', 0):,}")
        else:
            print("❌ TikTok profile not found or inaccessible")
    except Exception as e:
        print(f"❌ TikTok search error: {e}")
    
    print()
    
    # Instagram Demo
    print("📸 Instagram Analysis:")
    print("-" * 22)
    try:
        instagram_analyzer = InstagramAnalyzer()
        instagram_data = instagram_analyzer.extract_profile_data(username)
        
        if instagram_data and instagram_data.get('username'):
            print(f"✅ Found Instagram profile: @{instagram_data.get('username')}")
            print(f"   Display Name: {instagram_data.get('display_name', 'N/A')}")
            print(f"   Followers: {instagram_data.get('follower_count', 0):,}")
            print(f"   Posts: {instagram_data.get('posts_count', 0):,}")
            print(f"   Private: {'Yes' if instagram_data.get('private') else 'No'}")
        else:
            print("❌ Instagram profile not found or inaccessible")
    except Exception as e:
        print(f"❌ Instagram search error: {e}")
    
    print()
    
    # Twitter Demo
    print("🐦 Twitter Analysis:")
    print("-" * 19)
    try:
        twitter_analyzer = TwitterAnalyzer()
        twitter_data = twitter_analyzer.extract_profile_data(username)
        
        if twitter_data and twitter_data.get('username'):
            print(f"✅ Found Twitter profile: @{twitter_data.get('username')}")
            print(f"   Display Name: {twitter_data.get('display_name', 'N/A')}")
            print(f"   Followers: {twitter_data.get('follower_count', 0):,}")
            print(f"   Tweets: {twitter_data.get('tweets_count', 0):,}")
        else:
            print("❌ Twitter profile not found or inaccessible")
    except Exception as e:
        print(f"❌ Twitter search error: {e}")

def demo_multi_platform_search():
    """Demonstrate comprehensive multi-platform search"""
    
    username = "gnkihhhhf"
    
    print("\n\n🌐 MULTI-PLATFORM COMPREHENSIVE SEARCH")
    print("=" * 50)
    print(f"Target Username: {username}")
    print()
    
    try:
        searcher = MultiPlatformSearcher()
        
        # Perform comprehensive search
        print("🔍 Starting comprehensive search...")
        results = searcher.search_with_progress(username, include_variations=True)
        
        # Generate and display report
        print("\n📄 Generating comprehensive report...")
        report = searcher.generate_comprehensive_report(username)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"demo_report_{username}_{timestamp}.txt"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Report saved as: {report_filename}")
        
        # Display summary
        found_platforms = [name for name, result in results.items() if result.found]
        total_variations = sum(len(result.variations_found) for result in results.values())
        
        print(f"\n📊 SEARCH SUMMARY:")
        print(f"   Profiles found: {len(found_platforms)}/{len(results)} platforms")
        print(f"   Platforms with matches: {', '.join(found_platforms) if found_platforms else 'None'}")
        print(f"   Total variations found: {total_variations}")
        
        return report_filename
        
    except Exception as e:
        print(f"❌ Multi-platform search error: {e}")
        return None

def demo_username_variations():
    """Demonstrate username variation search"""
    
    username = "gnkihhhhf"
    
    print("\n\n🔄 USERNAME VARIATIONS DEMO")
    print("=" * 35)
    print(f"Searching variations of: {username}")
    print()
    
    # TikTok variations
    print("🎵 TikTok Variations:")
    try:
        tiktok_analyzer = TikTokAnalyzer()
        variations = tiktok_analyzer.search_username_variations(username)
        
        if variations:
            print(f"   Found {len(variations)} variations:")
            for i, variation in enumerate(variations[:3], 1):  # Show top 3
                var_username = variation.get('username', 'unknown')
                var_followers = variation.get('follower_count', 0)
                print(f"   {i}. @{var_username} ({var_followers:,} followers)")
        else:
            print("   No variations found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()

def main():
    """Main demo function"""
    
    print("🔍 SOCIAL MEDIA TRACKING TOOLS DEMO")
    print("=" * 45)
    print()
    
    # Important disclaimer
    print("⚠️  IMPORTANT NOTICE:")
    print("This demo is for educational purposes only.")
    print("Always respect platform terms of service and privacy rights.")
    print("Do not use for harassment or illegal activities.")
    print()
    
    # Run demos
    try:
        # Single platform demo
        demo_single_platform_search()
        
        # Multi-platform demo
        report_file = demo_multi_platform_search()
        
        # Variations demo
        demo_username_variations()
        
        print("\n✅ Demo completed successfully!")
        
        if report_file:
            print(f"\n📄 Detailed report saved as: {report_file}")
            print("You can open this file to see the full analysis.")
        
        print("\n💡 Next Steps:")
        print("1. Review the generated report")
        print("2. Try searching for other usernames")
        print("3. Explore individual platform analyzers")
        print("4. Always use responsibly and ethically")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()