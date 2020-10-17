from .randomemoji import RandomEmoji


def setup(bot):
    n = RandomEmoji(bot)
    bot.add_cog(n)
