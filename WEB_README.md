# 🌐 AI NPC Dialogue Generator - Web Interface

A modern web-based chatbot interface for the AI NPC Dialogue Generator with character and model selection.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Both Servers (Recommended)
```bash
python3 start_web.py
```

This will start both the API server and web interface automatically.

### 3. Manual Start (Alternative)
```bash
# Terminal 1: Start API server
python3 -m uvicorn main_groq:app --reload --port 8002

# Terminal 2: Start web interface
python3 web_interface.py
```

### 4. Access the Web Interface
Open your browser and go to: **http://127.0.0.1:8080**

## 🎭 Features

### **Character Selection**
- **Drogun** 🗡️ - Gruff Blacksmith
- **Lira** 🧪 - Enthusiastic Potion Seller
- **Eldrin** 🌲 - Mysterious Forest Hermit
- **Garrick** 🛡️ - Cynical City Guard
- **Elara** 🏪 - Cheerful Shopkeeper

### **Model Selection**
- **llama3-8b-8192** - Fast, good for dialogue
- **llama3-70b-8192** - More powerful, better responses
- **mixtral-8x7b-32768** - Balanced performance
- **gemma2-9b-it** - Efficient and reliable

### **Web Interface Features**
- ✅ **Real-time chat** with typing indicators
- ✅ **Character switching** with visual feedback
- ✅ **Model selection** dropdown
- ✅ **API status monitoring**
- ✅ **Responsive design** (mobile-friendly)
- ✅ **Modern UI** with gradients and animations
- ✅ **Error handling** with user-friendly messages

## 🎨 Interface Design

### **Layout**
- **Header**: Title and description
- **Sidebar**: Character selection, model selection, and status
- **Chat Area**: Message history and input

### **Styling**
- **Modern gradient background**
- **Card-based character selection**
- **Bubble-style chat messages**
- **Smooth animations and transitions**
- **Responsive grid layout**

## 🔧 Technical Details

### **Backend**
- **Flask** web framework
- **RESTful API** integration
- **JSON** communication
- **Error handling** and status monitoring

### **Frontend**
- **Vanilla JavaScript** (no frameworks)
- **CSS Grid** and **Flexbox** layout
- **Responsive design** with media queries
- **Real-time status updates**

### **API Integration**
- **POST /chat** - Send messages
- **GET /api/status** - Check API health
- **Automatic retry** and error handling

## 📱 Mobile Support

The web interface is fully responsive and works on:
- ✅ **Desktop browsers**
- ✅ **Tablets**
- ✅ **Mobile phones**

## 🛠️ Customization

### **Adding New Characters**
Edit `web_interface.py` and add to the `CHARACTERS` dictionary:

```python
"new_character": {
    "name": "Character Name",
    "type": "Character Type",
    "traits": "Character traits and personality",
    "description": "Character description",
    "emoji": "🎭"
}
```

### **Adding New Models**
Edit `web_interface.py` and add to the `MODELS` dictionary:

```python
"new-model": {
    "name": "model-name",
    "description": "Model description",
    "speed": "Speed rating",
    "quality": "Quality rating"
}
```

## 🚨 Troubleshooting

### **Web Interface Not Loading**
1. Check if Flask is installed: `pip install flask`
2. Ensure port 5000 is available
3. Check console for error messages

### **API Connection Issues**
1. Verify API server is running on port 8002
2. Check `.env` file for API key
3. Test API directly: `curl http://127.0.0.1:8002/health`

### **Character/Model Not Working**
1. Check browser console for JavaScript errors
2. Verify API response format
3. Test with different character/model combinations

## 🎯 Usage Examples

### **Chat with Drogun (Fast Model)**
1. Select **Drogun** character
2. Choose **llama3-8b-8192** model
3. Type: "Can you repair my sword?"
4. Get grumpy blacksmith response

### **Chat with Lira (Powerful Model)**
1. Select **Lira** character
2. Choose **llama3-70b-8192** model
3. Type: "What potions do you have?"
4. Get enthusiastic sales pitch

### **Compare Models**
1. Try the same message with different models
2. Notice response quality and speed differences
3. Choose the best model for your needs

## 🔗 Related Files

- `web_interface.py` - Flask web application
- `templates/index.html` - Web interface template
- `start_web.py` - Automated startup script
- `main_groq.py` - API server
- `requirements.txt` - Dependencies

## 🎉 Enjoy Your AI NPC Chatbot!

The web interface provides a user-friendly way to interact with your AI NPCs. Switch between characters and models to find the perfect combination for your needs! 