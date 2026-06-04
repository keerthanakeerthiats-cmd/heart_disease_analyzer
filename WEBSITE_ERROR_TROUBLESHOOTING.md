# 🛠️ Website Error Troubleshooting Guide

## 🔍 Common Website Errors and Solutions

### 1. "Error" or "Connection Error" Displayed on Website
This typically indicates a communication issue between the browser and the server.

**Solutions:**
1. **Check if server is running:**
   - Look for the Command Prompt window with server output
   - You should see "Running on http://127.0.0.1:5000" or similar

2. **Try different URLs:**
   - http://localhost:5001 (if using fixed version)
   - http://127.0.0.1:5000
   - http://127.0.0.1:5001

3. **Check for port conflicts:**
   - Run the diagnostic tool to check port availability
   - Use the fixed version which uses port 5001

### 2. Blank Results or No Response
This usually means the server is running but not processing requests properly.

**Solutions:**
1. **Check server console for errors:**
   - Look for red error messages in the Command Prompt
   - These will indicate what's going wrong

2. **Verify file upload:**
   - Ensure you're selecting a valid image file
   - Check that the file isn't corrupted

3. **Restart the server:**
   - Close the Command Prompt window
   - Run the app again using the batch file

### 3. JavaScript Console Errors
These appear in the browser's developer tools.

**Solutions:**
1. **Open Developer Tools:**
   - Press F12 in your browser
   - Click on the "Console" tab
   - Look for red error messages

2. **Common JavaScript errors:**
   - "Cannot convert undefined or null to object" - Already fixed in our updated HTML
   - "Failed to load resource" - Server not running or wrong URL
   - "CORS error" - Server configuration issue (already handled)

## 🧪 Diagnostic Steps

### Step 1: Check Server Status
1. Look at the Command Prompt window where you started the server
2. You should see something like:
   ```
   * Running on http://127.0.0.1:5000
   ```
3. If you don't see this, the server isn't running properly

### Step 2: Check Browser Console
1. Press F12 in your browser
2. Click on the "Console" tab
3. Try to upload an image
4. Look for any red error messages

### Step 3: Verify File Structure
Run the diagnostic tool:
```
python website_diagnostic.py
```

### Step 4: Test with Different Ports
If port 5000 is in use:
1. Run `RUN_FIXED_VERSION.bat` (uses port 5001)
2. Access the website at http://localhost:5001

## 🔧 Specific Solutions

### Solution 1: Use the Fixed Version
1. Double-click `RUN_FIXED_VERSION.bat`
2. This version:
   - Uses port 5001 to avoid conflicts
   - Has enhanced error handling
   - Provides detailed logging
   - Works without TensorFlow

### Solution 2: Clear Browser Cache
1. Press Ctrl+Shift+Delete
2. Select "Cached images and files"
3. Click "Clear data"
4. Refresh the page

### Solution 3: Check File Permissions
1. Ensure the `uploads` folder exists and is writable
2. Right-click the folder → Properties → Security
3. Ensure your user account has "Write" permissions

### Solution 4: Restart Everything
1. Close all Command Prompt windows
2. Close all browser windows
3. Run the diagnostic tool
4. Run the fixed version

## 🚀 Quick Fix Procedures

### Quick Fix 1: Run Diagnostic + Fixed Version
1. Double-click `RUN_FIXED_VERSION.bat`
2. Wait for browser to open
3. Try uploading an image

### Quick Fix 2: Check Everything
1. Run `website_diagnostic.py`
2. Fix any issues it identifies
3. Run `RUN_FIXED_VERSION.bat`

### Quick Fix 3: Clean Start
1. Delete the `uploads` folder
2. Restart the server with `RUN_FIXED_VERSION.bat`
3. Try uploading an image again

## 📋 Error Message Reference

### "Error: No file uploaded"
- **Cause:** File selection failed
- **Solution:** Try selecting the file again

### "Error: Server error"
- **Cause:** Backend Python error
- **Solution:** Check server console for details

### "Connection Error"
- **Cause:** Cannot reach server
- **Solution:** Check if server is running on correct port

### "Error: Invalid prediction type"
- **Cause:** URL routing issue
- **Solution:** Restart server, clear browser cache

## 🎯 If Nothing Works

1. **Take screenshots:**
   - Browser console errors (F12 → Console)
   - Server Command Prompt output
   - Exact error message on website

2. **Try the no-TensorFlow version:**
   - Run `RUN_NO_TENSORFLOW.bat`
   - This eliminates all AI dependencies

3. **Contact support with:**
   - Screenshots of errors
   - Output from diagnostic tool
   - Steps you've already tried

This guide should help you identify and resolve most website error issues.