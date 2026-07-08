import discord
from discord.ext import commands, tasks
import os
from config import DISCORD_TOKEN, DEFAULT_PREFIX
from database import db
import asyncio

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.moderation = True

class CustomBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self.get_prefix,
            intents=intents,
            help_command=None
        )
        self.db = db

    async def get_prefix(self, message):
        """Get the prefix for a guild"""
        if not message.guild:
            return DEFAULT_PREFIX
        
        prefix = await self.db.get_setting(message.guild.id, 'prefix')
        return prefix or DEFAULT_PREFIX

bot = CustomBot()

# Load Cogs
async def load_cogs():
    cogs_dir = 'cogs'
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"✅ Loaded {filename}")

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    print(f"📊 Bot is in {len(bot.guilds)} servers")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{DEFAULT_PREFIX}help"
    ))
    check_mutes.start()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # AFK Check
    if message.guild:
        # Remove AFK status if user is no longer AFK
        pass
    
    await bot.process_commands(message)

@tasks.loop(minutes=1)
async def check_mutes():
    """Check and remove expired mutes"""
    pass

async def main():
    async with bot:
        # Initialize database
        await db.init_db()
        
        # Load cogs
        await load_cogs()
        
        # Run bot
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
