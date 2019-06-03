import discord
from redbot.core import Config, checks, commands
from redbot.core.bot import Red
from redbot.core.commands import Context

class Daddy(commands.Cog):

    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
    
    def __init__(self, red: Red):
        self.bot = red
    
    async def replydad(self, message):
        user = message.author
        server = message.server
        content = message.content
        if(content[:3].lower() == "im ") :
            await self.bot.say("Hello " + content[3:] + ", I'm " + self.bot.user.name)
        elif (content[:4].lower() == "i'm ") :
            await self.bot.say("Hello " + content[4:] + ", I'm " + self.bot.user.name)
