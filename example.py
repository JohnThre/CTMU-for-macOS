#!/usr/bin/env python3
"""Example usage of CTMU Swiss Army Knife CLI Tool"""

import os
import subprocess
import tempfile
from pathlib import Path

def run_command(cmd):
    """Run a CTMU command and display output"""
    print(f"\n🔧 Running: ctmu {cmd}")
    try:
        result = subprocess.run(f"python -m ctmu.cli {cmd}", 
                              shell=True, capture_output=True, text=True, cwd="src")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Error running command: {e}")

def main():
    print("🛠️  CTMU Swiss Army Knife - Example Demonstrations")
    print("=" * 50)
    
    # Create example directory
    example_dir = "./swiss_army_examples"
    os.makedirs(example_dir, exist_ok=True)
    
    # 1. QR Code Generation
    print("\n🎯 QR Code Generation")
    run_command(f"qr https://github.com --style bauhaus --output {example_dir}")
    
    # 2. Hashing Examples
    print("\n🔐 Hashing & Security")
    
    # Create a test file
    test_file = Path(example_dir) / "test.txt"
    test_file.write_text("Hello, CTMU Swiss Army Knife!")
    
    run_command(f'hash text "Hello World"')
    run_command(f"hash file {test_file}")
    
    # 3. Encoding Examples
    print("\n📝 Encoding/Decoding")
    run_command('encode b64 "Swiss Army Knife"')
    run_command('encode b64d "U3dpc3MgQXJteSBLbmlmZQ=="')
    
    # 4. Network Examples
    print("\n🌐 Network Utilities")
    run_command("net ping google.com --port 80")
    run_command("net scan google.com --start 80 --end 85")
    run_command("net headers https://httpbin.org/headers")
    print("\n📝 Note: nmap requires installation: brew install nmap")
    run_command("net nmap --help")
    
    # 5. File Operations
    print("\n📁 File Operations")
    run_command(f"file info {test_file}")
    run_command(f"file tree {example_dir}")
    
    # 6. System Information
    print("\n💻 System Information")
    run_command("sys info")
    run_command("sys battery")
    
    # 7. Image Processing (if we have an image)
    print("\n🖼️  Image Processing")
    
    # Create a simple test image
    try:
        from PIL import Image
        test_img = Image.new('RGB', (200, 200), color='red')
        img_path = Path(example_dir) / "test_image.png"
        test_img.save(img_path)
        
        run_command(f"img resize {img_path} {example_dir}/resized.png --width 100")
        run_command(f"img convert {img_path} {example_dir}/converted.jpg --format JPEG")
    except ImportError:
        print("PIL not available for image processing demo")
    
    # 8. Emacs Integration
    print("\n📝 GNU Emacs Integration")
    run_command('emacs eval "(+ 2 3)"')
    run_command('emacs --help')
    
    print(f"\n🎉 All examples completed! Check {example_dir} for outputs.")
    print("\n💡 Try running individual commands:")
    print("   ctmu --help")
    print("   ctmu qr --help")
    print("   ctmu hash --help")
    print("   ctmu net --help")
    print("   ctmu emacs --help")

if __name__ == "__main__":
    main()