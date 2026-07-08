# Emoji Setup Guide

## 📋 Steps to Setup Custom Emojis

### Step 1: Extract Emoji IDs

Run this command to list all custom emojis your bot can see:

```bash
python emoji_setup.py
```

You'll see output like:
```
📍 Guild: Your Server Name (ID: 123456789)
------------------------------------------------------------
Name: success              | ID: 987654321
  Format: <:success:987654321>
  URL: https://cdn.discordapp.com/emojis/987654321.png
```

### Step 2: Update config.py

Open `config.py` and replace `YOUR_EMOJI_ID` with the actual IDs:

```python
EMOJIS = {
    'success': '<:success:987654321>',      # Replace with your ID
    'error': '<:error:987654322>',          # Replace with your ID
    # ... etc
}
```

### Step 3: Test the Emojis

Run the bot and check if emojis display correctly:

```bash
python main.py
```

Then try a command that uses emojis:
```
!help
!balance
!level
```

## 🎨 Emoji Categories

### System Emojis
- `success` - ✅ Success messages
- `error` - ❌ Error messages
- `warning` - ⚠️ Warning messages
- `info` - ℹ️ Info messages
- `loading` - ⏳ Loading states

### Moderation
- `mute` - Mute operations
- `kick` - Kick operations
- `ban` - Ban operations
- `warn` - Warning system
- `lock` / `unlock` - Channel locks
- `mod` - Moderation actions

### Economy & Levels
- `money` - Currency
- `bank` - Banking
- `coin` - Coins
- `leaderboard` - Leaderboards
- `levelup` - Level increases

### Fun
- `game` - Games
- `giveaway` - Giveaways
- `ticket` - Support tickets
- `afk` - AFK status

### Other
- `ai` - AI commands
- `help` - Help menu
- `settings` - Configuration
- `logs` - Logging

## 💡 Using Emojis in Code

### Method 1: Simple Emoji Get
```python
from config import get_emoji

emoji = get_emoji('success')
await ctx.send(f"{emoji} Success!")
```

### Method 2: Using Emoji Utils
```python
from utils import emoji_utils

# Create embed with emoji
embed = emoji_utils.create_success_embed(
    "Operation Complete",
    "Everything worked perfectly!"
)
await ctx.send(embed=embed)
```

### Method 3: In Embeds
```python
from config import get_emoji

embed = discord.Embed(title=f"{get_emoji('money')} Balance")
embed.add_field(name=f"{get_emoji('wallet')} Wallet", value="$100")
await ctx.send(embed=embed)
```

## ⚙️ Fallback System

If an emoji ID is invalid or not found, the bot automatically falls back to unicode emojis:

```python
# If this fails:
'success': '<:success:INVALID_ID>'

# It falls back to:
'success': '✅'
```

## 🔧 Troubleshooting

### Emojis not showing
1. Check the emoji ID is correct (use `emoji_setup.py`)
2. Ensure the bot can see the emoji (it's in a server the bot is in)
3. Check emoji format: `<:name:ID>` (no spaces)
4. Verify the emoji hasn't been deleted

### "Unknown Emoji" error
1. The emoji ID might be wrong
2. The bot might not have access to that emoji
3. Run `emoji_setup.py` again to verify IDs

### Custom emojis from nitro servers
If emojis are from a Nitro server, the bot must be in that server to use them.

## 📝 Quick Reference

```python
# Get emoji
get_emoji('success')  # Returns '<:success:ID>' or '✅'

# Create embeds with emojis
emoji_utils.create_success_embed(title, description)
emoji_utils.create_error_embed(title, description)
emoji_utils.create_warning_embed(title, description)

# Direct access
from config import EMOJIS
EMOJIS['success']  # Get raw emoji value
```

## 📚 Resources

- [How to get Emoji IDs](https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-use-unicode-emojis)
- [Discord Emoji API](https://discord.com/developers/docs/resources/emoji)
- [Unicode Emojis](https://unicode.org/emoji/charts/full-emoji-list.html)
