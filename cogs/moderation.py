import discord
from discord.ext import commands
from datetime import datetime, timedelta
from config import COLORS
from database import db

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.muted_users = {}

    # Mute Commands
    @commands.command(name='mute')
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: str = None, *, reason="No reason provided"):
        """Mute a member"""
        try:
            if duration:
                # Parse duration (e.g., "10m", "1h", "1d")
                time_amount = int(duration[:-1])
                time_unit = duration[-1]
                
                if time_unit == 'm':
                    delta = timedelta(minutes=time_amount)
                elif time_unit == 'h':
                    delta = timedelta(hours=time_amount)
                elif time_unit == 'd':
                    delta = timedelta(days=time_amount)
                else:
                    await ctx.send("❌ Invalid duration format. Use: 10m, 1h, 1d")
                    return
                
                await member.timeout(delta, reason=reason)
            else:
                await member.timeout(timedelta(hours=1), reason=reason)
            
            embed = discord.Embed(
                title="✅ Member Muted",
                description=f"{member.mention} has been muted",
                color=COLORS['success']
            )
            embed.add_field(name="Reason", value=reason)
            await ctx.send(embed=embed)
            
            # Log
            mod_logs_channel_id = await db.get_setting(ctx.guild.id, 'mod_logs_channel_id')
            if mod_logs_channel_id:
                log_channel = ctx.guild.get_channel(mod_logs_channel_id)
                if log_channel:
                    log_embed = discord.Embed(
                        title="Mute Logged",
                        description=f"{member.mention} muted by {ctx.author.mention}",
                        color=COLORS['warning'],
                        timestamp=datetime.now()
                    )
                    log_embed.add_field(name="Reason", value=reason)
                    await log_channel.send(embed=log_embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='unmute')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Unmute a member"""
        try:
            await member.timeout(None, reason=reason)
            embed = discord.Embed(
                title="✅ Member Unmuted",
                description=f"{member.mention} has been unmuted",
                color=COLORS['success']
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member"""
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="✅ Member Kicked",
                description=f"{member.mention} has been kicked",
                color=COLORS['success']
            )
            embed.add_field(name="Reason", value=reason)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member"""
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="✅ Member Banned",
                description=f"{member.mention} has been banned",
                color=COLORS['success']
            )
            embed.add_field(name="Reason", value=reason)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='softban')
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Softban a member (ban then unban)"""
        try:
            await member.ban(reason=f"Softban: {reason}")
            await ctx.guild.unban(member, reason=f"Softban: {reason}")
            embed = discord.Embed(
                title="✅ Member Softbanned",
                description=f"{member.mention} has been softbanned (message history deleted)",
                color=COLORS['success']
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason="No reason provided"):
        """Unban a user"""
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            embed = discord.Embed(
                title="✅ User Unbanned",
                description=f"{user.mention} has been unbanned",
                color=COLORS['success']
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    # Warning Commands
    @commands.command(name='warn')
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Warn a member"""
        await db.add_warning(ctx.guild.id, member.id, ctx.author.id, reason)
        embed = discord.Embed(
            title="⚠️ Warning Issued",
            description=f"{member.mention} has been warned",
            color=COLORS['warning']
        )
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.command(name='warnings')
    async def warnings(self, ctx, member: discord.Member = None):
        """Check warnings for a user"""
        target = member or ctx.author
        warnings = await db.get_user_warnings(ctx.guild.id, target.id)
        
        if not warnings:
            await ctx.send(f"✅ {target.mention} has no warnings")
            return
        
        embed = discord.Embed(
            title=f"Warnings for {target.name}",
            color=COLORS['warning']
        )
        for warn in warnings:
            embed.add_field(
                name=f"Warning ID: {warn[0]}",
                value=f"Reason: {warn[4]}\nDate: {warn[5]}",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(name='delwarn')
    @commands.has_permissions(moderate_members=True)
    async def delwarn(self, ctx, warn_id: int):
        """Delete a warning"""
        await db.delete_warning(warn_id)
        embed = discord.Embed(
            title="✅ Warning Deleted",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    # Purge Commands
    @commands.command(name='purge')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Purge messages"""
        deleted = await ctx.channel.purge(limit=amount)
        embed = discord.Embed(
            title="✅ Messages Purged",
            description=f"Deleted {len(deleted)} messages",
            color=COLORS['success']
        )
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name='purgetext')
    @commands.has_permissions(manage_messages=True)
    async def purge_text(self, ctx, text: str, amount: int = 50):
        """Purge messages containing specific text"""
        deleted = await ctx.channel.purge(
            limit=amount,
            check=lambda m: text.lower() in m.content.lower()
        )
        embed = discord.Embed(
            title="✅ Messages Purged",
            description=f"Deleted {len(deleted)} messages containing '{text}'",
            color=COLORS['success']
        )
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name='purgeuser')
    @commands.has_permissions(manage_messages=True)
    async def purge_user(self, ctx, member: discord.Member, amount: int = 50):
        """Purge messages from a specific user"""
        deleted = await ctx.channel.purge(
            limit=amount,
            check=lambda m: m.author == member
        )
        embed = discord.Embed(
            title="✅ Messages Purged",
            description=f"Deleted {len(deleted)} messages from {member.mention}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name='purgebots')
    @commands.has_permissions(manage_messages=True)
    async def purge_bots(self, ctx, amount: int = 50):
        """Purge bot messages"""
        deleted = await ctx.channel.purge(
            limit=amount,
            check=lambda m: m.author.bot
        )
        embed = discord.Embed(
            title="✅ Bot Messages Purged",
            description=f"Deleted {len(deleted)} bot messages",
            color=COLORS['success']
        )
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name='purgefiles')
    @commands.has_permissions(manage_messages=True)
    async def purge_files(self, ctx, amount: int = 50):
        """Purge messages with files/attachments"""
        deleted = await ctx.channel.purge(
            limit=amount,
            check=lambda m: len(m.attachments) > 0
        )
        embed = discord.Embed(
            title="✅ Messages With Files Purged",
            description=f"Deleted {len(deleted)} messages with attachments",
            color=COLORS['success']
        )
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name='purgelinks')
    @commands.has_permissions(manage_messages=True)
    async def purge_links(self, ctx, amount: int = 50):
        """Purge messages with links"""
        deleted = await ctx.channel.purge(
            limit=amount,
            check=lambda m: 'http' in m.content.lower()
        )
        embed = discord.Embed(
            title="✅ Messages With Links Purged",
            description=f"Deleted {len(deleted)} messages with links",
            color=COLORS['success']
        )
        await ctx.send(embed=embed, delete_after=5)

    # Lock/Unlock
    @commands.command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, *, reason="No reason provided"):
        """Lock the current channel"""
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(
            title="🔒 Channel Locked",
            description=f"Channel {ctx.channel.mention} has been locked",
            color=COLORS['warning']
        )
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, *, reason="No reason provided"):
        """Unlock the current channel"""
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(
            title="🔓 Channel Unlocked",
            description=f"Channel {ctx.channel.mention} has been unlocked",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    # Slowmode
    @commands.command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        """Set channel slowmode"""
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(
            title="✅ Slowmode Set",
            description=f"Slowmode set to {seconds} seconds",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    # Role Management
    @commands.command(name='addrole')
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, member: discord.Member, role: discord.Role):
        """Add a role to a member"""
        await member.add_roles(role)
        embed = discord.Embed(
            title="✅ Role Added",
            description=f"Added {role.mention} to {member.mention}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='removerole')
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, member: discord.Member, role: discord.Role):
        """Remove a role from a member"""
        await member.remove_roles(role)
        embed = discord.Embed(
            title="✅ Role Removed",
            description=f"Removed {role.mention} from {member.mention}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    # Prefix Command
    @commands.command(name='prefix')
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, new_prefix: str):
        """Change the bot prefix"""
        await db.set_setting(ctx.guild.id, 'prefix', new_prefix)
        embed = discord.Embed(
            title="✅ Prefix Changed",
            description=f"Prefix changed to `{new_prefix}`",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
