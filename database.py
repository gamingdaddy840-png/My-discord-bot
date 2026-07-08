import aiosqlite
import asyncio
from config import DATABASE_FILE

class Database:
    def __init__(self):
        self.db_file = DATABASE_FILE

    async def init_db(self):
        """Initialize database with all required tables"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.executescript("""
            -- Guild Settings
            CREATE TABLE IF NOT EXISTS guild_settings (
                guild_id INTEGER PRIMARY KEY,
                prefix TEXT DEFAULT '!',
                welcome_channel_id INTEGER,
                welcome_text TEXT,
                welcome_image_url TEXT,
                mod_logs_channel_id INTEGER,
                chat_logs_channel_id INTEGER,
                user_logs_channel_id INTEGER
            );

            -- Warnings
            CREATE TABLE IF NOT EXISTS warnings (
                warn_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                user_id INTEGER,
                moderator_id INTEGER,
                reason TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(guild_id) REFERENCES guild_settings(guild_id)
            );

            -- Mutes
            CREATE TABLE IF NOT EXISTS mutes (
                mute_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                user_id INTEGER,
                end_time DATETIME,
                reason TEXT
            );

            -- AutoMod Settings
            CREATE TABLE IF NOT EXISTS automod_settings (
                guild_id INTEGER PRIMARY KEY,
                all_caps BOOLEAN DEFAULT 0,
                bad_words BOOLEAN DEFAULT 0,
                duplicate_text BOOLEAN DEFAULT 0,
                emoji_spam BOOLEAN DEFAULT 0,
                fast_messages BOOLEAN DEFAULT 0,
                image_spam BOOLEAN DEFAULT 0,
                invite_links BOOLEAN DEFAULT 0,
                phishing_links BOOLEAN DEFAULT 0,
                mass_mentions BOOLEAN DEFAULT 0,
                masked_links BOOLEAN DEFAULT 0,
                spoilers BOOLEAN DEFAULT 0,
                zolgo_text BOOLEAN DEFAULT 0,
                FOREIGN KEY(guild_id) REFERENCES guild_settings(guild_id)
            );

            -- Bad Words List
            CREATE TABLE IF NOT EXISTS bad_words (
                word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                word TEXT,
                FOREIGN KEY(guild_id) REFERENCES guild_settings(guild_id)
            );

            -- AFK
            CREATE TABLE IF NOT EXISTS afk_status (
                user_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            -- Giveaways
            CREATE TABLE IF NOT EXISTS giveaways (
                giveaway_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                channel_id INTEGER,
                message_id INTEGER,
                prize TEXT,
                winners_count INTEGER,
                end_time DATETIME,
                ended BOOLEAN DEFAULT 0
            );

            -- Giveaway Entries
            CREATE TABLE IF NOT EXISTS giveaway_entries (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                giveaway_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY(giveaway_id) REFERENCES giveaways(giveaway_id)
            );

            -- Tickets
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                channel_id INTEGER,
                user_id INTEGER,
                status TEXT DEFAULT 'open',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                closed_at DATETIME
            );

            -- AutoResponder
            CREATE TABLE IF NOT EXISTS auto_responder (
                response_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                trigger TEXT,
                response TEXT,
                FOREIGN KEY(guild_id) REFERENCES guild_settings(guild_id)
            );

            -- AutoReaction
            CREATE TABLE IF NOT EXISTS auto_reaction (
                reaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                trigger TEXT,
                emoji TEXT,
                FOREIGN KEY(guild_id) REFERENCES guild_settings(guild_id)
            );

            -- No Prefix Users
            CREATE TABLE IF NOT EXISTS no_prefix_users (
                user_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            -- User Economy
            CREATE TABLE IF NOT EXISTS economy (
                user_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                balance INTEGER DEFAULT 0,
                bank INTEGER DEFAULT 0
            );

            -- Levels
            CREATE TABLE IF NOT EXISTS levels (
                user_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1
            );
            """)
            await db.commit()

    async def get_setting(self, guild_id, setting):
        """Get a guild setting"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                f"SELECT {setting} FROM guild_settings WHERE guild_id = ?",
                (guild_id,)
            ) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else None

    async def set_setting(self, guild_id, setting, value):
        """Set a guild setting"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                f"INSERT OR REPLACE INTO guild_settings (guild_id, {setting}) VALUES (?, ?)",
                (guild_id, value)
            )
            await db.commit()

    async def add_warning(self, guild_id, user_id, moderator_id, reason):
        """Add a warning to a user"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                "INSERT INTO warnings (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
                (guild_id, user_id, moderator_id, reason)
            )
            await db.commit()

    async def get_user_warnings(self, guild_id, user_id):
        """Get all warnings for a user"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                "SELECT * FROM warnings WHERE guild_id = ? AND user_id = ? ORDER BY timestamp DESC",
                (guild_id, user_id)
            ) as cursor:
                return await cursor.fetchall()

    async def delete_warning(self, warn_id):
        """Delete a specific warning"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("DELETE FROM warnings WHERE warn_id = ?", (warn_id,))
            await db.commit()

db = Database()
