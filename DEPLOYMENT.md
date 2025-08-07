# 🚀 AI NPC Dialogue Generator - Deployment Guide

## 📋 Prerequisites

- Python 3.9+
- Groq API key
- Git

## 🔧 Local Development Setup

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd hackathomnmmmmm
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file:
```bash
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=development
```

### 4. Run Locally
```bash
python app.py
```
Visit: http://localhost:8080

## 🌐 Deployment Options

### Option 1: Heroku Deployment

#### 1. Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### 2. Login and Create App
```bash
heroku login
heroku create your-app-name
```

#### 3. Set Environment Variables
```bash
heroku config:set GROQ_API_KEY=your_groq_api_key_here
```

#### 4. Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### 5. Open App
```bash
heroku open
```

### Option 2: Railway Deployment

#### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

#### 2. Login and Deploy
```bash
railway login
railway init
railway up
```

#### 3. Set Environment Variables
```bash
railway variables set GROQ_API_KEY=your_groq_api_key_here
```

### Option 3: Render Deployment

#### 1. Connect GitHub Repository
- Go to [Render](https://render.com)
- Connect your GitHub repository
- Create a new Web Service

#### 2. Configure Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Environment Variables**: Add `GROQ_API_KEY`

### Option 4: VPS Deployment

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip nginx -y

# Install virtual environment
sudo apt install python3-venv -y
```

#### 2. Application Setup
```bash
# Clone repository
git clone <your-repo-url>
cd hackathomnmmmmm

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY=your_groq_api_key_here
```

#### 3. Run with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### 4. Nginx Configuration
Create `/etc/nginx/sites-available/npc-chat`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/npc-chat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |
| `FLASK_ENV` | Flask environment (development/production) | ❌ No |
| `PORT` | Port number (auto-set by platforms) | ❌ No |

## 📁 Project Structure

```
hackathomnmmmmm/
├── app.py                 # Main production server
├── web_interface.py       # Development server
├── main_groq.py          # FastAPI server
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment
├── runtime.txt           # Python version
├── templates/
│   └── index.html        # Chat interface
├── .env                  # Environment variables (local)
└── DEPLOYMENT.md         # This file
```

## 🚀 Quick Deploy Commands

### Heroku
```bash
heroku create your-app-name
heroku config:set GROQ_API_KEY=your_key
git push heroku main
```

### Railway
```bash
railway login
railway init
railway variables set GROQ_API_KEY=your_key
railway up
```

### Render
- Connect GitHub repo
- Set environment variables
- Deploy automatically

## 🔧 Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Ensure `GROQ_API_KEY` is set in environment variables
   - Check `.env` file exists locally

2. **Port Already in Use**
   - Kill existing processes: `pkill -f python`
   - Use different port: `PORT=8081 python app.py`

3. **Dependencies Issues**
   - Update pip: `pip install --upgrade pip`
   - Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

4. **Voice Issues**
   - Voice synthesis is client-side only
   - Works best in Chrome/Edge browsers
   - May not work on all mobile devices

## 📞 Support

For deployment issues:
1. Check logs: `heroku logs --tail` (Heroku)
2. Check Railway dashboard for errors
3. Verify environment variables are set correctly
4. Ensure all dependencies are installed

## 🎮 Features

- ✅ **10 Unique NPCs** with distinct personalities
- ✅ **Real-time Chat Interface** with message bubbles
- ✅ **Voice Input/Output** (client-side)
- ✅ **Multiple AI Models** (Llama3, Gemma2)
- ✅ **Responsive Design** for mobile/desktop
- ✅ **Production Ready** for deployment

## 🔄 Updates

To update the deployed application:
```bash
git add .
git commit -m "Update application"
git push heroku main  # or your deployment platform
``` 