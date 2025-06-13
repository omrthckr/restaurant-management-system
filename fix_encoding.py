#!/usr/bin/env python3
"""
Script to fix encoding issues in HTML files
Run this script to convert all HTML files to proper UTF-8 encoding
"""

import os
import shutil
from datetime import datetime

def fix_html_encoding():
    """Fix encoding for all HTML files in the current directory"""
    
    html_files = [
        'admin_dashboard.html',
        'kitchen_system.html', 
        'restaurant_menu_html.html'
    ]
    
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1', 'cp1254']
    
    print("🔧 Starting to fix HTML file encodings...")
    print("=" * 50)
    
    for filename in html_files:
        if not os.path.exists(filename):
            print(f"⚠️  {filename} not found, skipping...")
            continue
            
        print(f"🔍 Processing {filename}...")
        
        # Create backup
        backup_name = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            shutil.copy2(filename, backup_name)
            print(f"📁 Backup created: {backup_name}")
        except Exception as e:
            print(f"❌ Could not create backup: {e}")
            continue
        
        # Try to read with different encodings
        content = None
        successful_encoding = None
        
        for encoding in encodings_to_try:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    content = f.read()
                    successful_encoding = encoding
                    print(f"✅ Successfully read with {encoding}")
                    break
            except UnicodeDecodeError as e:
                print(f"❌ Failed with {encoding}: {str(e)[:100]}...")
                continue
            except Exception as e:
                print(f"❌ Error with {encoding}: {str(e)}")
                continue
        
        # If all normal encodings fail, try binary read with replacement
        if content is None:
            try:
                with open(filename, 'rb') as f:
                    raw_content = f.read()
                    content = raw_content.decode('utf-8', errors='replace')
                    successful_encoding = "binary->utf-8 with replacement"
                    print(f"⚠️  Used binary read with character replacement")
            except Exception as e:
                print(f"❌ Complete failure reading {filename}: {e}")
                continue
        
        # Write back as UTF-8
        if content is not None:
            try:
                with open(filename, 'w', encoding='utf-8', newline='') as f:
                    f.write(content)
                print(f"✅ Successfully converted {filename} to UTF-8")
                print(f"   Original encoding: {successful_encoding}")
                print(f"   File size: {len(content)} characters")
            except Exception as e:
                print(f"❌ Error writing {filename}: {e}")
                # Restore backup if write failed
                try:
                    shutil.copy2(backup_name, filename)
                    print(f"🔄 Restored from backup")
                except:
                    pass
        
        print("-" * 30)
    
    print("🎉 Encoding fix process completed!")
    print("\n📝 Summary:")
    print("- Backup files created with timestamp")
    print("- All HTML files should now be UTF-8 encoded") 
    print("- You can delete backup files if everything works correctly")
    print("\n🚀 Try running your Flask app again: python app.py")

def clean_backups():
    """Remove all backup files"""
    backup_files = [f for f in os.listdir('.') if f.endswith('.backup_' + datetime.now().strftime('%Y%m%d'))]
    if backup_files:
        print(f"🗑️  Found {len(backup_files)} backup files from today")
        response = input("Delete them? (y/N): ").lower().strip()
        if response == 'y':
            for backup in backup_files:
                try:
                    os.remove(backup)
                    print(f"✅ Deleted {backup}")
                except Exception as e:
                    print(f"❌ Could not delete {backup}: {e}")
        else:
            print("Backup files kept.")
    else:
        print("No backup files found from today.")

if __name__ == "__main__":
    print("🍽️ Restaurant System - HTML Encoding Fixer")
    print("=" * 50)
    
    choice = input("Choose an option:\n1. Fix HTML encodings\n2. Clean backup files\n3. Both\nEnter choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        fix_html_encoding()
    
    if choice in ['2', '3']:
        print("\n" + "=" * 50)
        clean_backups()
    
    if choice not in ['1', '2', '3']:
        print("Invalid choice. Run the script again.")