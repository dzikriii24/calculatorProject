#!/usr/bin/env python3
"""
Main Runner untuk Social Media Tracker
Menjalankan semua fitur tracking dalam satu program
"""

import os
import sys
import time
from datetime import datetime
import json

def print_banner():
    """Print banner program"""
    print("=" * 60)
    print("🔍 SOCIAL MEDIA ACCOUNT TRACKER")
    print("=" * 60)
    print("Program untuk melacak akun sosial media dan komentar")
    print("⚠️  Hanya mengumpulkan data publik yang legal")
    print("=" * 60)

def print_menu():
    """Print menu pilihan"""
    print("\n📋 PILIHAN MENU:")
    print("1. Basic Social Media Tracking")
    print("2. Advanced Tracking (dengan Selenium)")
    print("3. Comment Tracking")
    print("4. Full Scan (Semua fitur)")
    print("5. Lihat hasil sebelumnya")
    print("6. Keluar")
    print("-" * 40)

def run_basic_tracking(username):
    """Jalankan basic tracking"""
    print(f"\n🔍 Menjalankan Basic Tracking untuk: {username}")
    print("Loading...")
    
    try:
        from social_media_tracker import SocialMediaTracker
        
        tracker = SocialMediaTracker(username)
        results = tracker.run_full_scan()
        tracker.print_summary()
        
        filename = tracker.save_results()
        print(f"\n📄 Hasil disimpan ke: {filename}")
        
        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def run_advanced_tracking(username):
    """Jalankan advanced tracking"""
    print(f"\n🚀 Menjalankan Advanced Tracking untuk: {username}")
    print("Loading...")
    
    try:
        from advanced_tracker import AdvancedSocialMediaTracker
        
        tracker = AdvancedSocialMediaTracker(username, use_selenium=True)
        results = tracker.run_advanced_scan()
        tracker.print_advanced_summary()
        
        filename = tracker.save_results()
        print(f"\n📄 Hasil disimpan ke: {filename}")
        
        tracker.cleanup()
        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def run_comment_tracking(username):
    """Jalankan comment tracking"""
    print(f"\n💬 Menjalankan Comment Tracking untuk: {username}")
    print("Loading...")
    
    try:
        from comment_tracker import CommentTracker
        
        tracker = CommentTracker(username)
        results = tracker.run_full_comment_search()
        
        print(f"\n{'='*50}")
        print(f"COMMENT SEARCH RESULTS FOR: {username.upper()}")
        print(f"{'='*50}")
        print(f"Total comments found: {results['total_comments']}")
        print()
        
        for platform, data in results['platforms'].items():
            print(f"📱 {platform.upper()}: {data['count']} comments")
            if data['count'] > 0:
                for i, comment in enumerate(data['comments'][:3]):
                    print(f"   {i+1}. {comment['content'][:100]}...")
                if data['count'] > 3:
                    print(f"   ... and {data['count'] - 3} more comments")
            print()
        
        report_filename = tracker.save_comment_report()
        print(f"📄 Comment report disimpan ke: {report_filename}")
        
        return results
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def run_full_scan(username):
    """Jalankan full scan (semua fitur)"""
    print(f"\n🔥 Menjalankan Full Scan untuk: {username}")
    print("Ini akan memakan waktu beberapa menit...")
    print("Loading...")
    
    all_results = {
        'username': username,
        'timestamp': datetime.now().isoformat(),
        'basic_tracking': None,
        'advanced_tracking': None,
        'comment_tracking': None
    }
    
    # 1. Basic Tracking
    print("\n1️⃣ Basic Social Media Tracking...")
    basic_results = run_basic_tracking(username)
    all_results['basic_tracking'] = basic_results
    
    # 2. Advanced Tracking
    print("\n2️⃣ Advanced Tracking...")
    advanced_results = run_advanced_tracking(username)
    all_results['advanced_tracking'] = advanced_results
    
    # 3. Comment Tracking
    print("\n3️⃣ Comment Tracking...")
    comment_results = run_comment_tracking(username)
    all_results['comment_tracking'] = comment_results
    
    # Simpan hasil lengkap
    filename = f"full_scan_results_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Full scan results disimpan ke: {filename}")
    
    return all_results

def view_previous_results():
    """Lihat hasil sebelumnya"""
    print("\n📁 Mencari file hasil sebelumnya...")
    
    # Cari file JSON hasil
    json_files = [f for f in os.listdir('.') if f.endswith('.json') and 'results' in f]
    
    if not json_files:
        print("❌ Tidak ada file hasil sebelumnya ditemukan")
        return
    
    print(f"\n📋 Ditemukan {len(json_files)} file hasil:")
    for i, file in enumerate(json_files, 1):
        print(f"{i}. {file}")
    
    try:
        choice = int(input("\nPilih file (nomor): ")) - 1
        if 0 <= choice < len(json_files):
            filename = json_files[choice]
            print(f"\n📖 Membaca file: {filename}")
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n{'='*50}")
            print(f"RESULTS: {data.get('username', 'Unknown').upper()}")
            print(f"{'='*50}")
            print(f"Timestamp: {data.get('timestamp', 'Unknown')}")
            
            if 'platforms' in data:
                print(f"\n📱 PLATFORMS:")
                for platform, info in data['platforms'].items():
                    status = info.get('status', 'unknown')
                    if status == 'found':
                        print(f"   ✅ {platform.upper()}: Found")
                    elif status == 'not_found':
                        print(f"   ❌ {platform.upper()}: Not Found")
                    else:
                        print(f"   ⚠️  {platform.upper()}: Error")
            
            if 'total_comments' in data:
                print(f"\n💬 COMMENTS: {data['total_comments']} found")
            
        else:
            print("❌ Pilihan tidak valid")
    except (ValueError, IndexError):
        print("❌ Input tidak valid")

def main():
    """Main function"""
    print_banner()
    
    # Username yang akan dilacak
    username = "gnkihhhhf"
    
    print(f"🎯 Target Username: {username}")
    print("⚠️  Pastikan Anda memiliki izin untuk melacak akun ini")
    
    while True:
        print_menu()
        
        try:
            choice = input("Pilih menu (1-6): ").strip()
            
            if choice == '1':
                run_basic_tracking(username)
            elif choice == '2':
                run_advanced_tracking(username)
            elif choice == '3':
                run_comment_tracking(username)
            elif choice == '4':
                run_full_scan(username)
            elif choice == '5':
                view_previous_results()
            elif choice == '6':
                print("\n👋 Terima kasih! Program selesai.")
                break
            else:
                print("❌ Pilihan tidak valid. Silakan pilih 1-6.")
            
            input("\n⏸️  Tekan Enter untuk melanjutkan...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Program dihentikan oleh user.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("⏸️  Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()