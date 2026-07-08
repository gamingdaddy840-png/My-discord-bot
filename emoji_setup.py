"""
Emoji Configuration Helper
This script helps you extract custom emoji IDs from your bot's test server
and configure them in the bot.

Usage:
1. Run this script: python emoji_setup.py
2. The bot will list all custom emojis it can see
3. Copy the emoji IDs and paste them in your config
"""

import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

class EmojiExtractor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def extract_emojis(self, guild_id=None):
        """Extract all custom emojis from bot's guilds"""
        print("\n" + "="*60)
        print("🎨 CUSTOM EMOJI EXTRACTOR")
        print("="*60 + "\n")
        
        for guild in self.bot.guilds:
            if guild_id and guild.id != guild_id:
                continue
            
            print(f"\n📍 Guild: {guild.name} (ID: {guild.id})")
            print("-" * 60)
            
            if not guild.emojis:
                print("No custom emojis found in this guild")
                continue
            
            for emoji in guild.emojis:
                emoji_format = f"<:{emoji.name}:{emoji.id}>"
                print(f"Name: {emoji.name:<20} | ID: {emoji.id:<20}")
                print(f"  Format: {emoji_format}")
                print(f"  URL: {emoji.url}")
                print()

async def main():
    intents = discord.Intents.default()
    intents.emojis = True
    intents.guilds = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        print(f"✅ Bot logged in as {bot.user}")
        
        extractor = EmojiExtractor(bot)
        await extractor.extract_emojis()
        
        await bot.close()
    
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Cancelled")
    except Exception as e:
        print(f"❌ Error: {e}")
