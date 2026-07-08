import discord
from discord.ext import commands
from config import COLORS
from datetime import datetime

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setmodlogs')
    @commands.has_permissions(administrator=True)
    async def set_mod_logs(self, ctx, channel: discord.TextChannel):
        """Set the mod logs channel"""
        from database import db
        await db.set_setting(ctx.guild.id, 'mod_logs_channel_id', channel.id)
        
        embed = discord.Embed(
            title="✅ Mod Logs Channel Set",
            description=f"Mod logs will be sent to {channel.mention}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='setchatlogs')
    @commands.has_permissions(administrator=True)
    async def set_chat_logs(self, ctx, channel: discord.TextChannel):
        """Set the chat logs channel"""
        from database import db
        await db.set_setting(ctx.guild.id, 'chat_logs_channel_id', channel.id)
        
        embed = discord.Embed(
            title="✅ Chat Logs Channel Set",
            description=f"Chat logs will be sent to {channel.mention}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='setuserlogs')
    @commands.has_permissions(administrator=True)
    async def set_user_logs(self, ctx, channel: discord.TextChannel):
        """Set the user logs channel"""
        from database import db
        await db.set_setting(ctx.guild.id, 'user_logs_channel_id', channel.id)
        
        embed = discord.Embed(
            title="✅ User Logs Channel Set",
            description=f"User logs will be sent to {channel.mention}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    # Message Delete Log
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Log deleted messages"""
        if message.author.bot:
            return
        
        from database import db
        chat_logs_channel_id = await db.get_setting(message.guild.id, 'chat_logs_channel_id')
        
        if not chat_logs_channel_id:
            return
        
        channel = self.bot.get_channel(chat_logs_channel_id)
        if not channel:
            return
        
        embed = discord.Embed(
            title="📛 Message Deleted",
            description=message.content[:1024] if message.content else "*[No content]*",
            color=0xFF0000,
            timestamp=datetime.now()
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar.url)
        embed.add_field(name="Channel", value=message.channel.mention)
        
        await channel.send(embed=embed)

    # Message Edit Log
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Log edited messages"""
        if before.author.bot:
            return
        
        if before.content == after.content:
            return
        
        from database import db
        chat_logs_channel_id = await db.get_setting(before.guild.id, 'chat_logs_channel_id')
        
        if not chat_logs_channel_id:
            return
        
        channel = self.bot.get_channel(chat_logs_channel_id)
        if not channel:
            return
        
        embed = discord.Embed(
            title="✏️ Message Edited",
            color=0xFFFF00,
            timestamp=datetime.now()
        )
        embed.set_author(name=before.author, icon_url=before.author.avatar.url)
        embed.add_field(name="Before", value=before.content[:1024] or "*[No content]*", inline=False)
        embed.add_field(name="After", value=after.content[:1024] or "*[No content]*", inline=False)
        embed.add_field(name="Channel", value=before.channel.mention)
        
        await channel.send(embed=embed)

    # Member Join Log
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Log member joins"""
        from database import db
        user_logs_channel_id = await db.get_setting(member.guild.id, 'user_logs_channel_id')
        
        if not user_logs_channel_id:
            return
        
        channel = self.bot.get_channel(user_logs_channel_id)
        if not channel:
            return
        
        embed = discord.Embed(
            title="✅ Member Joined",
            description=member.mention,
            color=0x00FF00,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at))
        
        await channel.send(embed=embed)

    # Member Leave Log
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Log member leaves"""
        from database import db
        user_logs_channel_id = await db.get_setting(member.guild.id, 'user_logs_channel_id')
        
        if not user_logs_channel_id:
            return
        
        channel = self.bot.get_channel(user_logs_channel_id)
        if not channel:
            return
        
        embed = discord.Embed(
            title="❌ Member Left",
            description=f"{member.name}#{member.discriminator}",
            color=0xFF0000,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Joined At", value=discord.utils.format_dt(member.joined_at))
        
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
