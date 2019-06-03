from .daddy import Daddy


def setup(bot):
    n = Daddy(bot)
    bot.add_listener(n.replydad, "on_message")
    bot.add_cog(n)
