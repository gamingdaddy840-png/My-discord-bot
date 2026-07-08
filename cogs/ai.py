import discord
from discord.ext import commands
from config import COLORS, GEMINI_API_KEY
import google.generativeai as genai

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    @commands.command(name='ask')
    async def ask_gemini(self, ctx, *, question):
        """Ask Gemini AI a question"""
        async with ctx.typing():
            try:
                response = self.model.generate_content(question)
                
                if len(response.text) > 2000:
                    # Split into multiple messages
                    chunks = [response.text[i:i+2000] for i in range(0, len(response.text), 2000)]
                    embed = discord.Embed(
                        title="🤖 Gemini Response",
                        description=chunks[0],
                        color=COLORS['info']
                    )
                    await ctx.send(embed=embed)
                    for chunk in chunks[1:]:
                        embed = discord.Embed(
                            description=chunk,
                            color=COLORS['info']
                        )
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="🤖 Gemini Response",
                        description=response.text,
                        color=COLORS['info']
                    )
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Error communicating with Gemini: {str(e)}",
                    color=COLORS['error']
                )
                await ctx.send(embed=embed)

    @commands.command(name='imagine')
    async def imagine(self, ctx, *, prompt):
        """Generate an image description using Gemini"""
        async with ctx.typing():
            try:
                response = self.model.generate_content(f"Describe this image concept and give details as if you're seeing it: {prompt}")
                
                embed = discord.Embed(
                    title="🎨 Image Concept",
                    description=response.text[:2000],
                    color=COLORS['info']
                )
                await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Error: {str(e)}",
                    color=COLORS['error']
                )
                await ctx.send(embed=embed)

async def setup(bot):
    if GEMINI_API_KEY:
        await bot.add_cog(AI(bot))
    else:
        print("⚠️ GEMINI_API_KEY not set, skipping AI cog")
