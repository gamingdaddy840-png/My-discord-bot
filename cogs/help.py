import discord
from discord.ext import commands
from config import COLORS

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help_command(self, ctx, category=None):
        """Show help menu"""
        if not category:
            embed = discord.Embed(
                title="📖 Bot Help Menu",
                description="Use `!help <category>` to see commands for a category",
                color=COLORS['info']
            )
            embed.add_field(name="Categories", value="`welcome` `moderation` `afk` `giveaway` `tickets` `ai` `games` `logs` `extra` `economy` `leveling` `automod`")
            await ctx.send(embed=embed)
            return
        
        category = category.lower()
        
        helps = {
            'welcome': (
                "Welcome System",
                "`!setwelcomechannel <channel>` - Set welcome channel\n"
                "`!setwelcometext <text>` - Set welcome message\n"
                "`!setwelcomeimage <url>` - Set welcome image\n"
                "`!testwelcome` - Test welcome message"
            ),
            'moderation': (
                "Moderation",
                "`!mute @user [duration] [reason]` - Mute user\n"
                "`!unmute @user` - Unmute user\n"
                "`!kick @user [reason]` - Kick user\n"
                "`!ban @user [reason]` - Ban user\n"
                "`!warn @user [reason]` - Warn user\n"
                "`!warnings [@user]` - View warnings\n"
                "`!purge <amount>` - Purge messages\n"
                "`!lock [reason]` - Lock channel\n"
                "`!unlock [reason]` - Unlock channel\n"
                "`!prefix <prefix>` - Change prefix"
            ),
            'afk': (
                "AFK System",
                "`!afk [status]` - Set AFK\n"
                "`!unafk` - Remove AFK"
            ),
            'giveaway': (
                "Giveaways",
                "`!gstart <duration> <winners> <prize>` - Start giveaway\n"
                "`!gend <message_id>` - End giveaway\n"
                "`!greroll <message_id>` - Reroll giveaway"
            ),
            'tickets': (
                "Tickets",
                "`!ticketpanel` - Create ticket panel"
            ),
            'ai': (
                "AI Commands",
                "`!ask <question>` - Ask Gemini\n"
                "`!imagine <prompt>` - Image concept"
            ),
            'games': (
                "Games",
                "`!guessthenumber [max]` - Guess the number game"
            ),
            'logs': (
                "Logging",
                "`!setmodlogs <channel>` - Set mod logs\n"
                "`!setchatlogs <channel>` - Set chat logs\n"
                "`!setuserlogs <channel>` - Set user logs"
            ),
            'extra': (
                "Extra Features",
                "`!arset <trigger> <response>` - Auto responder\n"
                "`!arreact <trigger> <emoji>` - Auto reaction\n"
                "`!np give @user` - Give no prefix\n"
                "`!np remove @user` - Remove no prefix\n"
                "`!np list` - List no prefix users"
            ),
            'economy': (
                "Economy",
                "`!balance [@user]` - Check balance\n"
                "`!daily` - Daily reward\n"
                "`!deposit <amount>` - Deposit to bank\n"
                "`!withdraw <amount>` - Withdraw from bank\n"
                "`!leaderboard` - Economy leaderboard"
            ),
            'leveling': (
                "Leveling",
                "`!level [@user]` - Check level\n"
                "`!leaderboard` - Level leaderboard"
            ),
            'automod': (
                "Auto Moderation",
                "`!addbadword <word>` - Add bad word\n"
                "`!removebadword <word>` - Remove bad word"
            )
        }
        
        if category not in helps:
            embed = discord.Embed(
                title="❌ Category Not Found",
                description=f"Available: `welcome` `moderation` `afk` `giveaway` `tickets` `ai` `games` `logs` `extra` `economy` `leveling` `automod`",
                color=COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        title, content = helps[category]
        embed = discord.Embed(
            title=f"📖 {title}",
            description=content,
            color=COLORS['info']
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
