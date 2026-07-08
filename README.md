# Discord Bot Auto Moderation

This is a fully-featured Discord bot with comprehensive moderation, auto-moderation, games, AI integration, and more.

## Features

### 🎉 Welcome System
- Set welcome channel
- Customize welcome messages
- Add welcome images
- Test welcome messages

### 🛡️ Moderation
- **User Management**: Mute, Unmute, Kick, Ban, Softban, Unban
- **Warnings**: Warn, View Warnings, Delete Warnings
- **Message Purging**: Purge all, by text, by user, bots only, with files, with links
- **Channel Management**: Lock, Unlock, Slowmode
- **Role Management**: Add/Remove roles
- **Channel/Role Creation**: Create and delete channels/roles

### 🤐 Auto Moderation (AutoMod)
- All caps detection
- Bad words filter
- Duplicate text detection
- Character count limits
- Emoji spam detection
- Fast message spam detection
- Image spam detection
- Invite link detection
- Phishing links detection
- Mass mentions detection
- Mentions cooldown
- Spoiler detection
- Masked links detection
- Sticker abuse prevention
- Zalgo text detection

### 😴 AFK System
- Set AFK status with custom message
- Auto-remove AFK when typing
- Get notified when mentioning AFK users

### 🎁 Giveaway System
- Create giveaways
- Set winners count
- End giveaways and pick winners
- Reroll giveaways

### 🎟️ Ticket System
- Support ticket panel
- Auto-create ticket channels
- Ticket management with buttons

### 🤖 AI Integration
- Gemini AI assistant
- Ask questions
- Image concept generation

### 🎮 Games
- Guess the Number game with DM interface
- Emoji reactions for correct answers

### 📊 Logging System
- Message delete logs
- Message edit logs
- Member join/leave logs
- Mod action logs

### 🛠️ Extra Features
- Auto Responder (custom triggers & responses)
- Auto Reactions
- Auto Role assignment on join
- No Prefix command access (admin-only)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```
DISCORD_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Run the bot:
```bash
python main.py
```

## Commands

### Welcome
- `!setwelcomechannel <channel>` - Set welcome channel
- `!setwelcometext <text>` - Set welcome message
- `!setwelcomeimage <url>` - Set welcome image
- `!testwelcome` - Test welcome message

### Moderation
- `!mute @user [duration] [reason]` - Mute a user
- `!unmute @user` - Unmute a user
- `!kick @user [reason]` - Kick a user
- `!ban @user [reason]` - Ban a user
- `!softban @user [reason]` - Softban a user
- `!unban <user_id> [reason]` - Unban a user
- `!warn @user [reason]` - Warn a user
- `!warnings [@user]` - View warnings
- `!delwarn <warn_id>` - Delete a warning
- `!purge <amount>` - Purge messages
- `!purgetext <text> [amount]` - Purge messages with text
- `!purgeuser @user [amount]` - Purge user's messages
- `!purgebots [amount]` - Purge bot messages
- `!purgefiles [amount]` - Purge messages with attachments
- `!purgelinks [amount]` - Purge messages with links
- `!lock [reason]` - Lock channel
- `!unlock [reason]` - Unlock channel
- `!slowmode <seconds>` - Set slowmode
- `!addrole @user @role` - Add role to user
- `!removerole @user @role` - Remove role from user
- `!prefix <new_prefix>` - Change prefix

### AFK
- `!afk [status]` - Set AFK status
- `!unafk` - Remove AFK status

### Giveaway
- `!gstart <duration> <winners> <prize>` - Start giveaway (e.g., `!gstart 1h 1 Steam Gift Card`)
- `!gend <message_id>` - End giveaway
- `!greroll <message_id>` - Reroll giveaway

### Tickets
- `!ticketpanel` - Create ticket support panel

### AI
- `!ask <question>` - Ask Gemini AI
- `!imagine <prompt>` - Generate image description

### Games
- `!guessthenumber [max_number]` - Start guess the number game (default: 100)

### Logs
- `!setmodlogs <channel>` - Set mod logs channel
- `!setchatlogs <channel>` - Set chat logs channel
- `!setuserlogs <channel>` - Set user logs channel

### Extra
- `!arset <trigger> <response>` - Set auto responder
- `!arremove <trigger>` - Remove auto responder
- `!arreact <trigger> <emoji>` - Set auto reaction
- `!np give @user` - Give no prefix access
- `!np remove @user` - Remove no prefix access
- `!np list` - List no prefix users
- `!autorole @role` - Set auto role on join

## Database

The bot uses SQLite for persistent storage. All data is stored in `bot_data.db`.

## Configuration

Edit `config.py` to customize:
- Bot prefix
- Embed colors
- Warning timeout
- And more...

## Support

For issues or feature requests, please create an issue on GitHub.

## License

MIT License
