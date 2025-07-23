#!/usr/bin/env python3
"""
Dependency checker for CancerCareBot project.
This script checks if all required dependencies are installed and working.
"""

import sys
import importlib

def check_dependency(package_name, import_name=None):
    """Check if a package is installed and can be imported."""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✓ {package_name} - OK")
        return True
    except ImportError:
        print(f"✗ {package_name} - Missing or not installed")
        return False

def main():
    print("Checking dependencies for CancerCareBot...\n")
    
    dependencies = [
        ("flask", "flask"),
        ("langchain", "langchain"),
        ("langchain-community", "langchain_community"),
        ("ctransformers", "ctransformers"),
        ("chromadb", "chromadb"),
        ("pypdf", "pypdf"),
        ("sentence-transformers", "sentence_transformers"),
        ("torch", "torch"),
    ]
    
    all_good = True
    for package, import_name in dependencies:
        if not check_dependency(package, import_name):
            all_good = False
    
    print("\n" + "="*50)
    if all_good:
        print("✓ All dependencies are installed correctly!")
        print("\nNext steps:")
        print("1. Make sure the neural-chat model is downloaded")
        print("2. Run: python ingest.py")
        print("3. Run: python app.py")
    else:
        print("✗ Some dependencies are missing!")
        print("\nPlease run: pip install -r requirements.txt")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
