import discord
from discord.ext import commands
from config import COLORS
from database import db
from datetime import datetime

class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Auto Responder
    @commands.command(name='arset')
    @commands.has_permissions(administrator=True)
    async def autoresponder_set(self, ctx, trigger: str, *, response: str):
        """Set an auto responder"""
        async with self.bot.db.db.execute(
            "INSERT INTO auto_responder (guild_id, trigger, response) VALUES (?, ?, ?)",
            (ctx.guild.id, trigger.lower(), response)
        ) as cursor:
            pass
        await self.bot.db.db.commit()
        
        embed = discord.Embed(
            title="✅ Auto Responder Set",
            description=f"Trigger: `{trigger}`",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='arremove')
    @commands.has_permissions(administrator=True)
    async def autoresponder_remove(self, ctx, trigger: str):
        """Remove an auto responder"""
        async with self.bot.db.db.execute(
            "DELETE FROM auto_responder WHERE guild_id = ? AND trigger = ?",
            (ctx.guild.id, trigger.lower())
        ):
            pass
        await self.bot.db.db.commit()
        
        embed = discord.Embed(
            title="✅ Auto Responder Removed",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Check for auto responder triggers"""
        if message.author.bot:
            return
        
        if not message.guild:
            return
        
        async with self.bot.db.db.execute(
            "SELECT response FROM auto_responder WHERE guild_id = ? AND trigger = ?",
            (message.guild.id, message.content.lower())
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                embed = discord.Embed(
                    description=row[0],
                    color=COLORS['info']
                )
                await message.reply(embed=embed)

    # Auto Reaction
    @commands.command(name='arreact')
    @commands.has_permissions(administrator=True)
    async def autoreaction_set(self, ctx, trigger: str, emoji):
        """Set an auto reaction"""
        async with self.bot.db.db.execute(
            "INSERT INTO auto_reaction (guild_id, trigger, emoji) VALUES (?, ?, ?)",
            (ctx.guild.id, trigger.lower(), str(emoji))
        ):
            pass
        await self.bot.db.db.commit()
        
        embed = discord.Embed(
            title="✅ Auto Reaction Set",
            description=f"Trigger: `{trigger}` -> {emoji}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    # No Prefix
    @commands.command(name='np')
    @commands.has_permissions(administrator=True)
    async def no_prefix(self, ctx, action: str, member: discord.Member = None):
        """Manage no prefix users
        Usage: !np give @user - Give no prefix access
        Usage: !np remove @user - Remove no prefix access
        Usage: !np list - List all no prefix users
        """
        if action.lower() == 'give':
            if not member:
                await ctx.send("❌ Please specify a member")
                return
            
            async with self.bot.db.db.execute(
                "INSERT OR IGNORE INTO no_prefix_users (user_id, guild_id) VALUES (?, ?)",
                (member.id, ctx.guild.id)
            ):
                pass
            await self.bot.db.db.commit()
            
            embed = discord.Embed(
                title="✅ No Prefix Access Given",
                description=f"Granted to {member.mention}",
                color=COLORS['success']
            )
            await ctx.send(embed=embed)
        
        elif action.lower() == 'remove':
            if not member:
                await ctx.send("❌ Please specify a member")
                return
            
            async with self.bot.db.db.execute(
                "DELETE FROM no_prefix_users WHERE user_id = ? AND guild_id = ?",
                (member.id, ctx.guild.id)
            ):
                pass
            await self.bot.db.db.commit()
            
            embed = discord.Embed(
                title="✅ No Prefix Access Removed",
                description=f"Removed from {member.mention}",
                color=COLORS['success']
            )
            await ctx.send(embed=embed)
        
        elif action.lower() == 'list':
            async with self.bot.db.db.execute(
                "SELECT user_id FROM no_prefix_users WHERE guild_id = ?",
                (ctx.guild.id,)
            ) as cursor:
                users = await cursor.fetchall()
            
            if not users:
                embed = discord.Embed(
                    title="📋 No Prefix Users",
                    description="No users with no prefix access",
                    color=COLORS['info']
                )
            else:
                user_list = "\n".join([f"<@{u[0]}>" for u in users])
                embed = discord.Embed(
                    title="📋 No Prefix Users",
                    description=user_list,
                    color=COLORS['info']
                )
            
            await ctx.send(embed=embed)

    # Auto Role Assign
    @commands.command(name='autorole')
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role):
        """Set auto role assignment on join"""
        await db.set_setting(ctx.guild.id, 'auto_role_id', role.id)
        
        embed = discord.Embed(
            title="✅ Auto Role Set",
            description=f"New members will get {role.mention}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Auto assign role on member join"""
        # This is handled by welcome cog but can be extended here
        pass

async def setup(bot):
    await bot.add_cog(Extra(bot))
