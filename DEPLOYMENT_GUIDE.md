# 🚀 Render Deployment Fix - Complete Guide

## ❌ Why Images Aren't Showing on Render

### Root Causes:
1. **Missing OpenAI API Key** - Images can't be generated without it
2. **Frontend hardcoded to localhost** - Can't reach the backend
3. **No error visibility** - Failures are silent

---

## ✅ COMPLETE FIX - Step by Step

### **STEP 1: Update Your Files on GitHub**

Replace these 3 files in your repository:

1. **api.py** (Backend with error handling)
2. **index.html** (Frontend with dynamic API URL)
3. **image_generator.py** (With explicit API key handling)
4. **prompt_builder.py** (With explicit API key handling)
5. **study_text_generator.py** (With explicit API key handling)

All fixed files are in the outputs folder!

---

### **STEP 2: Configure Render Environment Variables**

Go to your Render Dashboard → Your Service → Environment

**Add this environment variable:**

```
Key: OPENAI_API_KEY
Value: sk-proj-XXXXXXXXXXXXXXXXXX
```

**IMPORTANT:** Without this, image generation will fail!

---

### **STEP 3: Verify Render Configuration**

Make sure your Render service has:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn -b 0.0.0.0:5000 api:app
```

---

### **STEP 4: Deploy and Check Logs**

After pushing to GitHub:

1. Go to Render Dashboard → Your Service → Logs
2. Look for these messages:
   ```
   ✅ OPENAI_API_KEY is configured
   🔄 Generating content for: [question]
   📝 Step 1: Generating study text...
   ✅ Study text generated
   🎨 Step 2: Generating image...
   ✅ Image generated: output/icse_xxxxx.png
   📂 Serving file: output/icse_xxxxx.png
   ```

3. If you see errors, check:
   - Is `OPENAI_API_KEY` set correctly?
   - Is the API key valid?
   - Are there any import errors?

---

## 🔍 How to Debug on Render

### **Check if API is Working:**

Visit: `https://your-app.onrender.com/`
- Should show your ICSE Visual Learning page

### **Check Logs for Errors:**

In Render Dashboard → Logs, look for:
- `❌ Error in /generate:` - Backend error
- `⚠️ WARNING: OPENAI_API_KEY not set!` - Missing API key
- `❌ Image generation failed:` - OpenAI API issue

### **Test a Simple Request:**

Try generating study material for "What is radius?"
- Check browser console (F12) for errors
- Check Render logs for backend errors

---

## 📋 Key Changes Made

### **1. Frontend (index.html)**

**Before:**
```javascript
fetch("http://localhost:5000/generate", ...)  // ❌ Only works locally
```

**After:**
```javascript
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000' 
  : window.location.origin;

fetch(`${API_BASE_URL}/generate`, ...)  // ✅ Works everywhere
```

### **2. Backend (api.py)**

**Before:**
```python
# No error handling
generate_icse_infographic(image_prompt, image_path)
return jsonify({"study_data": study_data, "image_url": f"/{image_path}"})
```

**After:**
```python
try:
    print("🎨 Step 2: Generating image...")
    generate_icse_infographic(image_prompt, image_path)
    
    if not os.path.exists(image_path):
        raise Exception("Image file was not created")
    
    print(f"✅ Image generated: {image_path}")
    return jsonify({"study_data": study_data, "image_url": f"/{image_path}"})
except Exception as e:
    print(f"❌ Error: {str(e)}")
    traceback.print_exc()
    return jsonify({"error": str(e)}), 500
```

### **3. OpenAI Client (image_generator.py, etc.)**

**Before:**
```python
client = OpenAI()  # ❌ Might not find API key
```

**After:**
```python
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ Explicit
```

---

## 🎯 Expected Behavior After Fix

### **Local Development:**
- Works exactly as before
- Uses `http://localhost:5000`

### **Production (Render):**
- Uses `https://your-app.onrender.com`
- Generates images with OpenAI
- Serves images correctly
- Shows detailed logs for debugging

---

## 🆘 Still Having Issues?

### **Check These Common Problems:**

1. **Image shows alt text but no image:**
   - Check Render logs for "Image generation failed"
   - Verify OPENAI_API_KEY is set
   - Check OpenAI API quota/billing

2. **"Something went wrong" alert:**
   - Open browser console (F12)
   - Check for CORS or network errors
   - Check Render logs for backend errors

3. **Loading forever:**
   - OpenAI image generation takes 5-15 seconds
   - Check Render logs to see if it's stuck

4. **Wrong image or old image:**
   - Images are ephemeral on Render (reset on deploy)
   - Each generation creates a new unique file

---

## 💡 Pro Tips

1. **Always check Render logs first** - They show exactly what's happening
2. **Test locally before deploying** - Make sure it works with your API key
3. **Monitor OpenAI usage** - Image generation uses API credits
4. **Use guest limits** - Prevents API abuse

---

## 📞 Quick Checklist

Before asking for help, verify:

- [ ] OPENAI_API_KEY is set in Render environment
- [ ] All 5 Python files are updated (api.py, image_generator.py, etc.)
- [ ] index.html is updated with dynamic API_BASE_URL
- [ ] Render logs show "✅ OPENAI_API_KEY is configured"
- [ ] No errors in Render logs during generation
- [ ] Browser console (F12) shows no errors

---

Good luck! 🚀
