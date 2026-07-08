#!/usr/bin/env python3
"""
Discord Bot - Startup Script
This script helps you set up and run the bot easily
"""

import os
import sys
import asyncio
from pathlib import Path

def check_env():
    """Check if .env file exists"""
    if not Path('.env').exists():
        print("⚠️  .env file not found!")
        print("Creating .env from .env.example...")
        if Path('.env.example').exists():
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✅ .env created. Please edit it with your tokens.")
            return False
        else:
            print("❌ .env.example not found")
            return False
    return True

def check_requirements():
    """Check if requirements are installed"""
    try:
        import discord
        import dotenv
        import aiosqlite
        print("✅ All requirements installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def main():
    """Main startup function"""
    print("🤖 Discord Bot Startup")
    print("=" * 40)
    
    # Check environment
    if not check_env():
        print("\n⚠️  Please configure .env file and try again")
        return
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please install requirements and try again")
        return
    
    # Try to import and run bot
    try:
        import main
        print("\n🚀 Starting bot...")
        asyncio.run(main.main())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
