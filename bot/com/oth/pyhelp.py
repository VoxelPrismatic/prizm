#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord    
import logging, typing
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.prawUser import usr
from util.embedify import embedify

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["compy", "pyhelp", "hleppy", "pyhlep"],
                  help = "oth",
                  usage = ";]pyhelp {module} {command}",
                  brief = "Shows the entire command from a module",
                  description = """MODULE  [STR] - The module the command is located in, like decimal or math
COMMAND [STR] - The command you want, like solvers.solve or complex""")
async def pycom(ctx, module: str, command: str):
   text = open(f"/usr/lib/python3.7/{module}{'/'+'/'.join(command.split('.')[:-1]) if '.' in command else ''}.py").readlines()
   fn = command.split('.')[-1]
   lineno = 0
   for line in text:
       if line.startswith("def "+fn):
           break
       elif line.startswith("async def "+fn):
           break
       lineno += 1
   comtxt = ""
   for line in text[lineno:]:
       if line.startswith("def "):
           break
       elif line.startswith("async def "):
           break
       comtxt += line
   open("msc/pycom.py", "w+").write(comtxt)
   await ctx.send(f"```md\n#] HERE IS THE '{module}.{command}' COMMAND", file = discord.File("msc/pycom.py"))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(pycom)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('pycom')
    print('GOOD')
