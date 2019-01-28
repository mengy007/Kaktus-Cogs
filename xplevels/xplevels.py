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
from io import BytesIO
from __main__ import send_cmd_help
from random import randint
import os
import time
import aiohttp
try:
    from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
    pilAvailable = True
except ImportError:
    pilAvailable = False

client = discord.Client()
path = 'data/kaktuscog/xplevels'
rankimage = path + '/card.png'
fontpath = path + '/BebasNeue.otf'

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
        self.session = aiohttp.ClientSession()

# USER COMMANDS
    @commands.command(name="rank", pass_context=True)
    async def rank(self, ctx, user : discord.Member=None):
        """Show rank and XP.

        Defaults to yours."""
        if self.checkenabled(ctx.message.server):
            server = ctx.message.server
            if not user:
                user = ctx.message.author
                if user.id not in self.leaderboard[server.id]:
                    self.leaderboard[server.id][user.id] = {"username": user.name, "rank": 0, "XP": 0}

                #await self.bot.say("{} **LEVELL {} | XP {}/{} **".format(user.name, self.getuserrank(ctx,user), self.getxp(ctx, user), self.getxplevel(int(self.leaderboard[server.id][user.id]["rank"]))))
                rank = self.getuserrank(ctx, user)
                xp = self.getxp(ctx, user)
                channel = ctx.message.channel
                channel_object = self.bot.get_channel(channel.id)
                #await self.makeimage(ctx, user)
                image_obj = await self.makeimage(user, rank, xp)
                await self.bot.send_file(channel_object, image_obj, filename="rank.png")
            else:
                # Check if user exists in leader board, then check if user is in discord server
                if self.isusermember(ctx, user.id):
                    rank = self.getuserrank(ctx, user)
                    xp = self.getxp(ctx, user)
                    channel = ctx.message.channel
                    channel_object = self.bot.get_channel(channel.id)
                    #await self.makeimage(ctx, user)
                    image_obj = await self.makeimage(user, rank, xp)
                    await self.bot.send_file(channel_object, image_obj, filename="rank.png")
                    #os.remove('data/drawing/temp.png')
                    #await self.bot.say("{}'s stats: **LEVEL {} | XP {}/{} **".format(user.mention, self.getuserrank(user.), self.get_xp(user.id), self.get_level_xp(int(self.leaderboard[user.id]["rank"]))))
                else:
                    tell_nouser()

# ADMIN COMMANDS

    @commands.group(name="xplevelset", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _xplevelset(self, ctx):
        """Rank operations"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
    
    @_xplevelset.command(pass_context=True, no_pm=True)
    async def enablelevel(self, ctx):
        """Enable Rank on server"""
        if ctx.message.server.id not in self.settings:
            self.settings[ctx.message.server.id] = {}
            self.settings[ctx.message.server.id]["ENABLED"] = True
            self.settings[ctx.message.server.id]["XPCOOL"] = 60
            self.settings[ctx.message.server.id]["LVLUPMSG"] = "GG airshipa, you ranked up!"
            self.settings[ctx.message.server.id]["BLACKLISTCHANNELS"] = {}
            self.settings[ctx.message.server.id]["BLACKLISTROLES"] = {}
            self.settings[ctx.message.server.id]["RESETONLEAVE"] = True
            
            self.xpcool = self.settings[ctx.message.server.id]["XPCOOL"]
            self.lvlupmsg = self.settings[ctx.message.server.id]["LVLUPMSG"]
            self.backlistchannel = self.settings[ctx.message.server.id]["BLACKLISTCHANNELS"]
            self.backlistrole = self.settings[ctx.message.server.id]["BLACKLISTROLES"]
            self.resetonleave = self.settings[ctx.message.server.id]["RESETONLEAVE"]
        else:
            self.settings[ctx.message.server.id]["ENABLED"] = True
        
        dataIO.save_json(path + "/settings.json", self.settings)
    
    @_xplevelset.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def disablelevel(self, ctx):
        if ctx.message.server.id in self.settings:
            self.settings[ctx.message.server.id]["ENABLED"] = False
        dataIO.save_json(path + "/settings.json", self.settings)
    
    @_xplevelset.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)    
    async def setcooldown(self, ctx, coold: str):
        if ctx.message.server.id in self.settings:
            self.settings[ctx.message.server.id]["XPCOOL"] = int(coold)
        dataIO.save_json(path + "/settings.json", self.settings)


    @_xplevelset.command(name="set", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _set(self, ctx, user : discord.Member, rank : int, xp : int):
        """Set Rank and XP"""
        server = ctx.message.server
        self.leaderboard[server.id][user.id] = {"username": user.name, "rank": rank, "XP": xp}
        dataIO.save_json(path + "/leaderboard.json", self.leaderboard)
        await self.bot.say("**{}'s has been set to rank {} with {}/{} xp**".format(user.mention, self.getuserrank(user), self.getxp(ctx, user.id), self.getxplevel(int(self.leaderboard[server.id][user.id]["rank"]))))

    @_xplevelset.command(pass_context=True, no_pm=True)
    async def leave(self, ctx, user : discord.Member=None):
        """Resets rank and EXP!"""
        server = ctx.message.server
        if self.settings[server.id]["RESETONLEAVE"] == 1:
            user = ctx.message.author
            if user.id in self.leaderboard[server.id]:
                del self.leaderboard[server.id][user.id]
                dataIO.save_json(path + "/leaderboard.json", self.leaderboard)


# BOT FUNCTIONS

    async def gainxp(self, message):
        if self.checkenabled(message.server):
            user = message.author
            server = message.server
            if user == self.bot.user:
                return
            if user.id in self.waitingxp:
                seconds = abs(self.waitingxp[user.id] - int(time.perf_counter()))
                if seconds >= self.settings[server.id]["XPCOOL"]:
                    self.addxp(message, user)
                    self.waitingxp[user.id] = int(time.perf_counter())
                    fileIO(path + "/leaderboard.json", "save", self.leaderboard)
                if self.leaderboard[server.id][user.id]["XP"] >= self.getxplevel(self.leaderboard[server.id][user.id]["rank"]):
                    self.leaderboard[server.id][user.id]["rank"] += 1
                    self.leaderboard[server.id][user.id]["XP"] = 0
                    msg = '{} **has leveled up and is now level {}!!!\n HURRAY!!**'
                    msg = msg.format(message.author.display_name, self.leaderboard[server.id][user.id]["rank"])
                    await self.bot.send_message(message.channel, msg)
                    fileIO(path + "/leaderboard.json", "save", self.leaderboard)
            else:
                self.addxp(message, user)
                self.waitingxp[user.id] = int(time.perf_counter())
                fileIO(path + "/leaderboard.json", "save", self.leaderboard)
    
    def checkenabled(self, server):
        if server.id in self.settings:
            if "ENABLED" in self.settings[server.id]:
                if self.settings[server.id]["ENABLED"]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def addxp(self, message, user):
        server = message.server
        if server.id not in self.leaderboard:
            self.leaderboard[server.id] = {}
        if user.id not in self.leaderboard[server.id]:
            self.addtoleaderboard(message, user)
        self.leaderboard[server.id][user.id]["XP"] += int(randint(15, 20))

    def addtoleaderboard(self, message, user):
        server = message.server
        self.leaderboard[server.id][user.id] = {"username": user.name, "rank": 0, "XP": 0}
        dataIO.save_json(path + "/leaderboard.json", self.leaderboard)

    def getxplevel(self, level):
        xp = 5*(int(level)**2)+50*int(level)+100
        return xp

    def getuserrank(self, ctx, user):
        #TODO CHECK IF USER ARE IN DISCORD SERVER
        server = ctx.message.server
        if user.id in self.leaderboard[server.id]:
            return self.leaderboard[server.id][user.id]["rank"]
        else:
            return 0
    
    def getxp(self, ctx, user):
        server = ctx.message.server
        if user.id in self.leaderboard[server.id]:
            return self.leaderboard[server.id][user.id]["XP"]

    def isusermember(self, ctx, userid: int):
        member = ctx.message.server.get_member(userid)
        if member:
            return True
        else:
            return False

    def tell_nouser(self):
        #dunno whats going here yet
        return ""
        
    async def makeimage(self, user, rank, xp):
        no_profile_picture = Image.open(path + '/noimage.png')
        bordercolor = [0, 255, 0, 0]
        
        profile_area = Image.new("L", (512, 512), 0)
        
        draw = ImageDraw.Draw(profile_area)
        draw.ellipse(((0, 0), (512, 512)), fill=255)
        circle_img_size = tuple([128, 128])
        profile_area = profile_area.resize((circle_img_size), Image.ANTIALIAS)
        
        try:
            url = user.avatar_url.replace('webp?size=1024', 'png')
            url = url.replace('gif?size=1024', 'png')
            await self._get_profile(url)
            profile_picture = Image.open(path + '/tmp/profilepic.png')
        except:
            profile_picture = no_profile_picture
            
        profile_area_output = ImageOps.fit(profile_picture, (circle_img_size), centering=(0, 0))
        profile_area_output.putalpha(profile_area)    
        mask = Image.new('L', (512, 512), 0)
        draw_thumb = ImageDraw.Draw(mask)
        draw_thumb.ellipse((0, 0) + (512, 512), fill=255, outline=0)
        circle = Image.new("RGBA", (512, 512))
        draw_circle = ImageDraw.Draw(circle)
        draw_circle.ellipse([0, 0, 512, 512], fill=(bordercolor[0], bordercolor[1], bordercolor[2], 180), outline=(255, 255, 255, 250))
        circle_border_size = await self._circle_border(circle_img_size)
        circle = circle.resize((circle_border_size), Image.ANTIALIAS)
        circle_mask = mask.resize((circle_border_size), Image.ANTIALIAS)
        circle_pos = (67 + int((136 - circle_border_size[0]) / 2))
        border_pos = (71 + int((136 - circle_border_size[0]) / 2))
        #drawtwo = ImageDraw.Draw(welcome_picture)
            
            
            
            
            
            
            
            
            
            
            
    
    
        img = Image.open(rankimage)
        draw = ImageDraw.Draw(img)
        
        img.paste(circle, (circle_pos, circle_pos), circle_mask)
        img.paste(profile_area_output, (border_pos, border_pos), profile_area_output)
        
        
        
        
        imgpath = path + '/tmp/tmpout.png'
        fontsmall = ImageFont.truetype(fontpath, 40)
        fontbig = ImageFont.truetype(fontpath, 90)
        
        levelint_size = fontbig.getsize("45")
        levelint_x = 934-levelint_size[0]-50
        
        level_size = fontsmall.getsize("LEVEL")
        level_size_x = 934-50-levelint_size[0]-20-level_size[0]
        level_size_y = levelint_size[1] + 50 - level_size[1]
        
        
        
        
        #rankint_size = fontbig.getsize("#3545")
        #rank_size = fontsmall.getsize("RANK")
        
        
        
        draw.text((levelint_x, 50),"45",(255,255,255),font=fontbig)
        draw.text((level_size_x, level_size_y),"LEVEL",(255,255,255),font=fontsmall)
        
        #draw.text((380, 33),"#214412" + str(rank),(255,255,255),font=fontbig)
        #draw.text((150, 20),"LEVEL",(255,255,255),font=fontsmall)
        #draw.text((250, 20), str(xp),(255,255,255),font=fontsmall)
        image_object = BytesIO()
        img.save(image_object, format="PNG")
        image_object.seek(0)
        return image_object
        #with open(imgpath, 'rb') as f:
        #self.bot.send_file(ctx.message.channel, imgpath)
        #os.remove(imgpath)
        #sent = await self.bot.send_file(msg_dest, attachment, filename='captcha.png', content=content, embed=embed)
        
    async def _get_profile(self, url):
        async with self.session.get(url) as r:
            image = await r.content.read()
        with open(path + '/tmp/profilepic.png', 'wb') as f:
            f.write(image)
            
    async def _circle_border(self, circle_img_size: tuple):
        border_size = []
        for i in range(len(circle_img_size)):
            border_size.append(circle_img_size[0] + 8)
        return tuple(border_size)

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
    
    fp = path + "/settings.json"
    if not dataIO.is_valid_json(fp):
        print("Creating settings.json...")
        dataIO.save_json(fp, {})

def setup(bot):
    if pilAvailable:
        check_folders()
        check_files()
        n = XPLevels(bot)
        bot.add_listener(n.gainxp, "on_message")
        bot.add_cog(n)
    else:
        raise RuntimeError("You need to run 'pip3 install Pillow'")
