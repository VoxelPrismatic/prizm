#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os, psutil, tensorflow
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import numpy as np                #python3.7 -m pip install -U numpy
import numexpr as ne              #python3.7 -m pip install -U numexpr
import aiofiles, io, asyncio      #python3.7 -m pip install -U aiofiles
import matplotlib.pyplot as pyplt #python3.7 -m pip install -U matplotlib // SEE SITE FOR MORE
import matplotlib
import platform, sys, sysconfig
from util import embedify
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.pages import PageThis

def itms(itm):
    global lines, blank, comment, files, dirs, byte, types, folder
    if itm.name in ['.directory','__pycache__','bot-env'] or itm.name.endswith('.pyc'):
        return
    elif itm.is_file():
        if '.' not in itm.name:
            types['txt']+=1
        else:
            try:
                x = types[itm.name.split('.')[1]]
                types[itm.name.split('.')[1]] += 1
            except:
                types[itm.name.split('.')[1]] = 1

        byte+=itm.stat().st_size
        files += 1
        blockComm = False
        if '.' not in itm.name:
            return
        if itm.name.split('.')[1] != 'py':
            return
        for x in open(itm.path).readlines():
            lines+=1
            lines+=x.count(';')
            lines+=x.replace(':\n','').count(':')
            if x.strip().startswith('#') or blockComm:
                comment += 1
            elif x.strip()=='"""':
                comment += 1
                blockComm = not(blockComm)
            elif x.strip().startswith('"'):
                comment += 1
            elif x.strip().startswith("'"):
                comment += 1
            elif x.strip()=='':
                blank+=1
    else:
        dirs+=1
        folders.append(itm)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

global lines, blank, comment, files, dirs, byte, types, folders
lines = 0
blank = 0
comment = 0
files = 0
dirs = 0
byte = 0
types = {'txt':0}
folders = []

@commands.command(aliases=["system","os","sys"],
                  help = 'inf',
                  brief = 'Shows what I\'m running on',
                  usage = ';]os',
                  description = '[NO ARGS FOR THIS COMMAND]')

@commands.check(enbl)
async def _sysinfo(ctx):
    global lines, blank, comment, files, dirs, byte, types, folders
    lines = 0
    blank = 0
    comment = 0
    files = 0
    dirs = 0
    byte = 0
    types = {'txt':0}
    folders = []
    home = os.scandir('/home/priz/Desktop/PrizAI')
    for itm in home:
        itms(itm)

    while len(folders):
        for itm in os.scandir(folders[0].path): itms(itm)
        folders.pop(0)

    platform = str(sysconfig.get_platform())
    pyver = str(sysconfig.get_python_version())
    cpu = psutil.cpu_percent(interval=None,percpu=True)
    spu = psutil.cpu_freq(percpu=True)
    tpu = psutil.sensors_temperatures()['coretemp']
    swap = psutil.swap_memory()
    ram = psutil.virtual_memory()
    await PageThis(ctx,[f'''  PLATFORM // {platform}
    PYTHON // {pyver}
> --------
     NUMPY // {np.__version__}
   NUMEXPR // {ne.__version__}
   LOGGING // {logging.__version__}
  AIOFILES // {aiofiles.__version__}
DISCORD.PY // {discord.__version__}
MATPLOTLIB // {matplotlib.__version__}
TENSORFLOW // {tensorflow.__version__}''',
f'''      DIRS // {dirs}
     LINES // {lines}
     BLANK // {blank}
     FILES // {files}
     BYTES // {byte/1024:.5f} KiB
  COMMENTS // {comment}
CODE LINES // {lines-blank-comment}
> --------
      *.PY // {types['py']}
     *.TXT // {types['txt']}
    *.JSON // {types['json']}''',
f'''     CPU 0 // {cpu[0]}% [{spu[0].current} Mhz - {tpu[0].current}C]
     CPU 1 // {cpu[1]}% [{spu[1].current} Mhz - {tpu[0].current}C]
     CPU 2 // {cpu[2]}% [{spu[2].current} Mhz - {tpu[1].current}C]
     CPU 3 // {cpu[3]}% [{spu[3].current} Mhz - {tpu[1].current}C]
> --------
 RAM USAGE // {ram.used/1048576:.2f} MiB/{ram.total/1048576:.2f} MiB [{ram.percent}%]
SWAP USAGE // {swap.used/1048576:.2f} MiB/{swap.total/1048576:.2f} MiB [{swap.percent}%]
'''],'SYSTEM INFO')

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
