#!/usr/bin/env python3
"""
Startup script for AI NPC Dialogue Generator Web Interface
Runs both the API server and web interface
"""

import subprocess
import time
import sys
import os

def start_api_server():
    """Start the Groq API server"""
    print("🚀 Starting Groq API server...")
    try:
        # Start the API server in the background
        api_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main_groq:app", 
            "--reload", "--port", "8002"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ API server started on http://127.0.0.1:8002")
        return api_process
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def start_web_interface():
    """Start the web interface"""
    print("🌐 Starting web interface...")
    try:
        # Start the web interface
        web_process = subprocess.Popen([
            sys.executable, "web_interface.py"
        ])
        
        print("✅ Web interface started on http://127.0.0.1:8080")
        return web_process
    except Exception as e:
        print(f"❌ Failed to start web interface: {e}")
        return None

def main():
    print("🎭 AI NPC Dialogue Generator - Web Interface")
    print("=" * 50)
    
    # Check if required files exist
    if not os.path.exists("main_groq.py"):
        print("❌ Error: main_groq.py not found!")
        return
    
    if not os.path.exists("web_interface.py"):
        print("❌ Error: web_interface.py not found!")
        return
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        return
    
    # Wait a moment for API to start
    print("⏳ Waiting for API server to start...")
    time.sleep(3)
    
    # Start web interface
    web_process = start_web_interface()
    if not web_process:
        print("❌ Failed to start web interface")
        api_process.terminate()
        return
    
    print("\n🎉 Both servers are running!")
    print("📱 Web Interface: http://127.0.0.1:8080")
    print("🔌 API Server: http://127.0.0.1:8002")
    print("\n💡 Press Ctrl+C to stop both servers")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        api_process.terminate()
        web_process.terminate()
        print("✅ Servers stopped")

if __name__ == "__main__":
    main() 