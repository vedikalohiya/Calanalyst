# Troubleshooting Guide for CancerCareBot

## Common Issues and Solutions

### 1. Import Errors
**Problem:** Getting import errors like "Import 'langchain' could not be resolved"

**Solution:**
```bash
pip install -r requirements.txt
```

If you're still getting errors, try upgrading pip first:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Model Not Found Error
**Problem:** "Error: Model file 'neural-chat-7b-v3-1.Q4_K_M.gguf' not found!"

**Solution:**
- Run the setup script: `python setup.py`
- Or download manually from: https://huggingface.co/TheBloke/neural-chat-7B-v3-1-GGUF/resolve/main/neural-chat-7b-v3-1.Q4_K_M.gguf
- Place the downloaded file in the project root directory

### 3. Data Directory Issues
**Problem:** "Error: 'Data/' directory not found!" or "No PDF files found"

**Solution:**
- Make sure the directory is named "Data" (with capital D)
- Ensure PDF files are present in the Data directory
- Check file permissions

### 4. Memory Issues
**Problem:** Application crashes with out-of-memory errors

**Solution:**
- Close other applications to free up RAM
- The application requires at least 8GB RAM
- Consider using a machine with more memory

### 5. Port Already in Use
**Problem:** "Address already in use" when starting the Flask app

**Solution:**
```bash
# Kill any process using port 5000
lsof -ti:5000 | xargs kill -9
# Then restart the app
python app.py
```

### 6. Vector Store Issues
**Problem:** Issues with creating or loading vector store

**Solution:**
- Delete the `stores/` directory and recreate it:
```bash
rm -rf stores/
python ingest.py
```

### 7. Slow Performance
**Problem:** Application is very slow

**Solution:**
- Ensure you're running on a machine with adequate CPU
- The model runs on CPU, so a faster CPU will improve performance
- Close unnecessary applications

## Dependency Check
Run this command to check if all dependencies are properly installed:
```bash
python check_deps.py
```

## Getting Help
If you're still experiencing issues:
1. Check that you're using Python 3.8 or higher
2. Ensure all files are in the correct locations
3. Verify that you have sufficient disk space (5GB+ free)
4. Check the console output for specific error messages

## Quick Setup Summary
```bash
# 1. Download the model
python setup.py

# 2. Install dependencies
pip install -r requirements.txt

# 3. Check dependencies
python check_deps.py

# 4. Process the data
python ingest.py

# 5. Start the application
python app.py
```
