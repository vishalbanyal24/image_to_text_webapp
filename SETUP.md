# Setup Guide for Image to Text Generator

## Quick Start (Windows)

### Step 1: Get Google API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Set Environment Variables
**Option A: Use the setup script (Recommended)**
```bash
# Run the PowerShell script
.\setup_env.ps1
```

**Option B: Manual setup**
```bash
# PowerShell
$env:GOOGLE_API_KEY="your-api-key-here"

# Command Prompt
set GOOGLE_API_KEY=your-api-key-here
```

### Step 3: Test Setup
```bash
python test_setup.py
```

### Step 4: Start the Application
```bash
python manage.py runserver
```

### Step 5: Open in Browser
Go to: http://localhost:8000

## Quick Start (Linux/Mac)

### Step 1: Get Google API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Set Environment Variables
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### Step 3: Test Setup
```bash
python test_setup.py
```

### Step 4: Start the Application
```bash
python manage.py runserver
```

### Step 5: Open in Browser
Go to: http://localhost:8000

## Troubleshooting

### Common Issues and Solutions

#### 1. "Google API key not found"
**Solution**: Set the environment variable
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your-api-key-here"

# Windows Command Prompt
set GOOGLE_API_KEY=your-api-key-here

# Linux/Mac
export GOOGLE_API_KEY="your-api-key-here"
```

#### 2. "API test failed"
**Possible causes**:
- Invalid API key
- No internet connection
- API quota exceeded

**Solutions**:
- Verify your API key is correct
- Check your internet connection
- Check your Google AI Studio quota

#### 3. "Failed to fetch image"
**Possible causes**:
- Invalid image URL
- Image URL requires authentication
- Network issues

**Solutions**:
- Try a different image URL
- Use a publicly accessible image
- Test with: `https://picsum.photos/400/300`

#### 4. Scrolling not working
**Status**: ✅ FIXED
The scrolling issue has been resolved in the latest version.

### Testing Your Setup

#### Run the Test Script
```bash
python test_setup.py
```

This will check:
- ✅ Python and Django installation
- ✅ Required packages
- ✅ Environment variables
- ✅ Image download capability
- ✅ Google API connectivity

#### Test the Web Interface
1. Start the server: `python manage.py runserver`
2. Open: http://localhost:8000
3. Try uploading an image or using a URL
4. Check the test endpoint: http://localhost:8000/test-api/

### Test Image URLs

Try these test images:
- `https://picsum.photos/400/300`
- `https://via.placeholder.com/400x300`
- `https://httpbin.org/image/png`

### Railway Deployment

For Railway deployment, set these environment variables:
```bash
railway variables set GOOGLE_API_KEY="your-api-key-here"
railway variables set SECRET_KEY="your-django-secret-key"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="your-railway-domain.railway.app"
```

## File Structure

```
project1/
├── test_setup.py          # Test script
├── setup_env.bat          # Windows batch setup
├── setup_env.ps1          # PowerShell setup
├── SETUP.md               # This file
├── requirements.txt       # Dependencies
├── manage.py             # Django management
└── image_converter/      # Main application
```

## Still Having Issues?

1. **Run the test script**: `python test_setup.py`
2. **Check error messages** on the web page
3. **Test API endpoint**: http://localhost:8000/test-api/
4. **Verify API key** in Google AI Studio
5. **Try a different image** URL
6. **Check internet connection**

## Support

If you're still having issues:
1. Check the error message on the web page
2. Run `python test_setup.py` and share the output
3. Try the test API endpoint and share the response
4. Verify your Google API key is valid and has quota remaining
