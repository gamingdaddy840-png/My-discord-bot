import discord
from discord.ext import commands
from discord import app_commands
from config import COLORS
from datetime import datetime

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_messages = {}

    @commands.command(name='ticketpanel')
    @commands.has_permissions(administrator=True)
    async def ticket_panel(self, ctx):
        """Create a ticket help panel"""
        embed = discord.Embed(
            title="🎫 Support Ticket System",
            description="Click the button below to create a support ticket",
            color=COLORS['info']
        )
        
        view = TicketPanelView(self.bot)
        msg = await ctx.send(embed=embed, view=view)
        self.ticket_messages[msg.id] = msg

class TicketPanelView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.blurple, emoji="🎫")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Create a ticket for the user"""
        guild = interaction.guild
        
        # Create ticket channel
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category(name="Tickets")
        
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            topic=f"Ticket created by {interaction.user.mention}"
        )
        
        # Set permissions
        await channel.set_permissions(
            interaction.user,
            read_messages=True,
            send_messages=True
        )
        
        await channel.set_permissions(
            guild.default_role,
            read_messages=False
        )
        
        # Send ticket message
        embed = discord.Embed(
            title="Support Ticket",
            description=f"Thank you for creating a ticket, {interaction.user.mention}!",
            color=COLORS['info']
        )
        embed.add_field(name="Created At", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        view = TicketActionView(self.bot, channel)
        await channel.send(embed=embed, view=view)
        
        await interaction.response.send_message(
            f"✅ Ticket created: {channel.mention}",
            ephemeral=True
        )

class TicketActionView(discord.ui.View):
    def __init__(self, bot, channel):
        super().__init__()
        self.bot = bot
        self.channel = channel

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Close the ticket"""
        await self.channel.delete()
        await interaction.response.send_message(
            "✅ Ticket closed",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Tickets(bot))
