#!/usr/bin/env python3
"""
Configuration file untuk Social Media Tracker
"""

# Target username yang akan dilacak
TARGET_USERNAME = "gnkihhhhf"

# Platform yang akan di-scan
PLATFORMS = [
    'tiktok',
    'instagram', 
    'twitter',
    'youtube',
    'facebook',
    'reddit'
]

# Settings untuk scraping
SCRAPING_SETTINGS = {
    'use_selenium': True,  # Gunakan Selenium untuk scraping yang lebih efektif
    'headless': True,      # Jalankan browser dalam mode headless
    'delay_between_requests': 2,  # Delay antar request (detik)
    'max_retries': 3,      # Maksimal retry jika gagal
    'timeout': 15,         # Timeout untuk request (detik)
}

# Settings untuk comment tracking
COMMENT_SETTINGS = {
    'max_posts_per_platform': 10,  # Maksimal post yang akan di-scan per platform
    'max_comments_per_post': 50,   # Maksimal komentar per post
    'search_keywords': [TARGET_USERNAME],  # Keywords untuk pencarian
}

# Database settings
DATABASE_SETTINGS = {
    'db_name': f"tracking_{TARGET_USERNAME}.db",
    'backup_enabled': True,
    'backup_interval': 24,  # Backup setiap 24 jam
}

# Output settings
OUTPUT_SETTINGS = {
    'save_json': True,
    'save_html_report': True,
    'save_csv': True,
    'output_directory': 'results',
}

# Rate limiting settings
RATE_LIMITING = {
    'requests_per_minute': 30,
    'requests_per_hour': 1000,
    'delay_on_rate_limit': 60,  # Delay jika terkena rate limit (detik)
}

# User agent settings
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
]

# Proxy settings (opsional)
PROXY_SETTINGS = {
    'enabled': False,
    'proxies': [
        # 'http://proxy1:port',
        # 'http://proxy2:port',
    ],
    'rotation_enabled': False,
}

# Logging settings
LOGGING_SETTINGS = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'file': f"tracker_{TARGET_USERNAME}.log",
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
}

# Notification settings (opsional)
NOTIFICATION_SETTINGS = {
    'enabled': False,
    'email': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': '',
        'password': '',
        'to_email': '',
    },
    'webhook': {
        'enabled': False,
        'url': '',
    },
}

# Advanced settings
ADVANCED_SETTINGS = {
    'parallel_requests': False,  # Jalankan request secara parallel
    'max_workers': 3,           # Maksimal worker untuk parallel requests
    'cache_enabled': True,      # Enable caching untuk menghindari request berulang
    'cache_ttl': 3600,          # Cache TTL dalam detik (1 jam)
}

# Platform-specific settings
PLATFORM_SETTINGS = {
    'tiktok': {
        'enabled': True,
        'max_videos': 20,
        'include_comments': True,
    },
    'instagram': {
        'enabled': True,
        'max_posts': 20,
        'include_stories': False,
        'include_highlights': False,
    },
    'twitter': {
        'enabled': True,
        'max_tweets': 50,
        'include_retweets': True,
        'include_replies': True,
    },
    'youtube': {
        'enabled': True,
        'max_videos': 20,
        'include_comments': True,
        'include_playlists': False,
    },
    'facebook': {
        'enabled': True,
        'max_posts': 20,
        'include_photos': True,
        'include_videos': True,
    },
    'reddit': {
        'enabled': True,
        'max_posts': 30,
        'include_comments': True,
        'subreddits': [],  # Kosong = semua subreddit
    },
}

# Filter settings untuk hasil
FILTER_SETTINGS = {
    'min_follower_count': 0,     # Minimum follower count
    'max_follower_count': 999999999,  # Maximum follower count
    'verified_only': False,      # Hanya akun verified
    'active_only': True,         # Hanya akun yang aktif (posting dalam 30 hari terakhir)
    'exclude_private': True,     # Exclude akun private
}

# Export settings
EXPORT_SETTINGS = {
    'formats': ['json', 'html', 'csv'],  # Format export
    'include_raw_data': True,    # Include raw data dalam export
    'compress_output': False,    # Kompres output files
    'encrypt_sensitive': False,  # Encrypt data sensitif
}

# Monitoring settings
MONITORING_SETTINGS = {
    'enabled': True,
    'check_interval': 3600,      # Check interval dalam detik (1 jam)
    'alert_on_new_activity': True,
    'alert_on_profile_changes': True,
    'alert_on_new_comments': True,
}

# Security settings
SECURITY_SETTINGS = {
    'encrypt_database': False,
    'password_protect': False,
    'password': '',  # Password untuk proteksi
    'max_login_attempts': 3,
    'session_timeout': 3600,  # Session timeout dalam detik
}

# Debug settings
DEBUG_SETTINGS = {
    'verbose_logging': False,
    'save_screenshots': False,
    'save_html_pages': False,
    'debug_mode': False,
}

# API settings (untuk future use)
API_SETTINGS = {
    'tiktok_api': {
        'enabled': False,
        'api_key': '',
        'rate_limit': 100,  # requests per hour
    },
    'instagram_api': {
        'enabled': False,
        'access_token': '',
        'rate_limit': 200,  # requests per hour
    },
    'twitter_api': {
        'enabled': False,
        'bearer_token': '',
        'rate_limit': 300,  # requests per 15 minutes
    },
}

def get_config():
    """Return configuration dictionary"""
    return {
        'target_username': TARGET_USERNAME,
        'platforms': PLATFORMS,
        'scraping': SCRAPING_SETTINGS,
        'comments': COMMENT_SETTINGS,
        'database': DATABASE_SETTINGS,
        'output': OUTPUT_SETTINGS,
        'rate_limiting': RATE_LIMITING,
        'user_agents': USER_AGENTS,
        'proxy': PROXY_SETTINGS,
        'logging': LOGGING_SETTINGS,
        'notification': NOTIFICATION_SETTINGS,
        'advanced': ADVANCED_SETTINGS,
        'platforms_config': PLATFORM_SETTINGS,
        'filters': FILTER_SETTINGS,
        'export': EXPORT_SETTINGS,
        'monitoring': MONITORING_SETTINGS,
        'security': SECURITY_SETTINGS,
        'debug': DEBUG_SETTINGS,
        'api': API_SETTINGS,
    }

def update_username(new_username):
    """Update target username"""
    global TARGET_USERNAME
    TARGET_USERNAME = new_username
    COMMENT_SETTINGS['search_keywords'] = [new_username]
    DATABASE_SETTINGS['db_name'] = f"tracking_{new_username}.db"
    LOGGING_SETTINGS['file'] = f"tracker_{new_username}.log"

if __name__ == "__main__":
    # Test configuration
    config = get_config()
    print("Configuration loaded successfully!")
    print(f"Target username: {config['target_username']}")
    print(f"Platforms: {', '.join(config['platforms'])}")
    print(f"Scraping enabled: {config['scraping']['use_selenium']}")
    print(f"Comment tracking enabled: {config['comments']['max_posts_per_platform'] > 0}")