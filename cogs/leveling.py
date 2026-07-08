import discord
from discord.ext import commands
from config import COLORS

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_per_message = 10

    @commands.Cog.listener()
    async def on_message(self, message):
        """Give XP on message"""
        if message.author.bot:
            return
        
        if not message.guild:
            return
        
        # Add XP
        async with self.bot.db.db.execute(
            "SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?",
            (message.author.id, message.guild.id)
        ) as cursor:
            row = await cursor.fetchone()
        
        if row:
            current_xp = row[0]
            current_level = row[1]
        else:
            current_xp = 0
            current_level = 1
        
        new_xp = current_xp + self.xp_per_message
        xp_needed = current_level * 100
        
        if new_xp >= xp_needed:
            new_level = current_level + 1
            new_xp = 0
            
            if row:
                await self.bot.db.db.execute(
                    "UPDATE levels SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?",
                    (new_xp, new_level, message.author.id, message.guild.id)
                )
            else:
                await self.bot.db.db.execute(
                    "INSERT INTO levels (user_id, guild_id, xp, level) VALUES (?, ?, ?, ?)",
                    (message.author.id, message.guild.id, new_xp, new_level)
                )
            
            await self.bot.db.db.commit()
            
            embed = discord.Embed(
                title="📈 Level Up!",
                description=f"{message.author.mention} reached level {new_level}!",
                color=COLORS['success']
            )
            await message.reply(embed=embed)
        else:
            if row:
                await self.bot.db.db.execute(
                    "UPDATE levels SET xp = ? WHERE user_id = ? AND guild_id = ?",
                    (new_xp, message.author.id, message.guild.id)
                )
            else:
                await self.bot.db.db.execute(
                    "INSERT INTO levels (user_id, guild_id, xp, level) VALUES (?, ?, ?, ?)",
                    (message.author.id, message.guild.id, new_xp, 1)
                )
            
            await self.bot.db.db.commit()

    @commands.command(name='level')
    async def level(self, ctx, member: discord.Member = None):
        """Check user level"""
        target = member or ctx.author
        
        async with self.bot.db.db.execute(
            "SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?",
            (target.id, ctx.guild.id)
        ) as cursor:
            row = await cursor.fetchone()
        
        if not row:
            xp = 0
            level = 1
        else:
            xp = row[0]
            level = row[1]
        
        xp_needed = level * 100
        xp_percent = (xp / xp_needed) * 100
        
        embed = discord.Embed(
            title=f"📈 {target.name}'s Level",
            color=COLORS['info']
        )
        embed.add_field(name="Level", value=level, inline=True)
        embed.add_field(name="XP", value=f"{xp}/{xp_needed}", inline=True)
        embed.add_field(name="Progress", value=f"{'█' * int(xp_percent / 10)}{'░' * (10 - int(xp_percent / 10))} {int(xp_percent)}%", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        """Show level leaderboard"""
        async with self.bot.db.db.execute(
            "SELECT user_id, level, xp FROM levels WHERE guild_id = ? ORDER BY level DESC, xp DESC LIMIT 10",
            (ctx.guild.id,)
        ) as cursor:
            rows = await cursor.fetchall()
        
        if not rows:
            embed = discord.Embed(
                title="📈 Level Leaderboard",
                description="No users yet",
                color=COLORS['info']
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="📈 Level Leaderboard",
            color=COLORS['info']
        )
        
        for i, (user_id, level, xp) in enumerate(rows, 1):
            user = await self.bot.fetch_user(user_id)
            embed.add_field(
                name=f"#{i} {user.name}",
                value=f"Level {level} | {xp} XP",
                inline=False
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leveling(bot))
