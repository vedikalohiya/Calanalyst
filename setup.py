"""
Setup script for CancerCareBot project.
This script will help download the required LLM model and set up dependencies.
"""

import os
import urllib.request
import sys

def download_model():
    """Download the neural-chat model if it doesn't exist."""
    model_name = "neural-chat-7b-v3-1.Q4_K_M.gguf"
    model_url = f"https://huggingface.co/TheBloke/neural-chat-7B-v3-1-GGUF/resolve/main/{model_name}"
    
    if os.path.exists(model_name):
        print(f"Model {model_name} already exists. Skipping download.")
        return True
    
    print(f"Downloading {model_name}...")
    print("This may take a while (model is ~4GB)...")
    
    try:
        urllib.request.urlretrieve(model_url, model_name)
        print(f"Successfully downloaded {model_name}")
        return True
    except Exception as e:
        print(f"Failed to download model: {e}")
        print("Please download the model manually from:")
        print(model_url)
        return False

def main():
    print("Setting up CancerCareBot...")
    if not os.path.exists("app.py"):
        print("Error: Please run this script from the project root directory.")
        sys.exit(1)
    download_model()
    
    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run data ingestion: python ingest.py")
    print("3. Start the application: python app.py")

if __name__ == "__main__":
    main()
