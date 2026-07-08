import discord
from discord.ext import commands
from datetime import datetime, timedelta
import random
from config import COLORS

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gstart')
    @commands.has_permissions(administrator=True)
    async def giveaway_start(self, ctx, duration: str, winners: int, *, prize):
        """Start a giveaway
        Usage: !gstart 1h 1 A Steam Gift Card
        """
        # Parse duration
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
        
        end_time = datetime.now() + delta
        
        embed = discord.Embed(
            title="🎉 GIVEAWAY 🎉",
            description=f"**Prize:** {prize}\n**Winners:** {winners}",
            color=COLORS['info']
        )
        embed.add_field(name="Ends In", value=f"<t:{int(end_time.timestamp())}:R>")
        embed.set_footer(text="React with 🎉 to enter!")
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('🎉')
        
        # Store giveaway data
        self.bot.giveaways = getattr(self.bot, 'giveaways', {})
        self.bot.giveaways[msg.id] = {
            'channel_id': ctx.channel.id,
            'message_id': msg.id,
            'prize': prize,
            'winners_count': winners,
            'end_time': end_time,
            'ended': False,
            'entries': []
        }

    @commands.command(name='gend')
    @commands.has_permissions(administrator=True)
    async def giveaway_end(self, ctx, message_id: int):
        """End a giveaway and pick winners"""
        giveaways = getattr(self.bot, 'giveaways', {})
        
        if message_id not in giveaways:
            await ctx.send("❌ Giveaway not found")
            return
        
        giveaway = giveaways[message_id]
        channel = self.bot.get_channel(giveaway['channel_id'])
        message = await channel.fetch_message(message_id)
        
        # Get all reactions
        entries = []
        for reaction in message.reactions:
            if str(reaction.emoji) == '🎉':
                async for user in reaction.users():
                    if not user.bot:
                        entries.append(user)
        
        if len(entries) < giveaway['winners_count']:
            embed = discord.Embed(
                title="❌ Giveaway Ended",
                description=f"Not enough entries. Minimum: {giveaway['winners_count']}, Got: {len(entries)}",
                color=COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        winners = random.sample(entries, giveaway['winners_count'])
        winners_mention = ", ".join([w.mention for w in winners])
        
        embed = discord.Embed(
            title="🎉 GIVEAWAY ENDED 🎉",
            description=f"**Prize:** {giveaway['prize']}\n**Winners:** {winners_mention}",
            color=COLORS['success']
        )
        embed.add_field(name="Total Entries", value=len(entries))
        await ctx.send(embed=embed)
        
        giveaway['ended'] = True

    @commands.command(name='greroll')
    @commands.has_permissions(administrator=True)
    async def giveaway_reroll(self, ctx, message_id: int):
        """Reroll a giveaway"""
        giveaways = getattr(self.bot, 'giveaways', {})
        
        if message_id not in giveaways:
            await ctx.send("❌ Giveaway not found")
            return
        
        giveaway = giveaways[message_id]
        channel = self.bot.get_channel(giveaway['channel_id'])
        message = await channel.fetch_message(message_id)
        
        # Get all reactions
        entries = []
        for reaction in message.reactions:
            if str(reaction.emoji) == '🎉':
                async for user in reaction.users():
                    if not user.bot:
                        entries.append(user)
        
        if not entries:
            await ctx.send("❌ No entries found")
            return
        
        winners = random.sample(entries, min(giveaway['winners_count'], len(entries)))
        winners_mention = ", ".join([w.mention for w in winners])
        
        embed = discord.Embed(
            title="🎉 GIVEAWAY REROLLED 🎉",
            description=f"**Prize:** {giveaway['prize']}\n**New Winners:** {winners_mention}",
            color=COLORS['info']
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
