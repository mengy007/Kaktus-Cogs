# Discord
import discord

# Red
from redbot.core import commands

Cog = getattr(commands, "Cog", object)

class Daddy(Cog):

    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
    
    def __init__(self, bot):
        self.bot = bot
    
    async def replydad(self, message: discord.Message):
        guild: discord.Guild = message.guild
        txt = message.clean_content.lower()
        splittxt = txt.split()
        if len(splittxt) == 0:
            return

        if splittxt[0] == "i'm" and len(splittxt) >= 2:
            out = txt[4:]
            await message.channel.send("Hi {}, I'm {}!".format(out, guild.me.display_name))
        elif splittxt[0] == "im" and len(splittxt) >= 2:
            out = txt[3:]
            await message.channel.send("Hi {}, I'm {}!".format(out, guild.me.display_name))
