import logging
import random
import discord
from redbot.core import commands
from redbot.core.utils.menus import menu
import contextlib

log = logging.getLogger("red.stone-cogs.randomemoji")


class RandomEmoji(commands.Cog):
    """Emoji Commands"""

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self._remaining = {}  # invoking message id -> emotes not yet shown

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def _all_emotes(self):
        return [emoji for guild in self.bot.guilds for emoji in guild.emojis]

    async def _make_embed(self, ctx, chosen_emote):
        embed = discord.Embed(colour=await ctx.embed_colour(), title=f"{chosen_emote.name}")
        embed.set_footer(
            text=f"GID: {chosen_emote.guild.id}\n"
            f"EID: {chosen_emote.id}\n"
            f"Remaining emotes: {len(self._remaining.get(ctx.message.id, []))}"
        )
        embed.set_image(url=chosen_emote.url)
        return embed

    @commands.command(aliases=["randomemote"])
    @commands.bot_has_permissions(embed_links=True)
    async def randomemoji(self, ctx):
        """Posts a random emote from guilds this bot is in"""
        list_of_emotes = self._all_emotes()
        if not list_of_emotes:
            return await ctx.send("I can't see any emojis in the servers I'm in.")
        random.shuffle(list_of_emotes)
        chosen_emote = list_of_emotes.pop()
        self._remaining[ctx.message.id] = list_of_emotes
        embed = await self._make_embed(ctx, chosen_emote)
        emote_controls = {"❌": self.close_menu, "🔁": self.refresh_menu}
        try:
            await menu(ctx=ctx, pages=[embed], controls=emote_controls, page=0, timeout=30)
        finally:
            self._remaining.pop(ctx.message.id, None)

    async def close_menu(
        self,
        ctx: commands.Context,
        pages: list,
        controls: dict,
        message: discord.Message,
        page: int,
        timeout: float,
        emoji: str,
        **kwargs,
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
        **kwargs,
    ):
        perms = message.channel.permissions_for(ctx.me)
        if perms.manage_messages:  # Can manage messages, so remove react
            with contextlib.suppress(discord.NotFound):
                await message.remove_reaction(emoji, ctx.author)
        list_of_emotes = self._remaining.get(ctx.message.id, [])
        if not list_of_emotes:  # Refill once every emote has been shown
            list_of_emotes = self._all_emotes()
            random.shuffle(list_of_emotes)
        if not list_of_emotes:
            with contextlib.suppress(discord.NotFound):
                await message.delete()
            return
        chosen_emote = list_of_emotes.pop()
        self._remaining[ctx.message.id] = list_of_emotes
        embed = await self._make_embed(ctx, chosen_emote)
        pages = [embed]
        return await menu(ctx, pages, controls, message=message, page=page, timeout=timeout)
