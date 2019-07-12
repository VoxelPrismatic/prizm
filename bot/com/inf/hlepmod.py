#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio, json
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
] ";]ban {user} {delete days} {?reason}"
> Bans a {user} and removes messages from {delete days} ago for a {reason}
] ";]kick {user}"
> Kicks a {user} from the server
] ";]clr {int}"
> Deletes a {int} amount of messages
] ";]clrin {messageID1} {messageID2}"
> Deletes messages between {messageID1} and {messageID2}
] ";]mng {word,mod} {+,-,act} {modName,words,action}"
> Adds/removes/edits {modName,words,action} - given {+}, {-}, or {act}
] ";]pin {mID}"
> Pins {mID}
] ";]unpin {mID}"
> Unpins {mID}
] ";]enable {name}"
> Enables the {name} command // Server owner only
] ";]disable {name}"
> Disables the {name} command // Server owner only
] ";]prefix {prefix}"
> Sets the prefix to {prefix} // Server owner only
] ";]role {user} {+,-} {role} {?reason}"
> Adds or removes a {role} from {user} for {reason} - given {+} or {-}"""]
    await pages.PageThis(ctx, lit, "MOD STUFF", f"""```md
-] {'{?stuff}'} - Optional argument
-] To see user commands, use "{json.load(open('prefixes.json'))[str(ctx.guild.id)] if isinstance(ctx.channel, discord.TextChannel) else ';]'}hlep"
-] To have a conversation, use "]<txt>" or "{'}<txt>'}"
-] Some of your data is stored, use "{json.load(open('prefixes.json'))[str(ctx.guild.id)] if isinstance(ctx.channel, discord.TextChannel) else ';]'}data" to see more```""")

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
