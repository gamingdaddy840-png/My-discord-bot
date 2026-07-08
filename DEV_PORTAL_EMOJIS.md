# Developer Portal Emojis Setup Guide

## 📋 What are Developer Portal Emojis?

Developer Portal emojis are custom emojis uploaded directly to your bot's application in the Discord Developer Portal. Unlike server emojis, they:

✅ **Advantages:**
- Available to your bot globally (no need to be in a specific server)
- Can be used in any Discord server
- Perfect for bot UI and branding
- Up to 2,000 emojis per bot
- Don't count against server emoji limits

## 🚀 Step-by-Step Setup

### Step 1: Upload Emojis to Developer Portal

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your bot application
3. Go to **"Rich Presence"** tab (or look for emoji/assets section)
4. Upload your custom emojis
5. Note down the emoji **names** exactly as you upload them

### Step 2: Extract Emoji IDs

Run the extractor script to find your emoji IDs:

```bash
python dev_portal_emoji_setup.py
```

You'll see output like:
```
🎨 DEVELOPER PORTAL EMOJI EXTRACTOR
======================================================================
✅ Bot Application: YourBotName
📱 Application ID: 1234567890

Name: success                | ID: 987654321
  Format: <:success:987654321>
  URL: https://cdn.discordapp.com/app-emojis/...
```

### Step 3: Update config.py

Open `config.py` and replace the emoji IDs:

```python
EMOJIS = {
    'success': '<:success:987654321>',      # Your emoji ID
    'error': '<:error:987654322>',
    'warning': '<:warning:987654323>',
    # ... continue for all emojis
}
```

### Step 4: Test the Emojis

Run your bot and test:

```bash
python main.py
```

Try commands that use emojis:
```
!help
!balance
!level
!warn @user
```

## 🎨 How to Create Custom Emojis

### Option 1: Design from Scratch
- Use tools like Photoshop, GIMP, or Canva
- Size: **128x128 pixels** (recommended)
- Format: **PNG with transparency**
- Keep file size under **256KB**

### Option 2: Use Online Tools
- [Emoji.cool](https://emoji.cool) - Emoji maker
- [Pixelartmaker](https://pixelartmaker.com) - Pixel art
- [Figma](https://figma.com) - Design templates

### Option 3: Find Pre-made Sets
- [OpenMoji](https://openmoji.org) - Free emoji set
- [Twemoji](https://twemoji.twitter.com) - Twitter emojis
- [Noto Emoji](https://fonts.google.com/noto/specimen/Noto+Color+Emoji) - Google emojis

## 📁 Emoji Naming Convention

Keep names consistent and easy to remember:

```
System:
  success, error, warning, info, loading

Moderation:
  mute, unmute, kick, ban, warn, lock, unlock

Economy:
  money, bank, wallet, coin, leaderboard

Games:
  game, giveaway, ticket, afk, levelup

Other:
  ai, help, settings, logs, delete, edit, user, role
```

## 🔧 Using Developer Portal Emojis in Code

### Method 1: Simple Reference
```python
from config import get_emoji

emoji = get_emoji('success')
await ctx.send(f"{emoji} Task completed!")
```

### Method 2: In Embeds
```python
from utils import emoji_utils

embed = emoji_utils.create_success_embed(
    "Success!",
    "Operation completed successfully"
)
await ctx.send(embed=embed)
```

### Method 3: Direct Access
```python
from config import EMOJIS

await ctx.send(f"{EMOJIS['money']} You have $100")
```

## 📊 Example Configuration

Here's a complete emoji setup:

```python
EMOJIS = {
    # System (IDs from your Developer Portal)
    'success': '<:success:1087654321>',
    'error': '<:error:1087654322>',
    'warning': '<:warning:1087654323>',
    'info': '<:info:1087654324>',
    'loading': '<:loading:1087654325>',
    
    # Moderation
    'mute': '<:mute:1087654326>',
    'kick': '<:kick:1087654327>',
    'ban': '<:ban:1087654328>',
    'warn': '<:warn:1087654329>',
    'lock': '<:lock:1087654330>',
    'unlock': '<:unlock:1087654331>',
    
    # Economy
    'money': '<:money:1087654332>',
    'bank': '<:bank:1087654333>',
    'wallet': '<:wallet:1087654334>',
    'coin': '<:coin:1087654335>',
    'leaderboard': '<:leaderboard:1087654336>',
}
```

## ⚠️ Troubleshooting

### Emojis not appearing
**Problem:** Discord shows "Unknown Emoji"

**Solutions:**
1. Verify the emoji ID is correct
2. Check emoji format: `<:name:ID>` (no spaces)
3. Ensure emoji is uploaded to Developer Portal
4. Run `dev_portal_emoji_setup.py` again

### "Emoji not found" error
**Problem:** Bot can't find the emoji

**Solutions:**
1. Make sure you're using the right emoji name
2. Check spelling (case-sensitive)
3. Verify emoji hasn't been deleted
4. Use fallback unicode emojis temporarily

### Emoji shows but looks wrong
**Problem:** Emoji displays but quality is poor

**Solutions:**
1. Re-upload emoji with better quality (128x128 PNG)
2. Use transparent background
3. Ensure file isn't too small

## 🔄 Fallback System

If a custom emoji fails, the bot automatically uses unicode fallbacks:

```python
# If this fails:
EMOJIS['success'] = '<:success:INVALID_ID>'

# Falls back to:
'success': '✅'
```

## 📚 Discord.py Emoji Methods

```python
# Get emoji by name
emoji = discord.utils.get(bot.emojis, name="success")

# Use in message
await ctx.send(f"{emoji} Success!")

# React with emoji
await message.add_reaction(emoji)

# Fetch application emojis
async for emoji in bot.fetch_application_emojis():
    print(emoji.name, emoji.id)
```

## 💡 Best Practices

1. **Consistency** - Use the same emojis throughout the bot
2. **Naming** - Use clear, descriptive names
3. **Quality** - Use high-quality PNG files
4. **Organization** - Group related emojis
5. **Fallbacks** - Always have unicode alternatives
6. **Testing** - Test emojis in different Discord clients
7. **Documentation** - Keep track of emoji IDs and purposes

## 📖 Quick Reference

```bash
# Extract emoji IDs
python dev_portal_emoji_setup.py

# Extract server emojis
python emoji_setup.py

# Test bot with emojis
python main.py
```

## 🔗 Useful Links

- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord.py Emoji Docs](https://discordpy.readthedocs.io/en/stable/api.html#emoji)
- [Discord API Emojis](https://discord.com/developers/docs/resources/emoji)
- [Emoji Design Tools](https://www.figma.com)

## ❓ FAQ

**Q: Can I use emojis from other bots?**
A: No, you can only use emojis your bot has access to.

**Q: How many emojis can I upload?**
A: Up to 2,000 emojis per bot application.

**Q: Do they work in all servers?**
A: Yes! Developer Portal emojis work globally.

**Q: What if I delete an emoji?**
A: Update config.py to use the fallback unicode emoji.

**Q: Can I animate emojis?**
A: Yes, upload as GIF (max 128x128, 256KB).

---

**Need Help?** Check the bot's documentation or Discord.py docs!
