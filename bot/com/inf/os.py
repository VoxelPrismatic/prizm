#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os
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

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["system"])
async def os(ctx):
    platform = str(sysconfig.get_platform())
    pyver = str(sysconfig.get_python_version())
    await ctx.send(embed=embedify(f'''```md
#] !] PRIZ AI ;] [! SYSTEM INFO``````md
  PLATFORM // {platform}
    PYTHON // {pyver}
> -------
     NUMPY // {np.__version__}
   NUMEXPR // {ne.__version__}
   LOGGING // {logging.__version__}
  AIOFILES // {aiofiles.__version__}
DISCORD.PY // {discord.__version__}
MATPLOTLIB // {matplotlib.__version__}
```'''))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(os)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('os')
    print('GOOD')

