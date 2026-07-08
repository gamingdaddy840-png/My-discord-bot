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

# Custom Emojis Configuration
# To get emoji IDs, run: python emoji_setup.py
# Then replace the emoji IDs below with your custom emojis
# Format: '<:emoji_name:ID>' or use default unicode emojis

EMOJIS = {
    # System Emojis - UPDATE WITH YOUR CUSTOM EMOJI IDs
    'success': '<:success:YOUR_EMOJI_ID>',           # ✅
    'error': '<:error:YOUR_EMOJI_ID>',               # ❌
    'warning': '<:warning:YOUR_EMOJI_ID>',           # ⚠️
    'info': '<:info:YOUR_EMOJI_ID>',                 # ℹ️
    'loading': '<:loading:YOUR_EMOJI_ID>',           # ⏳
    
    # Moderation Emojis
    'mute': '<:mute:YOUR_EMOJI_ID>',                 # 🔇
    'unmute': '<:unmute:YOUR_EMOJI_ID>',             # 🔊
    'kick': '<:kick:YOUR_EMOJI_ID>',                 # 👢
    'ban': '<:ban:YOUR_EMOJI_ID>',                   # 🚫
    'warn': '<:warn:YOUR_EMOJI_ID>',                 # ⚠️
    'lock': '<:lock:YOUR_EMOJI_ID>',                 # 🔒
    'unlock': '<:unlock:YOUR_EMOJI_ID>',             # 🔓
    'slowmode': '<:slowmode:YOUR_EMOJI_ID>',         # 🐢
    'mod': '<:mod:YOUR_EMOJI_ID>',                   # 🛡️
    
    # Welcome System
    'welcome': '<:welcome:YOUR_EMOJI_ID>',           # 👋
    'user_join': '<:user_join:YOUR_EMOJI_ID>',       # ✅
    'user_leave': '<:user_leave:YOUR_EMOJI_ID>',     # 👋
    
    # Fun & Games
    'game': '<:game:YOUR_EMOJI_ID>',                 # 🎮
    'giveaway': '<:giveaway:YOUR_EMOJI_ID>',         # 🎁
    'ticket': '<:ticket:YOUR_EMOJI_ID>',             # 🎫
    'afk': '<:afk:YOUR_EMOJI_ID>',                   # 💤
    'levelup': '<:levelup:YOUR_EMOJI_ID>',           # 📈
    
    # Economy
    'money': '<:money:YOUR_EMOJI_ID>',               # 💰
    'bank': '<:bank:YOUR_EMOJI_ID>',                 # 🏦
    'wallet': '<:wallet:YOUR_EMOJI_ID>',             # 👛
    'coin': '<:coin:YOUR_EMOJI_ID>',                 # 🪙
    'leaderboard': '<:leaderboard:YOUR_EMOJI_ID>',   # 🏆
    
    # AI
    'ai': '<:ai:YOUR_EMOJI_ID>',                     # 🤖
    'ask': '<:ask:YOUR_EMOJI_ID>',                   # ❓
    
    # Logs & Actions
    'logs': '<:logs:YOUR_EMOJI_ID>',                 # 📊
    'delete': '<:delete:YOUR_EMOJI_ID>',             # 🗑️
    'edit': '<:edit:YOUR_EMOJI_ID>',                 # ✏️
    
    # Extra
    'settings': '<:settings:YOUR_EMOJI_ID>',         # ⚙️
    'help': '<:help:YOUR_EMOJI_ID>',                 # 📖
    'search': '<:search:YOUR_EMOJI_ID>',             # 🔍
    'user': '<:user:YOUR_EMOJI_ID>',                 # 👤
    'role': '<:role:YOUR_EMOJI_ID>',                 # 🎭
}

# Function to get emoji
def get_emoji(name):
    """Get emoji by name, fallback to unicode if custom emoji fails"""
    fallback_emojis = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'loading': '⏳',
        'mute': '🔇',
        'unmute': '🔊',
        'kick': '👢',
        'ban': '🚫',
        'warn': '⚠️',
        'lock': '🔒',
        'unlock': '🔓',
        'slowmode': '🐢',
        'mod': '🛡️',
        'welcome': '👋',
        'user_join': '✅',
        'user_leave': '👋',
        'game': '🎮',
        'giveaway': '🎁',
        'ticket': '🎫',
        'afk': '💤',
        'levelup': '📈',
        'money': '💰',
        'bank': '🏦',
        'wallet': '👛',
        'coin': '🪙',
        'leaderboard': '🏆',
        'ai': '🤖',
        'ask': '❓',
        'logs': '📊',
        'delete': '🗑️',
        'edit': '✏️',
        'settings': '⚙️',
        'help': '📖',
        'search': '🔍',
        'user': '👤',
        'role': '🎭',
    }
    
    emoji = EMOJIS.get(name, fallback_emojis.get(name, ''))
    
    # Check if it's a custom emoji format and contains 'YOUR_EMOJI_ID'
    if 'YOUR_EMOJI_ID' in str(emoji):
        return fallback_emojis.get(name, '')
    
    return emoji
