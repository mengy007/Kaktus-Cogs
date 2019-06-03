from .daddy import Daddy


def setup(bot):
    cog = Daddy(bot)
    bot.add_cog(cog)
