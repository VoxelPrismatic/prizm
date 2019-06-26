#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os, psutil
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
import platform, sys, sysconfig, traceback, shlex, os
from shlex import quote
from util import embedify
from ast import literal_eval
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["system","os","sys"])
@commands.check(enbl)
async def _sysinfo(ctx):
    lines = 0; blank = 0; comment = 0; files = 0; dirs = 0; byte = 0; 
    types = {'txt':0}; folders = []
    home = os.scandir('/home/priz/Desktop/PrizAI')
    for itm in home:
        if itm.name in ['.directory','__pycache__','bot-env'] or itm.name.endswith('.pyc'): continue
        elif itm.is_file():
            if '.' not in itm.name: types['txt']+=1
            else:
                try: 
                    x = types[itm.name.split('.')[1]]
                    types[itm.name.split('.')[1]] += 1
                except: types[itm.name.split('.')[1]] = 1
            byte+=itm.stat().st_size; files += 1
            for x in open(itm.path).readlines():
                lines+=1
                if x.startswith('#'): comment+=1
                if x=='\n':blank+=1
        else: dirs+=1; folders.append(itm)
    while len(folders):
        for itm in os.scandir(folders[0].path):
            if itm.name in ['.directory','__pycache__','bot-env'] or itm.name.endswith('.pyc'): continue
            if itm.is_file():
                if '.' not in itm.name: types['txt']+=1
                else:
                    try: 
                        x = types[itm.name.split('.')[1]]
                        types[itm.name.split('.')[1]] += 1
                    except: types[itm.name.split('.')[1]] = 1
                byte+=itm.stat().st_size; files += 1
                for x in open(itm.path).readlines():
                    lines+=1
                    if x.startswith('#'): comment+=1
                    if x=='\n':blank+=1
            else: dirs+=1; folders.append(itm)
        folders.pop(0)
    platform = str(sysconfig.get_platform())
    pyver = str(sysconfig.get_python_version())
    await ctx.send(embed=embedify.embedify(desc=f'''```md
#] !] PRIZ AI ;] [! SYSTEM INFO``````md
  PLATFORM // {platform}
    PYTHON // {pyver}
> --------
     NUMPY // {np.__version__}
   NUMEXPR // {ne.__version__}
   LOGGING // {logging.__version__}
  AIOFILES // {aiofiles.__version__}
DISCORD.PY // {discord.__version__}
MATPLOTLIB // {matplotlib.__version__}
> --------
      DIRS // {dirs}
     LINES // {lines}
     BLANK // {blank}
     FILES // {files}
     BYTES // {byte/1024:.5f} KiB
  COMMENTS // {comment}
CODE LINES // {lines-blank-comment}
> --------
      *.PY // {types['py']}
     *.TXT // {types['txt']}
    *.JSON // {types['json']}
```'''))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(_sysinfo)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('_sysinfo')
    print('GOOD')

