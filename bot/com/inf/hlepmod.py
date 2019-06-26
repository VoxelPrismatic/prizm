#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x00ffff)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["helpmod","modhlep","modhelp"])
async def hlepmod(ctx):
    lit = ["""
] ";]hlepmod"
> Brings up this message :)
] ";]ban {user} {delete days} {reason}"
> Bans a {user} and removes messages from {delete days} ago for a {reason}
] ";]kick {user}"
> Kicks a {user} from the server
] ";]clr {int}"
> Deletes a {int} amount of messages
] ";]clrin {messageID1} {messageID2}"
> Deletes messages between {messageID1} and {messageID2}""",
            """] ";]pin {mID}"
> Pins {mID}
] ";]unpin {mID}"
> Unpins {mID}
] ";]enable {name}"
> Enables the {name} command // Server owner only
] ";]disable {name}"
> Disables the {name} command // Server owner only
] ";]prefix {prefix}"
> Sets the prefix to {prefix} // Server owner only"""]
    await pages.PageThis(ctx, lit, "MOD STUFF", '''```diff
-] To see mod commands, use ";]hlepmod"
-] To have a conversation, use "]<your text here>"
-] To have a better conversation, use "}<your text here>"
-] Some of your data is stored, use ";]data" to see more
```''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hlepmod)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hlepmod')
    print('GOOD')