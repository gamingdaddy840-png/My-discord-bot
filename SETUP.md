# Discord Bot Setup Guide

## 📋 Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Gemini API Key (optional, for AI features)

## 🚀 Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/gamingdaddy840-png/My-discord-bot.git
cd My-discord-bot
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:
```
DISCORD_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

#### Getting a Discord Bot Token:
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" tab and click "Add Bot"
4. Copy the token under "TOKEN"
5. Enable necessary Intents:
   - Message Content Intent
   - Server Members Intent
   - Guild Members Intent

#### Getting Gemini API Key (Optional):
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key"
3. Copy your API key

### 5. Run the Bot
```bash
python main.py
```

You should see:
```
✅ Bot logged in as [BotName]
📊 Bot is in X servers
✅ Loaded welcome.py
✅ Loaded moderation.py
... (more cogs)
```

## 📁 Project Structure

```
My-discord-bot/
├── main.py                 # Main bot file
├── config.py              # Configuration settings
├── database.py            # Database initialization
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore file
├── README.md             # Bot documentation
├── SETUP.md              # This file
└── cogs/                 # Command modules
    ├── __init__.py
    ├── welcome.py        # Welcome system
    ├── moderation.py     # Moderation commands
    ├── afk.py            # AFK system
    ├── giveaway.py       # Giveaway system
    ├── tickets.py        # Ticket system
    ├── games.py          # Games
    ├── ai.py             # AI commands
    ├── logs.py           # Logging system
    ├── extra.py          # Extra features
    ├── automod.py        # Auto moderation
    ├── economy.py        # Economy system
    ├── leveling.py       # Leveling system
    └── help.py           # Help command
```

## 🎮 Quick Start Commands

### Admin Setup
```
!setwelcomechannel #welcome        # Set welcome channel
!setchatlogs #logs                 # Set chat logs
!setmodlogs #mod-logs              # Set mod logs
!setuserlogs #user-logs            # Set user logs
!prefix !                           # Set prefix (default is !)
!ticketpanel                       # Create ticket panel
```

### User Commands
```
!help                              # Show help menu
!afk Working on something          # Set AFK status
!guessthenumber 100               # Start guessing game
!balance                          # Check your balance
!level                            # Check your level
!ask What is Python?              # Ask Gemini AI
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
DEFAULT_PREFIX = '!'              # Bot prefix
WARN_TIMEOUT = 30                # Days before warnings expire
COLORS = {...}                   # Embed colors
```

## 🗄️ Database

The bot automatically creates `bot_data.db` with all necessary tables:
- Guild Settings
- Warnings
- Mutes
- AutoMod Settings
- AFK Status
- Giveaways
- Tickets
- Economy
- Levels
- And more...

## 🐛 Troubleshooting

### Bot doesn't start
- Check if `DISCORD_TOKEN` is set correctly in `.env`
- Ensure all intents are enabled in Developer Portal
- Check Python version (3.8+)

### Commands not working
- Ensure bot has proper permissions
- Check channel permissions
- Verify bot role is above command user's roles (for moderation)

### Database errors
- Delete `bot_data.db` and restart bot
- Ensure write permissions in bot directory

### Missing modules
- Run `pip install -r requirements.txt` again
- Use `pip install --upgrade discord.py`

## 📝 Adding Custom Commands

Create a new file in `cogs/` folder:

```python
import discord
from discord.ext import commands

class MyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mycommand')
    async def my_command(self, ctx):
        """My custom command"""
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(MyCommands(bot))
```

Restart the bot and your command will be loaded automatically!

## 🔒 Permissions

Bot requires these permissions:
- ✅ Read Messages/View Channels
- ✅ Send Messages
- ✅ Embed Links
- ✅ Attach Files
- ✅ Read Message History
- ✅ Mention @everyone, @here, and All Roles
- ✅ Manage Messages
- ✅ Manage Channels
- ✅ Manage Roles
- ✅ Ban Members
- ✅ Kick Members
- ✅ Timeout Members
- ✅ Manage Nicknames

## 📚 Documentation

- [Discord.py Docs](https://discordpy.readthedocs.io/)
- [Discord API Docs](https://discord.com/developers/docs/intro)
- [Google Generative AI Docs](https://ai.google.dev/)

## 💡 Tips & Best Practices

1. **Always use async/await** - Discord.py is async
2. **Use embeds** - More professional than plain text
3. **Add error handling** - Use try/except blocks
4. **Check permissions** - Use `@commands.has_permissions()`
5. **Keep bot responsive** - Avoid blocking operations

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review bot logs for errors
3. Check Discord.py documentation
4. Create an issue on GitHub

## 📄 License

MIT License - Feel free to use and modify!

---

**Made with ❤️ by Friday**
