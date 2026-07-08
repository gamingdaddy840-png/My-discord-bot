import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DEFAULT_PREFIX = '!'

# Database
DATABASE_FILE = 'bot_data.db'

# Colors for embeds
COLORS = {
    'success': 0x00FF00,
    'error': 0xFF0000,
    'info': 0x0099FF,
    'warning': 0xFFFF00,
}

# Timeouts
WARN_TIMEOUT = 30  # days
