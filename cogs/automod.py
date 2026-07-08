import discord
from discord.ext import commands
from config import COLORS
from database import db

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bad_words = [
            "badword1", "badword2", "badword3"  # Add your bad words here
        ]
        self.phishing_sites = [
            "bit.ly", "tinyurl", "discord.gg", "discordapp.com"
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        """Auto moderation checks"""
        if message.author.bot:
            return
        
        if not message.guild:
            return
        
        content = message.content.lower()
        
        # All Caps Check
        if len(content) > 5 and content.isupper():
            try:
                await message.delete()
                embed = discord.Embed(
                    title="🚫 Auto Moderation",
                    description="Your message was deleted for using too many capitals",
                    color=COLORS['warning']
                )
                await message.author.send(embed=embed)
            except:
                pass
            return
        
        # Bad Words Check
        for word in self.bad_words:
            if word in content:
                try:
                    await message.delete()
                    embed = discord.Embed(
                        title="🚫 Auto Moderation",
                        description="Your message was deleted for containing banned words",
                        color=COLORS['warning']
                    )
                    await message.author.send(embed=embed)
                except:
                    pass
                return
        
        # Duplicate Text Check
        if len(content) > 10:
            char_ratio = len(set(content)) / len(content)
            if char_ratio < 0.1:  # Less than 10% unique characters
                try:
                    await message.delete()
                    embed = discord.Embed(
                        title="🚫 Auto Moderation",
                        description="Your message was deleted for duplicate text spam",
                        color=COLORS['warning']
                    )
                    await message.author.send(embed=embed)
                except:
                    pass
                return
        
        # Emoji Spam Check
        emoji_count = sum(1 for c in message.content if ord(c) > 0x1F300)
        if emoji_count > 10:
            try:
                await message.delete()
                embed = discord.Embed(
                    title="🚫 Auto Moderation",
                    description="Your message was deleted for emoji spam",
                    color=COLORS['warning']
                )
                await message.author.send(embed=embed)
            except:
                pass
            return
        
        # Mass Mentions Check
        mention_count = len(message.mentions) + len(message.role_mentions)
        if mention_count > 5:
            try:
                await message.delete()
                embed = discord.Embed(
                    title="🚫 Auto Moderation",
                    description="Your message was deleted for mass mentions",
                    color=COLORS['warning']
                )
                await message.author.send(embed=embed)
            except:
                pass
            return
        
        # Invite Links Check
        if "discord.gg/" in content or "discord.com/invite/" in content:
            try:
                await message.delete()
                embed = discord.Embed(
                    title="🚫 Auto Moderation",
                    description="Your message was deleted for containing invite links",
                    color=COLORS['warning']
                )
                await message.author.send(embed=embed)
            except:
                pass
            return
        
        # Links Check (general)
        if "http" in content or "www." in content:
            for phishing_site in self.phishing_sites:
                if phishing_site in content:
                    try:
                        await message.delete()
                        embed = discord.Embed(
                            title="🚫 Auto Moderation",
                            description="Your message was deleted for containing suspicious links",
                            color=COLORS['warning']
                        )
                        await message.author.send(embed=embed)
                    except:
                        pass
                    return

    @commands.command(name='addbadword')
    @commands.has_permissions(administrator=True)
    async def add_bad_word(self, ctx, word: str):
        """Add a word to the bad words list"""
        self.bad_words.append(word.lower())
        embed = discord.Embed(
            title="✅ Bad Word Added",
            description=f"'{word}' added to bad words list",
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='removebadword')
    @commands.has_permissions(administrator=True)
    async def remove_bad_word(self, ctx, word: str):
        """Remove a word from the bad words list"""
        if word.lower() in self.bad_words:
            self.bad_words.remove(word.lower())
            embed = discord.Embed(
                title="✅ Bad Word Removed",
                description=f"'{word}' removed from bad words list",
                color=COLORS['success']
            )
        else:
            embed = discord.Embed(
                title="❌ Not Found",
                description=f"'{word}' not in bad words list",
                color=COLORS['error']
            )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
