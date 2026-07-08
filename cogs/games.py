import discord
from discord.ext import commands
from config import COLORS
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guessing_games = {}

    @commands.command(name='guessthenumber')
    async def guess_the_number(self, ctx, max_number: int = 100):
        """Start a guess the number game
        Usage: !guessthenumber 100
        """
        
        # Generate random number
        secret_number = random.randint(1, max_number)
        
        embed = discord.Embed(
            title="🎮 Guess The Number Game",
            description=f"I'm thinking of a number between 1 and {max_number}\nCheck your DMs to start playing!",
            color=COLORS['info']
        )
        
        await ctx.send(embed=embed)
        
        # Send DM to user
        try:
            dm_embed = discord.Embed(
                title="🎮 Guess The Number",
                description=f"A number has been chosen between 1 and {max_number}\n\nClick the button below to start guessing!",
                color=COLORS['info']
            )
            
            view = GuessGameView(self.bot, ctx.author, secret_number, max_number, ctx.channel)
            await ctx.author.send(embed=dm_embed, view=view)
        except:
            await ctx.send("❌ Could not send DM. Make sure DMs are enabled.")

class GuessGameView(discord.ui.View):
    def __init__(self, bot, user, secret_number, max_number, channel):
        super().__init__()
        self.bot = bot
        self.user = user
        self.secret_number = secret_number
        self.max_number = max_number
        self.channel = channel
        self.guesses = []
        self.game_active = False

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.green)
    async def start_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Start the game"""
        if interaction.user != self.user:
            await interaction.response.send_message("❌ This game is not for you", ephemeral=True)
            return
        
        self.game_active = True
        
        embed = discord.Embed(
            title="🎮 Guess The Number - Started",
            description=f"The game has started! I'm thinking of a number between 1 and {self.max_number}",
            color=COLORS['info']
        )
        
        view = GuessInputView(self.bot, self.user, self.secret_number, self.max_number, self.channel, self.guesses)
        await interaction.response.send_message(embed=embed, view=view)

class GuessInputView(discord.ui.View):
    def __init__(self, bot, user, secret_number, max_number, channel, guesses):
        super().__init__()
        self.bot = bot
        self.user = user
        self.secret_number = secret_number
        self.max_number = max_number
        self.channel = channel
        self.guesses = guesses

    @discord.ui.button(label="Make a Guess", style=discord.ButtonStyle.blurple)
    async def make_guess(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Open modal to input guess"""
        if interaction.user != self.user:
            await interaction.response.send_message("❌ This game is not for you", ephemeral=True)
            return
        
        modal = GuessModal(self.secret_number, self.max_number, self.channel, self.guesses)
        await interaction.response.send_modal(modal)

class GuessModal(discord.ui.Modal, title="Guess the Number"):
    number = discord.ui.TextInput(label="Your Guess", placeholder="Enter a number...")

    def __init__(self, secret_number, max_number, channel, guesses):
        super().__init__()
        self.secret_number = secret_number
        self.max_number = max_number
        self.channel = channel
        self.guesses = guesses

    async def on_submit(self, interaction: discord.Interaction):
        try:
            guess = int(self.number.value)
            
            if guess < 1 or guess > self.max_number:
                await interaction.response.send_message(
                    f"❌ Number must be between 1 and {self.max_number}",
                    ephemeral=True
                )
                return
            
            self.guesses.append(guess)
            
            if guess == self.secret_number:
                embed = discord.Embed(
                    title="🎉 Correct!",
                    description=f"You guessed the number in {len(self.guesses)} attempts!",
                    color=COLORS['success']
                )
                embed.add_field(name="Number", value=self.secret_number)
                embed.add_field(name="Attempts", value=len(self.guesses))
                
                # React to channel message
                await self.channel.send(f"✅ {interaction.user.mention} guessed correctly!")
                
                await interaction.response.send_message(embed=embed)
                
            elif guess < self.secret_number:
                embed = discord.Embed(
                    title="📈 Too Low",
                    description=f"Your guess ({guess}) is too low!\nAttempts: {len(self.guesses)}",
                    color=COLORS['info']
                )
                await interaction.response.send_message(embed=embed)
                
            else:
                embed = discord.Embed(
                    title="📉 Too High",
                    description=f"Your guess ({guess}) is too high!\nAttempts: {len(self.guesses)}",
                    color=COLORS['info']
                )
                await interaction.response.send_message(embed=embed)
        
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid number", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Games(bot))
