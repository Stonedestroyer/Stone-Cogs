import logging
import random
import discord
from redbot.core import commands
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions

log = logging.getLogger("red.Stone-Cogs.RandomEmoji")


class RandomEmoji(commands.Cog):
    """Emoji Commands"""

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @commands.command(aliases=["randomemote"])
    async def randomemoji(self, ctx):
        """Posts a random emote from guilds this bot is in"""
        listofemotes = []
        for guild in self.bot.guilds:
            for emoji in guild.emojis:
                listofemotes.append(emoji)
        chosen_emote = random.choice(listofemotes)
        description = f"Emote from {chosen_emote.guild.name} ({chosen_emote.guild.id})"
        embed = discord.Embed(colour=await ctx.embed_colour(), description=description)
        embed.set_image(url=chosen_emote.url)
        message = await ctx.send(embed=embed)
        start_adding_reactions(message, ["❌"])
        pred = ReactionPredicate.with_emojis(["❌"], message, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)
        if pred.result == 0:
            await message.delete()
