from .emoji import Emoji


def setup(bot):
    n = Emoji(bot)
    bot.add_cog(n)