#!/usr/bin/env python3
"""
Quick Scan - Jalankan semua tracking dalam satu command
"""

import sys
import os
from datetime import datetime

def main():
    print("🔍 QUICK SOCIAL MEDIA SCAN")
    print("=" * 40)
    
    # Username target
    username = "gnkihhhhf"
    print(f"Target: {username}")
    print()
    
    # 1. Basic Social Media Tracking
    print("1️⃣ Running Basic Social Media Tracking...")
    try:
        from social_media_tracker import SocialMediaTracker
        tracker = SocialMediaTracker(username)
        results = tracker.run_full_scan()
        tracker.print_summary()
        print("✅ Basic tracking completed")
    except Exception as e:
        print(f"❌ Basic tracking failed: {e}")
    
    print()
    
    # 2. Comment Tracking
    print("2️⃣ Running Comment Tracking...")
    try:
        from comment_tracker import CommentTracker
        comment_tracker = CommentTracker(username)
        comment_results = comment_tracker.run_full_comment_search()
        
        print(f"💬 Total comments found: {comment_results['total_comments']}")
        for platform, data in comment_results['platforms'].items():
            print(f"   📱 {platform.upper()}: {data['count']} comments")
        
        print("✅ Comment tracking completed")
    except Exception as e:
        print(f"❌ Comment tracking failed: {e}")
    
    print()
    print("🎉 Quick scan completed!")
    print("📄 Check the generated files for detailed results")

if __name__ == "__main__":
    main()