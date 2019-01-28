from discord.ext import commands
from .utils.chat_formatting import pagify, box
from .utils.dataIO import dataIO
from .utils import checks
import asyncio
import os
import re

path = 'data/kaktuscog/custcomimproved'
json = path + 'commands.json'

__author__ = "DasKaktus (DasKaktus#5299)"
__version__ = "1.0"


class CustomCommandsImproved:
    """Custom commands Improved."""

    def __init__(self, bot):
        self.bot = bot
        data = dataIO.load_json(json)
        self.cust_commands = data.get('COMMANDS', {})

    def save(self):
        data = {'COMMANDS': self.cust_commands,
                }
        dataIO.save_json(json, data)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def setcom(self, ctx, command: str, isdm: str, *, text):
        """Adds a custom command

        Example:
        !setcom yourcommand 1/0 Text you want
		The 1/0 represent if it should dm the response or not (1 = true, 0 = false)
        """
        command = command.lower()
        server = ctx.message.server
        if server.id not in self.cust_commands:
            self.cust_commands[server.id] = {}
        if command in self.bot.commands:
            await self.bot.say("That command is already a normal command.")
            return

        if command not in self.cust_commands[server.id]:
            self.cust_commands[server.id][command] = {}
            self.cust_commands[server.id][command]["response"] = text
            self.cust_commands[server.id][command]["isdm"] = isdm
            self.save()
            await self.bot.say("Custom command successfully added.")
        else:
            await self.bot.say("This command already exists. Are you sure "
                               "you want to redefine it? [y/N]")
            response = await self.bot.wait_for_message(author=ctx.message.author)

            if response.content.lower().strip() in ['y', 'yes']:
                self.cust_commands[server.id][command]["response"] = text
                self.cust_commands[server.id][command]["isdm"] = isdm
                self.save()
                await self.bot.say("Custom command successfully set.")
            else:
                await self.bot.say("OK, leaving that command alone.")

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def rmcom(self, ctx, command: str):
        """Removes a custom command

        Example:
        !rmgcom yourcommand"""
        command = command.lower()
        server = ctx.message.server
        if command in self.cust_commands[server.id]:
            self.cust_commands[server.id].pop(command)
            self.save()
            await self.bot.say("Custom command successfully deleted.")
        else:
            await self.bot.say("That command doesn't exist.")

    @commands.command(pass_context=True)
    async def lscom(self, ctx):
        """Shows custom commands list"""
        server = ctx.message.server
        if self.cust_commands[server.id]:
            sections = []
            #for command, isdm, text in sorted(self.cust_commands[server.id].items()):
            for command in sorted(self.cust_commands[server.id].items()):
                item = 'Name:    ' + command
                item += '\nText:    ' + self.cust_commands[server.id][command]["response"]
                item += '\nSend DM: ' + self.cust_commands[server.id][command]["isdm"]
                sections.append(item)

            for cmds in pagify('\n\n'.join(sections)):
                await self.bot.say(box(cmds))
        else:
            await self.bot.say("There are no custom commands defined. "
                               "Use setcom [command] [isdm=1 or 0] [text]")

    @commands.group(pass_context=True, invoke_without_command=True)
    @checks.is_owner()
    async def acom(self, ctx, command=None):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.lscom)

    async def on_message(self, message):
        msg = message.content
        server = message.server
        prefix = await self.get_prefix(message)
        if not self.bot.user_allowed(message) or not prefix:
            return

        cmd = msg[len(prefix):]
        cmd = cmd.lower()
        if cmd in self.cust_commands[server.id]:
            ret = self.cust_commands[server.id][cmd]["response"]
            ret = self.format_cc(ret, message)
            if message.author.id == self.bot.user.id:
                await self.bot.edit_message(message, ret)
            else:
                if self.cust_commands[server.id][cmd]["isdm"]:
                    await self.bot.send_message(message.author, ret)
                else:
                    await self.bot.send_message(message.channel, ret)

    async def get_prefix(self, msg):
        prefixes = self.bot.command_prefix
        if callable(prefixes):
            prefixes = prefixes(self.bot, msg)
            if asyncio.iscoroutine(prefixes):
                prefixes = await prefixes

        for p in prefixes:
            if msg.content.startswith(p):
                return p
        return None

    def format_cc(self, command, message):
        results = re.findall("\{([^}]+)\}", command)
        for result in results:
            param = self.transform_parameter(result, message)
            command = command.replace("{" + result + "}", param)
        return command

    def transform_parameter(self, result, message):
        """
        For security reasons only specific objects are allowed
        Internals are ignored
        """
        raw_result = "{" + result + "}"
        objects = {
            "message": message,
            "author": message.author,
            "channel": message.channel,
            "server": message.server
        }
        if result in objects:
            return str(objects[result])
        try:
            first, second = result.split(".")
        except ValueError:
            return raw_result
        if first in objects and not second.startswith("_"):
            first = objects[first]
        else:
            return raw_result
        return str(getattr(first, second, raw_result))
		


def check_folders():
    if not os.path.exists(path):
        print("Creating " + path + " folder...")
        os.makedirs(path)


def check_files():
    if not dataIO.is_valid_json(json):
        print("Creating empty %s" % json)
        default = {'COMMANDS': {},
                   '_CGCOM_VERSION': 2
                   }
        dataIO.save_json(json, default)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(CustomCommandsImproved(bot))
