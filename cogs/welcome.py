import discord
from discord.ext import commands
from discord import app_commands
from config import COLORS
from database import db

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setwelcomechannel')
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        """Set the welcome channel"""
        await db.set_setting(ctx.guild.id, 'welcome_channel_id', channel.id)
        embed = discord.Embed(
            title="✅ Welcome Channel Set",
            description=f"Welcome channel set to {channel.mention}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='setwelcometext')
    @commands.has_permissions(administrator=True)
    async def set_welcome_text(self, ctx, *, text):
        """Set the welcome message text"""
        await db.set_setting(ctx.guild.id, 'welcome_text', text)
        embed = discord.Embed(
            title="✅ Welcome Text Set",
            description=f"Welcome text updated",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='setwelcomeimage')
    @commands.has_permissions(administrator=True)
    async def set_welcome_image(self, ctx, image_url: str):
        """Set the welcome message image"""
        await db.set_setting(ctx.guild.id, 'welcome_image_url', image_url)
        embed = discord.Embed(
            title="✅ Welcome Image Set",
            description=f"Welcome image updated",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='testwelcome')
    @commands.has_permissions(administrator=True)
    async def test_welcome(self, ctx):
        """Send a test welcome message"""
        welcome_text = await db.get_setting(ctx.guild.id, 'welcome_text')
        welcome_image = await db.get_setting(ctx.guild.id, 'welcome_image_url')
        
        embed = discord.Embed(
            title="Welcome!",
            description=welcome_text or f"Welcome to {ctx.guild.name}!",
            color=COLORS['info']
        )
        if welcome_image:
            embed.set_image(url=welcome_image)
        
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send welcome message when a member joins"""
        welcome_channel_id = await db.get_setting(member.guild.id, 'welcome_channel_id')
        welcome_text = await db.get_setting(member.guild.id, 'welcome_text')
        welcome_image = await db.get_setting(member.guild.id, 'welcome_image_url')
        
        if not welcome_channel_id:
            return
        
        channel = member.guild.get_channel(welcome_channel_id)
        if not channel:
            return
        
        embed = discord.Embed(
            title="Welcome!",
            description=welcome_text or f"Welcome {member.mention} to {member.guild.name}!",
            color=COLORS['info']
        )
        embed.set_thumbnail(url=member.avatar.url)
        if welcome_image:
            embed.set_image(url=welcome_image)
        
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
