# Discord
import discord

# Red
from redbot.core import commands
from redbot.core.bot import Red

class Daddy:

    async def on_message(self, message: discord.Message):
        guild: discord.Guild = message.guild
        txt = message.clean_content.lower()
        splittxt = txt.split()
        if len(splittxt) == 0:
            return

        if splittxt[0] == "i'm" and len(splittxt) >= 2:
            out = txt[4:]
            await message.channel.send("Hi {}, I'm {}!".format(out, guild.me.display_name))
        elif splittxt[0] == "im" and len(splittxt) >= 2:
            out = txt[4:]
            await message.channel.send("Hi {}, I'm {}!".format(out, guild.me.display_name))
