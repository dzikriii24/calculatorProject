#!/usr/bin/env python3
"""
Generate comprehensive report dari hasil tracking
"""

import json
import os
from datetime import datetime
from typing import Dict, List

def load_tracking_results() -> Dict:
    """Load hasil tracking dari file JSON"""
    json_files = [f for f in os.listdir('.') if f.endswith('.json') and 'tracking_results' in f]
    
    if not json_files:
        print("❌ Tidak ada file hasil tracking ditemukan")
        return {}
    
    # Ambil file terbaru
    latest_file = max(json_files, key=os.path.getctime)
    print(f"📄 Loading results from: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_comprehensive_report(data: Dict) -> str:
    """Generate laporan lengkap dalam format HTML"""
    
    username = data.get('username', 'Unknown')
    timestamp = data.get('timestamp', 'Unknown')
    platforms = data.get('platforms', {})
    
    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Laporan Lengkap - {username}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.5em;
                font-weight: 300;
            }}
            .header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
                font-size: 1.1em;
            }}
            .summary {{
                padding: 30px;
                background: #f8f9fa;
                border-bottom: 1px solid #e9ecef;
            }}
            .summary-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}
            .summary-card {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .summary-card h3 {{
                margin: 0 0 10px 0;
                color: #495057;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .summary-card .number {{
                font-size: 2em;
                font-weight: bold;
                color: #007bff;
            }}
            .platforms {{
                padding: 30px;
            }}
            .platform {{
                margin: 20px 0;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                overflow: hidden;
            }}
            .platform-header {{
                padding: 20px;
                background: #f8f9fa;
                border-bottom: 1px solid #e9ecef;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }}
            .platform-name {{
                font-size: 1.3em;
                font-weight: 600;
                color: #495057;
            }}
            .platform-status {{
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: 500;
            }}
            .status-found {{
                background: #d4edda;
                color: #155724;
            }}
            .status-not-found {{
                background: #f8d7da;
                color: #721c24;
            }}
            .status-error {{
                background: #fff3cd;
                color: #856404;
            }}
            .platform-content {{
                padding: 20px;
            }}
            .profile-data {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
            }}
            .data-item {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 6px;
                border-left: 4px solid #007bff;
            }}
            .data-label {{
                font-weight: 600;
                color: #495057;
                margin-bottom: 5px;
                font-size: 0.9em;
            }}
            .data-value {{
                color: #212529;
                font-size: 1.1em;
            }}
            .footer {{
                padding: 20px 30px;
                background: #f8f9fa;
                border-top: 1px solid #e9ecef;
                text-align: center;
                color: #6c757d;
                font-size: 0.9em;
            }}
            .disclaimer {{
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 6px;
                padding: 15px;
                margin: 20px 0;
                color: #856404;
            }}
            .disclaimer h4 {{
                margin: 0 0 10px 0;
                color: #856404;
            }}
            .disclaimer ul {{
                margin: 0;
                padding-left: 20px;
            }}
            .disclaimer li {{
                margin: 5px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 Laporan Pelacakan Sosial Media</h1>
                <p>Username: <strong>{username}</strong></p>
                <p>Generated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <h2>📊 Ringkasan Hasil</h2>
                <div class="summary-grid">
                    <div class="summary-card">
                        <h3>Platform Ditemukan</h3>
                        <div class="number">{sum(1 for p in platforms.values() if p.get('status') == 'found')}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Platform Tidak Ditemukan</h3>
                        <div class="number">{sum(1 for p in platforms.values() if p.get('status') == 'not_found')}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Platform Error</h3>
                        <div class="number">{sum(1 for p in platforms.values() if p.get('status') == 'error')}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Total Platform</h3>
                        <div class="number">{len(platforms)}</div>
                    </div>
                </div>
            </div>
            
            <div class="platforms">
                <h2>📱 Detail Platform</h2>
    """
    
    # Tampilkan setiap platform
    for platform_name, platform_data in platforms.items():
        status = platform_data.get('status', 'unknown')
        status_class = f"status-{status.replace('_', '-')}"
        status_text = status.replace('_', ' ').title()
        
        html += f"""
                <div class="platform">
                    <div class="platform-header">
                        <div class="platform-name">📱 {platform_name.upper()}</div>
                        <div class="platform-status {status_class}">{status_text}</div>
                    </div>
                    <div class="platform-content">
        """
        
        if status == 'found':
            url = platform_data.get('url', 'N/A')
            profile_data = platform_data.get('profile_data', {})
            
            html += f"""
                        <p><strong>URL:</strong> <a href="{url}" target="_blank">{url}</a></p>
                        <p><strong>Last Checked:</strong> {platform_data.get('last_checked', 'N/A')}</p>
            """
            
            if profile_data:
                html += """
                        <h4>📋 Informasi Profil:</h4>
                        <div class="profile-data">
                """
                
                for key, value in profile_data.items():
                    if value:  # Hanya tampilkan jika ada nilai
                        label = key.replace('_', ' ').title()
                        html += f"""
                            <div class="data-item">
                                <div class="data-label">{label}</div>
                                <div class="data-value">{value}</div>
                            </div>
                        """
                
                html += "</div>"
            else:
                html += "<p><em>Informasi profil tidak tersedia</em></p>"
                
        elif status == 'not_found':
            error = platform_data.get('error', 'Account not found')
            html += f"<p><strong>Status:</strong> Account tidak ditemukan</p>"
            html += f"<p><strong>Error:</strong> {error}</p>"
            
        else:  # error
            error = platform_data.get('error', 'Unknown error')
            html += f"<p><strong>Status:</strong> Error terjadi</p>"
            html += f"<p><strong>Error:</strong> {error}</p>"
        
        html += """
                    </div>
                </div>
        """
    
    # Disclaimer
    html += """
            </div>
            
            <div class="disclaimer">
                <h4>⚠️ Disclaimer Penting</h4>
                <ul>
                    <li>Program ini hanya mengumpulkan informasi yang tersedia secara publik</li>
                    <li>Selalu patuhi Terms of Service platform sosial media</li>
                    <li>Hormati privasi pengguna lain</li>
                    <li>Gunakan dengan bertanggung jawab dan legal</li>
                    <li>Jangan gunakan untuk tujuan yang merugikan atau mengganggu</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>Generated by Social Media Tracker | {}</p>
                <p>⚠️ Gunakan dengan bijak dan legal!</p>
            </div>
        </div>
    </body>
    </html>
    """.format(datetime.now().strftime('%Y'))
    
    return html

def main():
    print("📊 Generating Comprehensive Report")
    print("=" * 40)
    
    # Load data
    data = load_tracking_results()
    if not data:
        return
    
    # Generate report
    html_content = generate_comprehensive_report(data)
    
    # Save report
    username = data.get('username', 'unknown')
    filename = f"comprehensive_report_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Report generated: {filename}")
    print(f"📄 Open the file in your browser to view the report")

if __name__ == "__main__":
    main()