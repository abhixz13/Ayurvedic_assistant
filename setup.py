#!/usr/bin/env python3
"""
Setup script for the Ayurvedic Diagnostic Assistant.
"""

import os
import sys
from pathlib import Path

def main():
    """Main setup function."""
    print("🩺 Ayurvedic Diagnostic Assistant - Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print("✅ Python version is compatible")
    
    # Check if virtual environment is activated
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
    else:
        print("⚠️  Virtual environment not detected")
        print("💡 Consider creating a virtual environment:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    
    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        print("💡 Create .env file with your Google API key:")
        print("   cp env.example .env")
        print("   # Edit .env and add: GOOGLE_API_KEY=your_key_here")
        return False
    
    # Check for required directories
    required_dirs = ["src", "data", "tests"]
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ {dir_name}/ directory found")
        else:
            print(f"❌ {dir_name}/ directory not found")
            return False
    
    # Check for required files
    required_files = [
        "requirements.txt",
        "src/__init__.py",
        "src/ai/diagnostic_engine.py",
        "src/ui/gradio_ui.py"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} found")
        else:
            print(f"❌ {file_path} not found")
            return False
    
    print("\n🎉 Setup validation completed!")
    print("\n📋 Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run: python gradio_demo.py (for web interface)")
    print("3. Run: python interactive_demo.py (for command-line interface)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 