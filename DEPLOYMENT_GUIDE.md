# 🚀 Deploy Your UCP Shopping Agent Demo

## Step 1: Prepare Your Project

### A. Update Your API Key Setup
Your current code has the API key visible. We need to hide it for security.

**Edit `server.py`:** Change line 25 from:
```python
API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDgXM23SMpUC1KvJHLkd1n_3e5lOYQzYV0')
```

To:
```python
API_KEY = os.environ.get('GEMINI_API_KEY', '')
if not API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY environment variable not set!")
```

### B. Fix Your .gitignore File
Rename `_gitignore` to `.gitignore` (with a dot at the start)

---

## Step 2: Put Your Code on GitHub

### Option A: Using GitHub Website (Easiest)

1. **Create a GitHub Account**
   - Go to https://github.com
   - Click "Sign up" (skip if you already have an account)

2. **Create a New Repository**
   - Click the "+" icon in top right
   - Select "New repository"
   - Repository name: `ucp-shopping-demo`
   - Description: "AI-powered shopping agent demo with UCP and AP2"
   - Keep it **Public** (so it can be deployed free)
   - ✅ Check "Add a README file"
   - Click "Create repository"

3. **Upload Your Files**
   - Click "Add file" → "Upload files"
   - Drag all your files:
     - `server.py`
     - `products.json`
     - `requirements.txt`
     - `README.md`
     - `.gitignore`
     - `index.html` (goes in a folder called `static`)
   - Write commit message: "Initial commit"
   - Click "Commit changes"

### Option B: Using Git (If you know command line)

```bash
# In your project folder
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ucp-shopping-demo.git
git push -u origin main
```

---

## Step 3: Deploy to Render (Free & Easy)

### Why Render?
- ✅ Free tier available
- ✅ Easy setup
- ✅ Stays online 24/7
- ✅ No credit card required

### Deployment Steps

1. **Create Render Account**
   - Go to https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub (recommended)

2. **Connect Your Repository**
   - Click "New +" → "Web Service"
   - Click "Connect GitHub"
   - Find your `ucp-shopping-demo` repository
   - Click "Connect"

3. **Configure the Service**
   Fill in these settings:
   
   - **Name**: `ucp-shopping-demo`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Instance Type**: `Free`

4. **Add Environment Variable**
   - Scroll down to "Environment Variables"
   - Click "Add Environment Variable"
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `AIzaSyDgXM23SMpUC1KvJHLkd1n_3e5lOYQzYV0`
   - Click "Add"

5. **Deploy**
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - You'll get a URL like: `https://ucp-shopping-demo.onrender.com`

---

## Step 4: Fix the Server for Production

Your Flask app needs a small change to work online. Update the last line of `server.py`:

**Change from:**
```python
app.run(debug=True, port=5000)
```

**To:**
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=False)
```

Then push this change to GitHub:
- Edit the file on GitHub.com
- Or if using Git: `git commit -am "Fix for production" && git push`

Render will automatically redeploy!

---

## Step 5: Test Your Live Site

1. Open your Render URL (like `https://ucp-shopping-demo.onrender.com`)
2. Try chatting: "Show me running shoes"
3. Add items to cart
4. Test checkout

---

## 🎉 You're Done!

### Share Your Project

Add this to your portfolio:

**Live Demo**: https://your-app.onrender.com
**GitHub Code**: https://github.com/YOUR_USERNAME/ucp-shopping-demo

### Update Your README

Add a banner at the top of your `README.md`:

```markdown
## 🌐 Live Demo

**[Try it live here!](https://your-app.onrender.com)** 👈 Click to see the demo

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)
```

---

## ⚠️ Important Notes

### Free Tier Limitations
- App "sleeps" after 15 minutes of inactivity
- First load after sleep takes 30-60 seconds
- 750 hours/month free (enough for demo purposes)

### Keep It Awake (Optional)
Use a service like [UptimeRobot](https://uptimerobot.com):
- Free account
- Add your URL to monitor
- Pings every 5 minutes
- Keeps your app awake

### API Key Security
- ✅ Never commit API keys to GitHub
- ✅ Always use environment variables
- ⚠️ Your current key is exposed - consider generating a new one from Google Cloud Console

---

## Alternative: Deploy to Railway

If Render doesn't work, try [Railway](https://railway.app):

1. Sign up at railway.app
2. "New Project" → "Deploy from GitHub"
3. Select your repo
4. Add `GEMINI_API_KEY` environment variable
5. Railway auto-detects Python and deploys!

---

## Need Help?

If something doesn't work:
1. Check Render logs: Dashboard → Your Service → Logs
2. Common issues:
   - **"Module not found"**: Check `requirements.txt`
   - **"Port already in use"**: Use `PORT` environment variable
   - **"API key error"**: Check environment variable is set

---

## 📝 Checklist

- [ ] Updated `server.py` to hide API key
- [ ] Renamed `_gitignore` to `.gitignore`
- [ ] Created GitHub repository
- [ ] Uploaded all files to GitHub
- [ ] Created Render account
- [ ] Deployed to Render
- [ ] Added `GEMINI_API_KEY` environment variable
- [ ] Fixed Flask server for production
- [ ] Tested live URL
- [ ] Updated README with live demo link
- [ ] Added to portfolio!

---

Good luck with your project! 🚀
