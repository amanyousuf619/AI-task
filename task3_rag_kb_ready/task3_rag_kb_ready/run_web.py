#!/usr/bin/env python3
"""
Web server startup script for RAG Knowledge Base
"""
import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting RAG Knowledge Base Web Server...")
    print("Server will be available at: http://127.0.0.1:8000")
    print("Try: http://127.0.0.1:8000/query?q=delivery")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        "app.web:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
