import discord
from discord.ext import commands
import aiohttp
import io

class Stattracker:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
		
    @commands.command(pass_context=True, no_pm=True, name="bf1stats")
    async def bf1stats(self, ctx, platformog, user):
        """Retrieves stats for BF1"""
        await self.bot.send_typing(ctx.message.channel)
        try:
            p = {
                'PSN': 2,
                'PS4': 2,
                'XBOX': 1,
                'X1': 1,
                'PC': 3,
            }
            platform = p.get(platformog.upper(), 0)
            if platform:
                url = 'http://bots.tracker.network/bf1/bf1.php?platform=' + str(platform) + '&username=' + user
                await fetch_image(self, ctx, ctx.message.author, url, user, platformog)
            else:
                await self.bot.say("Please specify a valid platform. (PSN, XBOX or PC)")
        except Exception as e:
            await self.bot.say("error: " + e.message + " -- " + e.args)
			
    def __unload(self):
        self.session.close()

async def fetch_image(self, ctx, duser, urlen, user, platform):
    async with aiohttp.get(urlen) as response:
        if response.headers['Content-Type'] == "image/png":
            return await self.bot.send_file(ctx.message.channel, io.BytesIO(await response.read()), filename=user + '.png')
        else:
            return await self.bot.say(duser.mention + " Sorry, could not find the player '"+user+"'")

def setup(bot):
    bot.add_cog(Stattracker(bot))
