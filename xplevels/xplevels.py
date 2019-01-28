# !
# !
# ! NOT YET FINISHED, UNDER DEVELOPMENT
# !
# !
import discord
from discord.ext import commands
from .utils import checks
from .utils.dataIO import dataIO
from .utils.dataIO import fileIO
from __main__ import send_cmd_help
from random import randint
import os
import time
##from PIL import Image
##from PIL import ImageFont
##from PIL import ImageDraw 

client = discord.Client()
path = 'data/kaktuscog/xplevels'
rankimage = path + '/rankimage.png'
#https://github.com/ridinginstyle00/ridings-cogs/blob/master/Levels/Levels.py

class XPLevels:

    __author__ = "DasKaktus (DasKaktus#5299)"
    __version__ = "1.0"

    def __init__(self, bot):
        self.bot = bot
		
        try:
            self.settings = dataIO.load_json(path + "/settings.json")
        except Exception:
            self.settings =  {}

        #self.xpcool = self.settings[server.id]["XPCOOL"]
        #self.lvlupmsg = self.settings[server.id]["LVLUPMSG"]
        #self.backlistchannel = self.settings[server.id]["BLACKLISTCHANNELS"]
        #self.backlistrole = self.settings[server.id]["BLACKLISTROLES"]
        #self.resetonleave = self.settings[server.id]["RESETONLEAVE"]
        self.leaderboard = dataIO.load_json(path + "/leaderboard.json")
        self.roleboard = dataIO.load_json(path + "/roleboard.json")

        self.waitingxp = {}

# USER COMMANDS
    @commands.command(name="rank", pass_context=True)
    async def rank(self, ctx, user : discord.Member=None):
        """Show rank and XP.

        Defaults to yours."""
        if not user:
            user = ctx.message.author
            if user.id not in self.leaderboard:
                self.leaderboard[user.id] = {"username": user.name, "rank": 0, "XP": 0}

            await self.bot.say("{} **LEVEL {} | XP {}/{} **".format(user.name, self.getuserrank(user),
                                                                         self.get_xp(user.id),
                                                                         self.get_level_xp(int(self.leader_board[user.id]["rank"]))))
        else:
            # Check if user exists in leader board, then check if user is in discord server
            if isusermember(user_id):
                rank = self.get_rank(user.id)
                xp = self.get_xp(user.id)
                channel = ctx.message.channel
                img = await makeimage(user)
                with open(img, 'rb') as f:
                    await self.bot.send_file(channel, f, filename='rank.png', content=content, embed=embed)
                #await self.bot.say("{}'s stats: **LEVEL {} | XP {}/{} **".format(user.mention, self.getuserrank(user.),
                                                                         self.get_xp(user.id),
                                                                         self.get_level_xp(int(self.leader_board[user.id]["rank"]))))
            else:
                tell_nouser()

# ADMIN COMMANDS
		
    @commands.group(name="xplevelset", pass_context=True)		
    async def _rank(self, ctx):
        """Rank operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_rank.command(name="set", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _set(self, ctx, user : discord.Member, rank : int, xp : int):
        """Set Rank and XP"""
        self.leaderboard[user.id] = {"username": user.name, "rank": rank, "XP": xp}
        dataIO.save_json(path + "/leaderboard.json", self.leaderboard)
        await self.bot.say("**{}'s has been set to rank {} with {}/{} xp**".format(user.mention, self.getuserrank(user), self.getxp(user.id), self.getlevelxp(int(self.leaderboard[user.id]["rank"]))))
			
    @_rank.command(pass_context=True, no_pm=True)
    async def leave(self, ctx, user : discord.Member=None):
        """Resets rank and EXP!"""
        if self.settings[server.id]["RESETONLEAVE"] == 1:
            user = ctx.message.author
            if user.id in self.leader_board:
                del self.leader_board[user.id]
                dataIO.save_json(path + "/leaderboard.json", self.leaderboard)


# BOT FUNCTIONS

    async def gainxp(self, message):
        user = message.author
        if user.id in self.waitingxp:
            seconds = abs(self.waitingxp[user.id] - int(time.perf_counter()))
            if seconds >= self.xpcool:
                self.addxp(user)
                self.gettingxp[user.id] = int(time.perf_counter())
                fileIO(path + "/leaderboard.json", "save", self.leaderboard)
            if self.leaderboard[user.id]["XP"] >= self.getxplevel(self.leaderboard[user.id]["rank"]):
                self.leaderboard[user.id]["rank"] += 1
                self.leaderboard[user.id]["XP"] = 0
                msg = '{} **has leveled up and is now level {}!!!\n HURRAY!!**'
                msg = msg.format(message.author.display_name, self.leader_board[user.id]["rank"])
                await self.bot.send_message(message.channel, msg)
                fileIO(path + "/leaderboard.json", "save", self.leader_board)
        else:
            self.addxp(id)
            self.gettingxp[id] = int(time.perf_counter())
            fileIO(path + "/leaderboard.json", "save", self.leader_board)

    def addxp(self, user):
        if user.id not in self.leaderboard:
            addtoleaderboard(user)
        self.leaderboard[user.id]["XP"] += int(randint(15, 20))

    def addtoleaderboard(self, user):
        self.leaderboard[user.id] = {"username": user.name, "rank": 0, "XP": 0}
        dataIO.save_json(path + "/leaderboard.json", self.leaderboard)

    def getxplevel(self, level):
        xp = 5*(int(level)**2)+50*int(level)+100
        return xp

    def getuserrank(self, user):
        #TODO CHECK IF USER ARE IN DISCORD SERVER
        if user.id in self.leaderboard:
            return self.leaderboard[user.id]["rank"]
        else:
            return 0

    def isusermember(self, ctx, userid: int):
        member = discord.utils.get(ctx.guild.members, id=userid)
        if member:
            return True
        else:
            return False

    def tell_nouser(self):
	
    def makeimage(self, user):
    	img = Image.open(rankimage)
        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
		# draw.text((x, y),"Sample Text",(r,g,b))
		
		#TODO Get Profile Pic
		#TODO Måste tänka över Rank och level, rank i denna koden är egentligen level... :thonk:
		
        fontsmall = ImageFont.truetype("sans-serif.ttf", 8)
		fontbig = ImageFont.truetype("sans-serif.ttf", 16)
        
		draw.text((0, 0),"RANK",(255,255,255),font=fontsmall)
		draw.text((40, 0),"#" + getuserrank(user),(255,255,255),font=fontsmall)
		
		draw.text((0, 0),"LEVEL",(255,255,255),font=fontsmall)
		draw.text((40, 0),"#" + getuserrank(user),(255,255,255),font=fontsmall)
		
        img.save(path + '/tmp/sample-out.jpg')
        return path + '/tmp/sample-out.jpg'
        #sent = await self.bot.send_file(msg_dest, attachment, filename='captcha.png', content=content, embed=embed)

def check_folders():
    if not os.path.exists(path):
        print("Creating " + path + " folder...")
        os.mkdir(path)
        print("Creating " + path + "/tmp folder...")
        os.mkdir(path + '/tmp')


def check_files():
    fp = path + "/leaderboard.json"
    if not dataIO.is_valid_json(fp):
        print("Creating leaderboard.json...")
        dataIO.save_json(fp, {})

    fp = path + "/roleboard.json"
    if not dataIO.is_valid_json(fp):
        print("Creating roleboard.json...")
        dataIO.save_json(fp, {})


def setup(bot):
    check_folders()
    check_files()
    n = XPLevels(bot)
    bot.add_listener(n.gainxp, "on_message")
    bot.add_cog(n)
