#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import ast
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import numpy as np                #python3.7 -m pip install -U numpy
import numexpr as ne              #python3.7 -m pip install -U numexpr
import datetime, time
import aiofiles, io, asyncio      #python3.7 -m pip install -U aiofiles
import matplotlib.pyplot as pyplt #python3.7 -m pip install -U matplotlib // SEE SITE FOR MORE
import matplotlib, math, statistics, random
import platform, sys, sysconfig, traceback, shlex
from shlex import quote
from ast import literal_eval
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions
bot = commands.Bot(command_prefix=";]")
bot.remove_command("help")
logging.basicConfig(level='INFO')

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)
def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)
async def log(head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
    return msgs
async def _io(TxT):
    msgs = await log("AI I/O", f'{TxT}')
    print(f']{TxT}')
    return msgs
async def com(command):
    msgs = await log("COMMAND USED", f'COMMAND // {command}')
    print(f']{command}')
    return msgs
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

class info(commands.Cog):
    def __init__(self, bot): self.bot = bot
    async def cog_command_error(self, ctx, error):
        await log("It fucked up :C", f'ERROR // {error}\n> TRACE // {sys.exc_info()}')
        await ctx.send(embed=embedify('GG, It fucked up. [Hopefully] all data was logged'))

    @commands.command(aliases=["help"])
    async def hlep(self,ctx):
        await ctx.author.send(embed=embedify('''```md
#] !] PRIZ AI ;] [! COMMANDS LIST``````md
] ";]hlep"
> Brings up this message :)
] ";]sys"
> Shows some sys info :P
] ";]ping"
> Shows the ping time :L
] ";]slots"
> Slot machine :D
] ";]coin {x}" [Option: {x}]
> Flips a virtual coin {x} times 0.0
] ";]git"
> Shows the github/gitlab repo ;]
] ";]rng {x} {y} {z}" [Option: {z}]
> Prints an RNG from {x} to {y}, {z} times
] ";]usrinfo"
> Shows your user info 0.0
] ";]dnd"
> Roles all dice from Dragons and Dungeons!
] ";]info"
> Shows additional info
] ";]cool {uID}"
> Gives someone [{userID}] a sneaky surpise ;D
] ";]rick"
> Rick Roll! °ω°
] ";]blkjck"
> BLACKJACK! 0o0
] ";]spam {x}"
> Spams {x} amount of chars >.<
] ";]graph {eq} {xmin} {xmax}"
> Graphs {eq} from {xmin} to {xmax} 9.6
] ";]rto {x} {y}"
> Reduces the ratio of {x} and {y} ;-;
] ";]rad {x}"
> Reduces a radical, {x}! >:D
] ";]react {mID} {reactions}" [{reaction}.split " "]
> Adds {reactions} to a given {mID} .-.
] ";]stats {data}"
> Gives stats given {data} ._.
] ";]quad {a} {b} {c}"
> Uses {a}, {b}, and {c} to solve the Quad Formula 0o0`````md
#] To see mod commands, use ";]hlepmod"
#] To have a conversation, use "]{your text here}""
#] Some of your data is stored, use ";]data" to see more
```'''))
        await com("HELP")

    @commands.command(aliases=["helpmod"])
    async def hlepmod(self, ctx):
        await ctx.author.send(embed=embedify('''```diff
-] !] PRIZ AI ;] [! MOD STUFF``````md
] ";]hlepmod"
> Brings up this message :)
] ";]ban {user} {delete days} {reason}"
> Bans a {user} and removes messages from {delete days} ago for a {reason}
] ";]kick {user}"
> Kicks a {user} from the server
] ";]clr {int}"
> Deletes a {int} amount of messages
] ";]clrin {messageID1} {messageID2}"
> Deletes messages between {messageID1} and {messageID2}
] ";]pin {mID}"
> Pins {mID}
] ";]unpin {mID}"
> Unpins {mID}``````diff
-] To see user commands, use ";]hlep"
-] To have a conversation, use "]{your text here}
-] Some of your data is stored, use ";]data" to see more"
```'''))
        await com("MOD HELP")

    @commands.command()
    async def data(self, ctx):
        await ctx.send(embed=embedify('''```md
#] HOW YOUR DATA IS USED
Data is only stored when talking to the bot directly,
using "]{message}" or using commands
This data is stored forever on the owner's computer
This data only stores your message content, and nothing
more.
If you do not feel comfortable with this, dont talk to
this bot, or just dont say bad things.
#] TL;DR // Only messages are stored when using "]{msg}"
#] and when you use commands```'''))
        await com('DATA USAGE')

    @commands.command()
    async def info(self, ctx):
        try:
            await ctx.send(embed=embedify('''```md
#] PRIZ AI
> An RNG based AI that compares strings... literally
> Originally written for the TI84+CSE and adapted into a way better Discord Bot!
> This is version [0]-RW, a rewritten version```'''))
            await com("BOT INFO")
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def ping(self, ctx):
        try:
            await ctx.send(embed=embedify(f'```md\n#] !] PONG ;] [!\n> Ping Time: {bot.latency}s```'))
            await com("PING TIME")
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def git(self, ctx):
        try:
            await ctx.send('''`]GITHUB PAGE` https://github.com/VoxelPrismatic/basic-ai/
    `]GITLAB PAGE` https://gitlab.com/VoxelPrismatic/basic-ai/''')
            await com("GITHUB/GITLAB")
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command(aliases=["system"])
    async def os(self, ctx):
        platform = str(sysconfig.get_platform())
        pyver = str(sysconfig.get_python_version())
        await ctx.send(embed=embedify(f'''```diff
+] !] PRIZ AI ;] [! SYSTEM INFO``````md
  PLATFORM // {platform}
    PYTHON // {pyver}
DISCORD.PY // {discord.__version__}
   LOGGING // {logging.__version__}
  AIOFILES // {aiofiles.__version__}
MATPLOTLIB // {matplotlib.__version__}
     NUMPY // {np.__version__}
   NUMEXPR // {ne.__version__}
```'''))
        await com("SYS INFO")

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    bot.add_cog(info(bot))
