import discord
from discord.ext import commands
import pathlib
from cogs.utils.dataIO import dataIO
import aiohttp
import io
from .utils import checks

path = 'data/kaktuscog/stattracker'

#bot = commands.Bot(command_prefix=commands.when_mentioned, description="Battlefield Stats Tracker")

class Stattracker:

    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "2.0"

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        try:
            self.settings = dataIO.load_json(path + '/settings.json')
        except Exception:
            self.settings = {}

    def save_json(self):
        dataIO.save_json(path + '/settings.json', self.settings)

    def init_server(self, server: discord.Server, reset=False):
        if server.id not in self.settings or reset:
            self.settings[server.id] = {
                'whitelist': []
            }

    @commands.group(name='statsset', pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def _group(self, ctx):
        """
        settings for stattracker	
        """

        if ctx.invoked_subcommand is None:
            #await self.bot.send_help(ctx)
            #await ctx.send_help()
            await self.send_cmd_help(ctx)
	
    @_group.command(name='whitelist', pass_context=True, no_pm=True)
    async def whitelist(self, ctx, channel: discord.Channel):
        """
        add a channel where stats are allowed (if you want)
        """

        server = ctx.message.server
        self.init_server(server)

        if channel.id in self.settings[server.id]['whitelist']:
            return await self.bot.say('Channel already whitelisted')
        self.settings[server.id]['whitelist'].append(channel.id)
        self.save_json()
        await self.bot.say('Channel whitelisted.')

    @_group.command(name='unwhitelist', pass_context=True, no_pm=True)
    async def unwhitelist(self, ctx, channel: discord.Channel):
        """
        unwhitelist a channel
        """

        server = ctx.message.server
        self.init_server(server)

        if channel.id not in self.settings[server.id]['whitelist']:
            return await self.bot.say('Channel wasn\'t whitelisted')
        self.settings[server.id]['whitelist'].remove(channel.id)
        self.save_json()
        await self.bot.say('Channel unwhitelisted.')

    @_group.command(name='reset', pass_context=True, no_pm=True)
    async def rset(self, ctx):
        """
        resets to defaults
        """

        server = ctx.message.server
        self.init_server(server, True)
        await self.bot.say('Settings reset')
	
    @commands.command(pass_context=True, no_pm=True, name="bfvstats")
    async def bfvstats(self, ctx, platform, *, playername):
        """Retrieves stats for BFV"""

        server = ctx.message.server
        channel = ctx.message.channel
		
        if server.id not in self.settings:
            return
        if channel.id not in self.settings[server.id]['whitelist']:
            return
			
        await self.bot.send_typing(channel)
        try:
            p = {
                'PSN': 2,
                'PS4': 2,
                'PLAYSTATION': 2,
                'XBOX': 1,
                'XB': 1,
                'XB1': 1,
                'X1': 1,
                'PC': 3,
                'MAC': 4,
            }
            pform = p.get(platform.upper(), 0)
            if pform:
                if pform == 4:
                    await self.bot.say(ctx.message.author.mention + ", Ha ha ha ha ha... Mac.. You Sir are hilarious")
                else:
                    url = 'https://www.baver.se/bfv/index.php?pf=' + str(pform) + '&user=' + playername.replace(" ", "%20")
                    await fetch_image(self, ctx, ctx.message.author, url, playername, platform)
            else:
                await self.bot.say(ctx.message.author.mention + ", please specify a valid platform. (PSN, XBOX or PC)")
        except Exception as e:
            #await self.bot.say("error: " + e.message + " -- " + e.args)
            err = e.message
		
    @commands.command(pass_context=True, no_pm=True, name="bf1stats")
    async def bf1stats(self, ctx, platform, *, playername):
        """Retrieves stats for BF1"""

        server = ctx.message.server
        channel = ctx.message.channel
		
        if server.id not in self.settings:
            return
        if channel.id not in self.settings[server.id]['whitelist']:
            return
			
        await self.bot.send_typing(channel)
        try:
            p = {
                'PSN': 2,
                'PS4': 2,
                'PLAYSTATION': 2,
                'XBOX': 1,
                'XB': 1,
                'XB1': 1,
                'X1': 1,
                'PC': 3,
                'MAC': 4,
            }
            pform = p.get(platform.upper(), 0)
            if pform:
                if pform == 4:
                    await self.bot.say(ctx.message.author.mention + ", Ha ha ha ha ha... Mac.. You Sir are hilarious")
                else:
                    url = 'http://bots.tracker.network/bf1/bf1.php?platform=' + str(pform) + '&username=' + playername
                    await fetch_image(self, ctx, ctx.message.author, url, playername, platform)
            else:
                await self.bot.say(ctx.message.author.mention + ", please specify a valid platform. (PSN, XBOX or PC)")
        except Exception as e:
            #await self.bot.say("error: " + e.message + " -- " + e.args)
            err = e.message

    def __unload(self):
        self.session.close()
		
    async def send_cmd_help(self, ctx):
        if ctx.invoked_subcommand:
            pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)
        else:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)


async def fetch_image(self, ctx, duser, urlen, user, platform):
    async with aiohttp.get(urlen) as response:
        if response.headers['Content-Type'] == "image/png":
            return await self.bot.send_file(ctx.message.channel, io.BytesIO(await response.read()), filename=user + '.png')
        else:
            return await self.bot.say("Sorry " + duser.mention + ", could not find the player `"+ user + "`")

def setup(bot):
    pathlib.Path(path).mkdir(exist_ok=True, parents=True)
    bot.add_cog(Stattracker(bot))
