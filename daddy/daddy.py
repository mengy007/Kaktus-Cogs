import discord
from discord.ext import commands

class Daddy:

    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
    
    def __init__(self, bot):
        self.bot = bot
            
    async def replydad(self, message):
        user = message.author
        server = message.server
        content = message.content
        if(content[:3].lower() == "im ") :
		    await self.bot.say("Hello " + content[3:] + ", I'm " + self.bot.user.name)
		elif (content[:4].lower() == "i'm ")
		    await self.bot.say("Hello " + content[4:] + ", I'm " + self.bot.user.name)
        

def setup(bot):
    n = Daddy(bot)
    bot.add_listener(n.replydad, "on_message")
    bot.add_cog(n)
