import discord
from discord.ext import commands
from config import COLORS

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='balance')
    async def balance(self, ctx, member: discord.Member = None):
        """Check user balance"""
        target = member or ctx.author
        
        async with self.bot.db.db.execute(
            "SELECT balance, bank FROM economy WHERE user_id = ? AND guild_id = ?",
            (target.id, ctx.guild.id)
        ) as cursor:
            row = await cursor.fetchone()
            balance = row[0] if row else 0
            bank = row[1] if row else 0
        
        embed = discord.Embed(
            title=f"💰 {target.name}'s Balance",
            color=COLORS['info']
        )
        embed.add_field(name="Wallet", value=f"${balance}", inline=True)
        embed.add_field(name="Bank", value=f"${bank}", inline=True)
        embed.add_field(name="Total", value=f"${balance + bank}", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name='daily')
    async def daily(self, ctx):
        """Claim daily reward"""
        daily_amount = 100
        
        async with self.bot.db.db.execute(
            "SELECT balance FROM economy WHERE user_id = ? AND guild_id = ?",
            (ctx.author.id, ctx.guild.id)
        ) as cursor:
            row = await cursor.fetchone()
        
        if row:
            new_balance = row[0] + daily_amount
            await self.bot.db.db.execute(
                "UPDATE economy SET balance = ? WHERE user_id = ? AND guild_id = ?",
                (new_balance, ctx.author.id, ctx.guild.id)
            )
        else:
            await self.bot.db.db.execute(
                "INSERT INTO economy (user_id, guild_id, balance) VALUES (?, ?, ?)",
                (ctx.author.id, ctx.guild.id, daily_amount)
            )
        
        await self.bot.db.db.commit()
        
        embed = discord.Embed(
            title="✅ Daily Reward",
            description=f"You received ${daily_amount}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='deposit')
    async def deposit(self, ctx, amount: int):
        """Deposit money to bank"""
        async with self.bot.db.db.execute(
            "SELECT balance, bank FROM economy WHERE user_id = ? AND guild_id = ?",
            (ctx.author.id, ctx.guild.id)
        ) as cursor:
            row = await cursor.fetchone()
            balance = row[0] if row else 0
            bank = row[1] if row else 0
        
        if balance < amount:
            embed = discord.Embed(
                title="❌ Insufficient Funds",
                color=COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        new_balance = balance - amount
        new_bank = bank + amount
        
        if row:
            await self.bot.db.db.execute(
                "UPDATE economy SET balance = ?, bank = ? WHERE user_id = ? AND guild_id = ?",
                (new_balance, new_bank, ctx.author.id, ctx.guild.id)
            )
        else:
            await self.bot.db.db.execute(
                "INSERT INTO economy (user_id, guild_id, balance, bank) VALUES (?, ?, ?, ?)",
                (ctx.author.id, ctx.guild.id, new_balance, new_bank)
            )
        
        await self.bot.db.db.commit()
        
        embed = discord.Embed(
            title="✅ Deposited",
            description=f"Deposited ${amount}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='withdraw')
    async def withdraw(self, ctx, amount: int):
        """Withdraw money from bank"""
        async with self.bot.db.db.execute(
            "SELECT balance, bank FROM economy WHERE user_id = ? AND guild_id = ?",
            (ctx.author.id, ctx.guild.id)
        ) as cursor:
            row = await cursor.fetchone()
            balance = row[0] if row else 0
            bank = row[1] if row else 0
        
        if bank < amount:
            embed = discord.Embed(
                title="❌ Insufficient Bank Funds",
                color=COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        new_balance = balance + amount
        new_bank = bank - amount
        
        if row:
            await self.bot.db.db.execute(
                "UPDATE economy SET balance = ?, bank = ? WHERE user_id = ? AND guild_id = ?",
                (new_balance, new_bank, ctx.author.id, ctx.guild.id)
            )
        else:
            await self.bot.db.db.execute(
                "INSERT INTO economy (user_id, guild_id, balance, bank) VALUES (?, ?, ?, ?)",
                (ctx.author.id, ctx.guild.id, new_balance, new_bank)
            )
        
        await self.bot.db.db.commit()
        
        embed = discord.Embed(
            title="✅ Withdrawn",
            description=f"Withdrawn ${amount}",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        """Show economy leaderboard"""
        async with self.bot.db.db.execute(
            "SELECT user_id, balance, bank FROM economy WHERE guild_id = ? ORDER BY (balance + bank) DESC LIMIT 10",
            (ctx.guild.id,)
        ) as cursor:
            rows = await cursor.fetchall()
        
        if not rows:
            embed = discord.Embed(
                title="💰 Economy Leaderboard",
                description="No users yet",
                color=COLORS['info']
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="💰 Economy Leaderboard",
            color=COLORS['info']
        )
        
        for i, (user_id, balance, bank) in enumerate(rows, 1):
            user = await self.bot.fetch_user(user_id)
            total = balance + bank
            embed.add_field(
                name=f"#{i} {user.name}",
                value=f"💵 ${total}",
                inline=False
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
