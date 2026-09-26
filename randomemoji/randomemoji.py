import logging
import random
import discord
from redbot.core import commands
from redbot.core.utils.menus import menu
import contextlib
import contextvars

log = logging.getLogger("red.stone-cogs.randomemoji")
emotes = contextvars.ContextVar("emotes", default=[])


class RandomEmoji(commands.Cog):
    """Emoji Commands"""

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command(aliases=["randomemote"])
    @commands.bot_has_permissions(embed_links=True)
    async def randomemoji(self, ctx):
        """Posts a random emote from guilds this bot is in"""
        list_of_emotes = []
        for guild in self.bot.guilds:
            for emoji in guild.emojis:
                list_of_emotes.append(emoji)
        emotes.set(list_of_emotes)
        chosen_emote = random.choice(list_of_emotes)
        embed = discord.Embed(colour=await ctx.embed_colour(), title=f"{chosen_emote.guild.name}")
        embed.set_footer(
            text=f"GID: {chosen_emote.guild.id}\n"
            f"EID: {chosen_emote.id}\n"
            f"Remaining emotes: {len(emotes.get())}"
        )
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
        list_of_emotes = emotes.get()
        random.shuffle(list_of_emotes)
        if list_of_emotes:
            chosen_emote = list_of_emotes.pop()
        else:
            for guild in self.bot.guilds:
                for emoji in guild.emojis:
                    list_of_emotes.append(emoji)
        emotes.set(list_of_emotes)

        # TODO Refresh list when popped

        embed = discord.Embed(colour=await ctx.embed_colour(), title=f"{chosen_emote.name}")
        embed.set_footer(
            text=f"GID: {chosen_emote.guild.id}\n"
            f"EID: {chosen_emote.id}\n"
            f"Remaining emotes: {len(emotes.get())}"
        )
        embed.set_image(url=chosen_emote.url)
        pages = [embed]
        return await menu(ctx, pages, controls, message=message, page=page, timeout=timeout)
