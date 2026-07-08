import discord
from discord.ext import commands
from config import get_emoji, COLORS

class EmojiUtils:
    """Utility class for emoji management"""
    
    @staticmethod
    def get_emoji(name):
        """Get emoji by name with fallback"""
        return get_emoji(name)
    
    @staticmethod
    def create_embed(title, description=None, emoji_name='info', color=None, **kwargs):
        """Create an embed with emoji"""
        emoji = get_emoji(emoji_name)
        full_title = f"{emoji} {title}"
        
        if color is None:
            color = COLORS['info']
        
        embed = discord.Embed(
            title=full_title,
            description=description,
            color=color,
            **kwargs
        )
        return embed
    
    @staticmethod
    def create_success_embed(title, description=None, **kwargs):
        """Create a success embed"""
        return EmojiUtils.create_embed(title, description, 'success', COLORS['success'], **kwargs)
    
    @staticmethod
    def create_error_embed(title, description=None, **kwargs):
        """Create an error embed"""
        return EmojiUtils.create_embed(title, description, 'error', COLORS['error'], **kwargs)
    
    @staticmethod
    def create_warning_embed(title, description=None, **kwargs):
        """Create a warning embed"""
        return EmojiUtils.create_embed(title, description, 'warning', COLORS['warning'], **kwargs)

# Create a global instance
emoji_utils = EmojiUtils()
