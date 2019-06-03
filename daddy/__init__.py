from .daddy import Daddy


def setup(bot):
    cog = Daddy(bot)
    bot.add_listener(cog.replydad, "on_message")
    bot.add_cog(cog)
