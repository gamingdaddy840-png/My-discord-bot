"""
Extract Custom Emojis from Discord Developer Portal
This script retrieves emojis uploaded to your bot's application
in the Discord Developer Portal.

These emojis are automatically available to your bot without
needing to be in a specific server.
"""

import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

class DeveloperPortalEmojiExtractor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def extract_dev_portal_emojis(self):
        """Extract emojis from Developer Portal (application emojis)"""
        print("\n" + "="*70)
        print("🎨 DEVELOPER PORTAL EMOJI EXTRACTOR")
        print("="*70 + "\n")
        
        try:
            # Get the bot's application
            app = await self.bot.application_info()
            
            print(f"✅ Bot Application: {app.name}")
            print(f"📱 Application ID: {app.id}\n")
            
            # Application emojis are stored in the bot's global scope
            # Try to fetch from application
            async for emoji in self.bot.fetch_application_emojis():
                emoji_format = f"<:{emoji.name}:{emoji.id}>"
                print(f"Name: {emoji.name:<25} | ID: {emoji.id:<20}")
                print(f"  Format: {emoji_format}")
                print(f"  URL: {emoji.url}")
                print()
                
        except Exception as e:
            print(f"❌ Error fetching application emojis: {e}")
            print("\n⚠️  Note: Application emojis might not be available through this method.")
            print("Try using the Discord API directly or check the Developer Portal.\n")

async def main():
    intents = discord.Intents.default()
    intents.emojis = True
    intents.applications = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        print(f"✅ Bot logged in as {bot.user}")
        
        extractor = DeveloperPortalEmojiExtractor(bot)
        await extractor.extract_dev_portal_emojis()
        
        # Alternative: Show server emojis as fallback
        print("\n" + "="*70)
        print("📍 AVAILABLE GUILD EMOJIS (Fallback)")
        print("="*70 + "\n")
        
        for guild in bot.guilds:
            if guild.emojis:
                print(f"Guild: {guild.name}")
                for emoji in guild.emojis:
                    emoji_format = f"<:{emoji.name}:{emoji.id}>"
                    print(f"  {emoji.name}: {emoji_format}")
                print()
        
        await bot.close()
    
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Cancelled")
    except Exception as e:
        print(f"❌ Error: {e}")
