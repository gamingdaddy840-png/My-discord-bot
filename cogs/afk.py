import discord
from discord.ext import commands
from datetime import datetime
from config import COLORS
from database import db

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}

    @commands.command(name='afk')
    async def set_afk(self, ctx, *, status="AFK"):
        """Set AFK status"""
        self.afk_users[ctx.author.id] = {
            'status': status,
            'timestamp': datetime.now(),
            'guild_id': ctx.guild.id
        }
        
        embed = discord.Embed(
            title="✅ AFK Set",
            description=f"You are now AFK: {status}",
            color=COLORS['info']
        )
        await ctx.send(embed=embed)

    @commands.command(name='unafk')
    async def unafk(self, ctx):
        """Remove AFK status"""
        if ctx.author.id in self.afk_users:
            del self.afk_users[ctx.author.id]
            embed = discord.Embed(
                title="✅ AFK Removed",
                description="You are no longer AFK",
                color=COLORS['success']
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Not AFK",
                description="You were not AFK",
                color=COLORS['error']
            )
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Check for AFK mentions"""
        if message.author.bot:
            return
        
        # Remove AFK if user types
        if message.author.id in self.afk_users:
            del self.afk_users[message.author.id]
            await message.reply("✅ Welcome back! AFK status removed.")
        
        # Check for mentions of AFK users
        for mention in message.mentions:
            if mention.id in self.afk_users:
                afk_data = self.afk_users[mention.id]
                embed = discord.Embed(
                    title="👤 User is AFK",
                    description=f"{mention.mention} is currently AFK\n**Status:** {afk_data['status']}",
                    color=COLORS['info']
                )
                await message.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(AFK(bot))
