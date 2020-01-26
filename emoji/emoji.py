import logging
import random

from redbot.core import commands

log = logging.getLogger("red.Stone-Cogs.Emoji")

__VERSION__ = 1.0.1

class Emoji(commands.Cog):
    """Emoji Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['randomemote'])
    @commands.is_owner()
    async def randomemoji(self, ctx):
        """Posts a random emote from guilds this bot is in"""
        listofemotes = []
        for guild in self.bot.guilds:
            for emoji in guild.emojis:
                listofemotes.append(emoji)
        chosen_emote = random.choice(listofemotes)
        await ctx.send(f"Emote from {chosen_emote.guild.name} ({chosen_emote.guild.id})")
        await ctx.send(f"{chosen_emote}")
