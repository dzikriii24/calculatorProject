#!/usr/bin/env python3
"""
Setup Script for Social Media Tracking Tools
============================================

This script helps set up the social media tracking tools and
verifies that all dependencies are properly installed.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Check if requirements.txt exists
        if not os.path.exists('requirements.txt'):
            print("❌ requirements.txt not found")
            return False
        
        # Install dependencies
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def verify_imports():
    """Verify that all modules can be imported"""
    print("\n🔍 Verifying module imports...")
    
    modules_to_test = [
        ('requests', 'HTTP requests'),
        ('bs4', 'BeautifulSoup HTML parsing'),
        ('cloudscraper', 'Anti-bot protection'),
        ('lxml', 'XML/HTML processing')
    ]
    
    all_good = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError as e:
            print(f"❌ {module_name} - {description} - Error: {e}")
            all_good = False
    
    return all_good

def test_analyzers():
    """Test that our analyzer modules can be imported"""
    print("\n🧪 Testing analyzer modules...")
    
    analyzers = [
        ('social_media_tracker', 'Main tracker'),
        ('tiktok_analyzer', 'TikTok analyzer'),
        ('instagram_analyzer', 'Instagram analyzer'),
        ('twitter_analyzer', 'Twitter analyzer'),
        ('multi_platform_searcher', 'Multi-platform searcher')
    ]
    
    all_good = True
    
    for module_name, description in analyzers:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError as e:
            print(f"❌ {module_name} - {description} - Error: {e}")
            all_good = False
    
    return all_good

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['logs', 'reports', 'data']
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"✅ Created/verified directory: {directory}")
        except Exception as e:
            print(f"❌ Failed to create directory {directory}: {e}")

def show_usage_examples():
    """Show usage examples"""
    print("\n💡 USAGE EXAMPLES:")
    print("=" * 30)
    print()
    
    print("1. Run the demo:")
    print("   python demo_search.py")
    print()
    
    print("2. Multi-platform search:")
    print("   python multi_platform_searcher.py")
    print()
    
    print("3. Individual platform analysis:")
    print("   python tiktok_analyzer.py")
    print("   python instagram_analyzer.py")
    print("   python twitter_analyzer.py")
    print()
    
    print("4. Programmatic usage:")
    print("   from multi_platform_searcher import MultiPlatformSearcher")
    print("   searcher = MultiPlatformSearcher()")
    print("   results = searcher.search_all_platforms('username')")
    print()

def main():
    """Main setup function"""
    print("🔧 SOCIAL MEDIA TRACKING TOOLS SETUP")
    print("=" * 45)
    print()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        return False
    
    # Verify imports
    if not verify_imports():
        print("\n❌ Setup failed during import verification")
        print("Try running: pip install -r requirements.txt")
        return False
    
    # Test analyzers
    if not test_analyzers():
        print("\n❌ Setup failed during analyzer testing")
        print("Make sure all Python files are in the same directory")
        return False
    
    # Create directories
    create_directories()
    
    print("\n✅ SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 35)
    
    # Show usage examples
    show_usage_examples()
    
    # Important reminders
    print("⚠️  IMPORTANT REMINDERS:")
    print("- Use these tools responsibly and ethically")
    print("- Respect platform terms of service")
    print("- Do not use for harassment or illegal activities")
    print("- Always verify information through official channels")
    print()
    
    print("🚀 You're ready to start using the social media tracking tools!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)