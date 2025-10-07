# 🔍 Social Media Profile Tracker

A comprehensive tool for tracking and analyzing social media profiles across multiple platforms. This tool helps you monitor public information from TikTok, Instagram, Twitter/X, YouTube, and other social media platforms in a legal and ethical manner.

## ⚠️ Important Legal Notice

**This tool is for educational and legitimate research purposes only.**

- ✅ Use for cybersecurity research and digital forensics
- ✅ Use for brand monitoring and reputation management  
- ✅ Use for academic research with proper permissions
- ❌ **DO NOT** use for harassment, stalking, or illegal activities
- ❌ **DO NOT** violate platform terms of service
- ❌ **DO NOT** collect private or sensitive information without consent

Always respect privacy rights and applicable laws in your jurisdiction.

## 🚀 Features

### Multi-Platform Support
- **TikTok**: Profile analysis, follower metrics, content patterns
- **Instagram**: Account type detection, engagement analysis, authenticity scoring
- **Twitter/X**: Influence metrics, activity patterns, verification status
- **YouTube**: Channel information and subscriber data
- **Cross-Platform**: Comprehensive analysis across all platforms

### Advanced Analysis
- 📊 **Profile Analytics**: Follower counts, engagement ratios, content metrics
- 🔍 **Username Variations**: Automatic discovery of similar usernames
- 🎯 **Authenticity Scoring**: Assessment of profile completeness and legitimacy
- 📈 **Influence Metrics**: Categorization of account types and reach
- 🔗 **Cross-Platform Correlation**: Compare presence across multiple platforms

### Ethical Features
- ⏱️ **Rate Limiting**: Respects platform rate limits automatically
- 🔒 **Privacy Focused**: Only collects publicly available information
- 📝 **Comprehensive Logging**: Full audit trail of all activities
- 📄 **Detailed Reports**: Professional reports with disclaimers

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `cloudscraper` - Anti-bot protection handling
- `lxml` - XML/HTML processing
- `pandas` - Data analysis (optional)
- `colorama` - Colored terminal output

## 🎯 Usage

### Quick Start
```bash
# Run the main multi-platform searcher
python multi_platform_searcher.py

# Run individual platform analyzers
python tiktok_analyzer.py
python instagram_analyzer.py
python twitter_analyzer.py
```

### Example Usage

#### Multi-Platform Search
```python
from multi_platform_searcher import MultiPlatformSearcher

searcher = MultiPlatformSearcher()
results = searcher.search_all_platforms("username", include_variations=True)
report = searcher.generate_comprehensive_report("username")
print(report)
```

#### TikTok Analysis
```python
from tiktok_analyzer import TikTokAnalyzer

analyzer = TikTokAnalyzer()
profile_data = analyzer.extract_profile_data("username")
analysis = analyzer.analyze_profile_activity("username")
```

#### Instagram Analysis
```python
from instagram_analyzer import InstagramAnalyzer

analyzer = InstagramAnalyzer()
profile_data = analyzer.extract_profile_data("username")
patterns = analyzer.analyze_profile_patterns("username")
```

## 📊 Sample Output

### Multi-Platform Report
```
================================================================================
COMPREHENSIVE SOCIAL MEDIA SEARCH REPORT
================================================================================
Target Username: example_user
Search Date: 2024-01-15 14:30:22
Platforms Searched: tiktok, instagram, twitter

📊 EXECUTIVE SUMMARY
----------------------------------------
✅ Profiles Found: 2/3 platforms
🔍 Total Variations Found: 5
🎯 Primary Matches: tiktok, instagram

🔍 TIKTOK ANALYSIS
--------------------------------------------------
✅ Profile Found: @example_user
📝 Display Name: Example User
👥 Followers: 15,234
➡️ Following: 892
🎬 Videos: 127
✅ Verified: No
🔒 Private: No
📄 Bio: Content creator sharing daily life...

🔍 INSTAGRAM ANALYSIS
--------------------------------------------------
✅ Profile Found: @example_user
📝 Display Name: Example User
👥 Followers: 8,567
➡️ Following: 1,234
📸 Posts: 89
💼 Business: No
✅ Verified: No
🔒 Private: Yes
```

## 🛠️ Configuration

### Rate Limiting
Each analyzer includes built-in rate limiting to respect platform guidelines:
- TikTok: 3 seconds between requests
- Instagram: 5 seconds between requests  
- Twitter: 3 seconds between requests

### Customization
You can modify the analyzers to:
- Adjust rate limiting delays
- Add new platforms
- Customize analysis metrics
- Modify report formats

## 📁 File Structure

```
social-media-tracker/
├── social_media_tracker.py      # Main tracker class
├── multi_platform_searcher.py   # Comprehensive multi-platform tool
├── tiktok_analyzer.py           # TikTok-specific analyzer
├── instagram_analyzer.py        # Instagram-specific analyzer  
├── twitter_analyzer.py          # Twitter/X-specific analyzer
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── logs/                        # Generated log files
    └── social_media_tracker.log
```

## 🔧 Advanced Features

### Username Variation Search
The tool automatically searches for common username variations:
- Lowercase/uppercase variations
- Underscore prefixes/suffixes
- Number suffixes (1, 2, 3)
- Common prefixes (real, official, the)
- Platform-specific variations

### Cross-Platform Analysis
When profiles are found on multiple platforms, the tool provides:
- Follower count comparisons
- Display name consistency analysis
- Verification status across platforms
- Content strategy differences

### Authenticity Scoring
Each profile receives an authenticity score based on:
- Profile completeness (bio, display name, profile picture)
- External links and verification status
- Follower/following ratios
- Content patterns and activity levels

## ⚖️ Legal Compliance

### Terms of Service Compliance
This tool is designed to comply with major platform terms of service:
- Uses only publicly available information
- Implements proper rate limiting
- Does not circumvent platform security measures
- Respects robots.txt and API guidelines

### Privacy Protection
- No collection of private or sensitive information
- No storage of personal data without consent
- Clear disclaimers in all reports
- Audit trail of all activities

### Responsible Use Guidelines
1. **Always verify** information through official channels
2. **Respect privacy** and do not share personal information
3. **Follow local laws** regarding data collection and privacy
4. **Use for legitimate purposes** only
5. **Report abuse** if you discover illegal activities

## 🐛 Troubleshooting

### Common Issues

#### "Profile not found" errors
- Check username spelling and format
- Some profiles may be private or restricted
- Platform may have anti-scraping measures active
- Try again later with proper rate limiting

#### Rate limiting errors
- Increase delay between requests
- Use VPN if IP is temporarily blocked
- Respect platform guidelines and limits

#### Installation issues
```bash
# Update pip and try again
pip install --upgrade pip
pip install -r requirements.txt

# For parsing issues, install lxml separately
pip install lxml
```

### Debug Mode
Enable detailed logging by setting the log level:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

Contributions are welcome! Please ensure all contributions:
1. Maintain ethical standards and legal compliance
2. Include proper error handling and rate limiting
3. Follow existing code style and documentation standards
4. Include tests for new features

## 📄 License

This project is provided for educational purposes. Users are responsible for ensuring their use complies with applicable laws and platform terms of service.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review platform terms of service for any changes
3. Ensure you're using the tool for legitimate purposes
4. Consider the ethical implications of your research

---

**Remember**: With great power comes great responsibility. Use this tool ethically and legally.