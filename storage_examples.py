#!/usr/bin/env python3
"""Storage examples for CTMU - S3 and Nextcloud integration"""

import os
import tempfile
from src.ctmu.storage import *

def demo_s3_operations():
    """Demonstrate S3 operations"""
    print("🪣 S3 Storage Demo")
    print("=" * 50)
    
    # Create a test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Hello from CTMU S3 demo!")
        test_file = f.name
    
    try:
        bucket = "my-test-bucket"
        key = "demo/test.txt"
        
        print(f"📤 Uploading {test_file} to S3...")
        result = s3_upload(test_file, bucket, key)
        print(f"   {result}")
        
        print(f"📋 Listing bucket contents...")
        objects = s3_list(bucket, "demo/")
        if isinstance(objects, list):
            for obj in objects:
                print(f"   📄 {obj['Key']} ({obj['Size']} bytes)")
        
        print(f"📥 Downloading from S3...")
        download_path = "downloaded_test.txt"
        result = s3_download(bucket, key, download_path)
        print(f"   {result}")
        
        # Clean up
        os.unlink(test_file)
        if os.path.exists(download_path):
            os.unlink(download_path)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure AWS credentials are configured")

def demo_nextcloud_operations():
    """Demonstrate Nextcloud operations"""
    print("\n☁️  Nextcloud Storage Demo")
    print("=" * 50)
    
    # Create a test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Hello from CTMU Nextcloud demo!")
        test_file = f.name
    
    try:
        # Example Nextcloud configuration
        url = "https://cloud.example.com/remote.php/dav/files/username/"
        username = "demo_user"
        password = "demo_password"
        remote_path = "/demo/test.txt"
        
        print(f"📤 Uploading {test_file} to Nextcloud...")
        result = nextcloud_upload(test_file, remote_path, url, username, password)
        print(f"   {result}")
        
        print(f"📋 Listing directory contents...")
        items = nextcloud_list("/demo/", url, username, password)
        if isinstance(items, list):
            for item in items:
                size_info = f" ({item['Size']} bytes)" if item['Type'] == 'File' else ""
                print(f"   📁 {item['Name']} [{item['Type']}]{size_info}")
        
        print(f"📥 Downloading from Nextcloud...")
        download_path = "downloaded_nextcloud_test.txt"
        result = nextcloud_download(remote_path, download_path, url, username, password)
        print(f"   {result}")
        
        # Clean up
        os.unlink(test_file)
        if os.path.exists(download_path):
            os.unlink(download_path)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Update the Nextcloud configuration with your server details")

def main():
    """Run storage demos"""
    print("🛠️  CTMU Storage Integration Demo")
    print("=" * 60)
    
    # S3 Demo
    demo_s3_operations()
    
    # Nextcloud Demo  
    demo_nextcloud_operations()
    
    print("\n✅ Demo completed!")
    print("\n📚 Usage Examples:")
    print("   ctmu s3 upload file.txt my-bucket --key path/file.txt")
    print("   ctmu nextcloud list /remote/ -u https://cloud.example.com/remote.php/dav/files/user/ --username user --password pass")

if __name__ == "__main__":
    main()