import logging
import random
import discord
from redbot.core import commands
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
import contextlib
import contextvars

log = logging.getLogger("red.Stone-Cogs.RandomEmoji")
emotes = contextvars.ContextVar("emotes")


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
        emotes.set(listofemotes)
        chosen_emote = random.choice(listofemotes)
        description = f"{chosen_emote.guild.id}"
        embed = discord.Embed(colour=await ctx.embed_colour(), title=f"{chosen_emote.guild.name}")
        embed.set_footer(text=f"GID: {chosen_emote.guild.id}\n" f"EID: {chosen_emote.id}")
        embed.set_image(url=chosen_emote.url)
        emote_controls = {"❌": self.close_menu, "🔁": self.refresh_menu}
        await menu(ctx=ctx, pages=[embed], controls=emote_controls, page=0, timeout=30)

    async def close_menu(
        self,
        ctx: commands.Context,
        pages: list,
        controls: dict,
        message: discord.Message,
        page: int,
        timeout: float,
        emoji: str,
    ):
        with contextlib.suppress(discord.NotFound):
            await message.delete()

    async def refresh_menu(
        self,
        ctx: commands.Context,
        pages: list,
        controls: dict,
        message: discord.Message,
        page: int,
        timeout: float,
        emoji: str,
    ):
        perms = message.channel.permissions_for(ctx.me)
        if perms.manage_messages:  # Can manage messages, so remove react
            with contextlib.suppress(discord.NotFound):
                await message.remove_reaction(emoji, ctx.author)
        # emote logic
        listofemotes = emotes.get()
        random.shuffle(listofemotes)
        chosen_emote = listofemotes.pop()
        emotes.set(listofemotes)

        embed = discord.Embed(colour=await ctx.embed_colour(), title=f"{chosen_emote.guild.name}")
        embed.set_footer(text=f"GID: {chosen_emote.guild.id}\n" f"EID: {chosen_emote.id}")
        embed.set_image(url=chosen_emote.url)
        await message.edit(embed=embed)
        pages = [embed]
        return await menu(ctx, pages, controls, message=message, page=page, timeout=timeout)
