#!/usr/bin/env python3
"""
Server runner script for Nivaaran Backend.
"""

import sys
import os
import uvicorn
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

if __name__ == "__main__":
    print(f"🚀 Starting Nivaaran Server on http://{HOST}:{PORT}")
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
