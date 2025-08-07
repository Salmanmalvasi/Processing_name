# 🚀 Vercel Deployment Guide - AI NPC Dialogue Generator

## 📋 Prerequisites

- [Vercel Account](https://vercel.com/signup)
- [GitHub Account](https://github.com)
- Groq API Key

## 🔧 Step-by-Step Vercel Deployment

### 1. Prepare Your Repository

Make sure your project is pushed to GitHub with these files:
- `app.py` (main Flask application)
- `vercel.json` (Vercel configuration)
- `requirements.txt` (Python dependencies)
- `templates/index.html` (web interface)

### 2. Connect to Vercel

#### Option A: Vercel Dashboard
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Select the repository containing your AI NPC project

#### Option B: Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from your project directory
vercel
```

### 3. Configure Environment Variables

In your Vercel project dashboard:

1. Go to **Settings** → **Environment Variables**
2. Add the following variable:
   - **Name**: `GROQ_API_KEY`
   - **Value**: Your Groq API key
   - **Environment**: Production, Preview, Development

### 4. Deploy

#### Via Dashboard:
1. Click **Deploy** in the Vercel dashboard
2. Wait for build to complete
3. Your app will be live at `https://your-project-name.vercel.app`

#### Via CLI:
```bash
vercel --prod
```

## 🔧 Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### requirements.txt
```
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
aiohttp==3.9.1
flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
```

## 🌐 Custom Domain (Optional)

1. In Vercel dashboard, go to **Settings** → **Domains**
2. Add your custom domain
3. Follow DNS configuration instructions
4. Your app will be available at your custom domain

## 🔄 Updates

To update your deployed app:

### Via GitHub (Recommended):
1. Push changes to your GitHub repository
2. Vercel automatically redeploys

### Via CLI:
```bash
vercel --prod
```

## 🔧 Troubleshooting

### Common Issues:

1. **404 NOT_FOUND Error**
   - Check that `app.py` is the main entry point
   - Verify `vercel.json` routing configuration
   - Ensure all files are committed to GitHub
   - Test locally first: `python app.py`

2. **Build Failures**
   - Check `requirements.txt` for correct dependencies
   - Ensure `app.py` is the main entry point
   - Verify `vercel.json` configuration
   - Check Vercel build logs for specific errors

3. **Environment Variables**
   - Ensure `GROQ_API_KEY` is set in Vercel dashboard
   - Check that the variable name is exactly correct
   - Redeploy after setting environment variables

4. **API Errors**
   - Verify your Groq API key is valid
   - Check API usage limits
   - Test locally first using `test_vercel.py`

5. **Voice Features**
   - Voice synthesis works client-side only
   - May not work on all mobile devices
   - Requires HTTPS for microphone access

### Debug Steps:

1. **Test Locally First:**
   ```bash
   python app.py
   # In another terminal:
   python test_vercel.py
   ```

2. **Check Vercel Logs:**
   - Go to Vercel dashboard
   - Click on your deployment
   - Check "Functions" tab for errors

3. **Verify File Structure:**
   ```
   your-project/
   ├── app.py
   ├── vercel.json
   ├── requirements.txt
   └── templates/
       └── index.html
   ```

4. **Force Redeploy:**
   ```bash
   # Make a small change and push
   git add .
   git commit -m "Fix deployment"
   git push origin main
   ```

### Debug Commands:
```bash
# Check deployment status
vercel ls

# View deployment logs
vercel logs

# Remove deployment
vercel remove
```

## 📊 Monitoring

### Vercel Analytics:
- **Function Execution Time**: Monitor API response times
- **Error Rates**: Track failed requests
- **Geographic Distribution**: See where users are located

### Performance Tips:
1. **Cold Starts**: First request may be slower
2. **Function Timeout**: 10 seconds max per request
3. **Memory Usage**: Optimize for serverless environment

## 🎮 Features Available on Vercel

- ✅ **10 Unique NPCs** with distinct personalities
- ✅ **Real-time Chat Interface** with message bubbles
- ✅ **Voice Input** (client-side microphone)
- ✅ **Multiple AI Models** (Llama3, Gemma2)
- ✅ **Responsive Design** for mobile/desktop
- ✅ **HTTPS by default** for security
- ✅ **Global CDN** for fast loading
- ✅ **Automatic deployments** from GitHub

## 🔐 Security

- **Environment Variables**: Securely stored in Vercel
- **HTTPS**: Automatic SSL certificates
- **CORS**: Configured for cross-origin requests
- **API Key**: Never exposed in client-side code

## 📞 Support

### Vercel Support:
- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- [Vercel Status](https://vercel-status.com)

### Project Issues:
1. Check deployment logs in Vercel dashboard
2. Test API endpoints locally first
3. Verify environment variables are set correctly
4. Check Groq API status and limits

## 🚀 Quick Deploy Checklist

- [ ] Repository pushed to GitHub
- [ ] `vercel.json` configured
- [ ] `requirements.txt` updated
- [ ] `GROQ_API_KEY` set in Vercel
- [ ] Domain configured (optional)
- [ ] Test deployment locally
- [ ] Monitor first deployment
- [ ] Share your live URL! 🎉

Your AI NPC Dialogue Generator will be live at:
`https://your-project-name.vercel.app` 