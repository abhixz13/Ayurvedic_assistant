#!/usr/bin/env python3
"""
Setup script for Ayurvedic Diagnostic Assistant.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories."""
    directories = [
        "data/raw",
        "data/processed", 
        "logs",
        "notebooks",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies."""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def setup_environment():
    """Setup environment variables."""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("📝 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("""# Google AI API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Model Configuration
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.2
MAX_TOKENS=4096

# RAG Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5

# Vector Store Configuration
VECTOR_STORE_PATH=./data/processed/vector_store
USE_GPU=false

# Document Processing
SUPPORTED_FORMATS=pdf,docx,txt
MAX_FILE_SIZE_MB=50

# UI Configuration
DISPLAY_MODE=html
ENABLE_INTERACTIVE=true
""")
        print("✅ Created .env file")
        print("⚠️  Please edit .env file and add your Google API key")
    else:
        print("✅ .env file already exists")

def run_tests():
    """Run the test suite."""
    return run_command("python -m pytest tests/ -v", "Running tests")

def main():
    """Main setup function."""
    print("🚀 Setting up Ayurvedic Diagnostic Assistant...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies FIRST
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # THEN run tests
    print("\n🧪 Running tests...")
    if run_tests():
        print("✅ All tests passed")
    else:
        print("⚠️  Some tests failed, but setup can continue")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your Google API key")
    print("2. Add Ayurvedic documents to data/raw/ directory")
    print("3. Run: jupyter notebook notebooks/main_assistant.ipynb")
    print("4. Follow the notebook instructions")
    
    print("\n⚠️  Important:")
    print("- This tool is for educational purposes only")
    print("- Always consult qualified practitioners for medical advice")
    print("- Keep your API key secure and never commit it to version control")

if __name__ == "__main__":
    main() 