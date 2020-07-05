#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os, tensorflow, dbl, scipy, cv2
import discord                    #python3.7 -m pip install -U discord.py
import logging
import numpy as np                #python3.7 -m pip install -U numpy
import numexpr as ne              #python3.7 -m pip install -U numexpr
import aiofiles, io, asyncio      #python3.7 -m pip install -U aiofiles
import matplotlib
import platform, sys, sysconfig, praw
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
import re
from util.pages import PageThis

def itms(itm):
    global lines, blank, comment, files, dirs, byte, types, folder
    if itm.name in ['.directory','__pycache__','bot-env'] or itm.name.endswith('.pyc'):
        return
    elif itm.is_file():
        if '.' not in itm.name:
            types['txt'] += 1
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
        dirs += 1
        folders.append(itm)

async def grab_dirs(lvl = "./"):
    lines = 0
    comment = 0
    blank = 0
    files = 0
    dirs = 0
    byte = 0
    strblock = False
    for f in os.listdir(lvl):
        if f.endswith(".py"):
            files += 1
            async with aiofiles.open(lvl + f) as g:
                t = await g.read()
            byte += len(t)
            for l in t.splitlines():
                lines += 1
                if l.strip() == "" and not strblock:
                    blank += 1
                if l.strip().startswith("#") or strblock:
                    comment += 1
                if l.count("'''") % 2 or l.count('"""') % 2:
                    strblock = not(strblock)
                if l.strip().startswith("'") or l.strip().startswith('"'):
                    comment += 1
        else:
            try:
                a, b, c, d, e, f = await grab_dirs(lvl + f)
                lines += a
                comment += b
                blank += c
                files += d
                dirs += e
                byte += f
            except:
                pass
    return lines, comment, blank, files, dirs, byte

def readlines(com):
    file = "/home/priz/Desktop/PRIZM/msc/stats.txt"
    open(file, "w+").write("")
    os.system(f"{com} > {file}")
    lines = open(file).read().split("\n")
    for line in range(len(lines)):
        lines[line] = re.sub(" +", " ", lines[line])
    return lines


##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases=["system","os","sys"],
    help = 'inf',
    brief = 'Shows what I\'m running on',
    usage = ';]os',
    description = '''\
[NO INPUT FOR THIS COMMAND]
'''
)
@commands.check(enbl)
async def _sysinfo(ctx):

    #Collect data
    async with ctx.channel.typing():
        platform = str(sysconfig.get_platform())
        pyver = str(sysconfig.get_python_version())
        lines = readlines("free")
        swap = int(lines[2].split(" ")[2])
        totalswap = int(lines[2].split(" ")[1])
        ram = int(lines[1].split(" ")[2])
        totalram = int(lines[1].split(" ")[1])
        lines = readlines("sensors")
        cpu_temps = [lines[8].split(" ")[2], lines[9].split(" ")[2]]
        lines = readlines("mpstat -A")
        cpu = []
        for x in range(4, 8):
            temp = 100 - float(lines[x].split(" ")[-1])
            cpu.append(f"{temp:.2f}%")
        lines = readlines('cat /proc/cpuinfo | grep "^[c]pu MHz"')
        spu = []
        for x in range(4):
            spu.append(int(float(lines[x].split(" ")[-1])))
        lines, comment, blank, files, dirs, byte = await grab_dirs()
    await PageThis(ctx,[f'''#] SYSTEM
  PLATFORM ] {platform}
    PYTHON ] {pyver}
#] DEPENDENCIES
       CV2 ] {cv2.__version__}
      PRAW ] {praw.__version__}
     NUMPY ] {np.__version__}
     DBLPY ] {dbl.__version__}
     SCIPY ] {scipy.__version__}
   NUMEXPR ] {ne.__version__}
   LOGGING ] {logging.__version__}
  AIOFILES ] {aiofiles.__version__}
DISCORD.PY ] {discord.__version__}
MATPLOTLIB ] {matplotlib.__version__}
TENSORFLOW ] {tensorflow.__version__}''',
f'''#] FILES AND THINGS
      DIRS ] {dirs}
     LINES ] {lines}
     BLANK ] {blank}
     FILES ] {files}
     BYTES ] {byte/(1024**2):.3f} KiB
  COMMENTS ] {comment}
CODE LINES ] {lines-blank-comment}''',
f'''#] RESOURCES
CPU 0 ] {cpu[0]:<7} [{spu[0]} Mhz - {cpu_temps[0]}]
CPU 1 ] {cpu[1]:<7} [{spu[1]} Mhz - {cpu_temps[0]}]
CPU 2 ] {cpu[2]:<7} [{spu[2]} Mhz - {cpu_temps[1]}]
CPU 3 ] {cpu[3]:<7} [{spu[3]} Mhz - {cpu_temps[1]}]
  RAM ] {ram/1048576:.2f} GiB/{totalram/1048576:.2f} GiB [{ram/totalram * 100:.2f}%]
 SWAP ] {swap/1048576:.2f} GiB/{totalswap/1048576:.2f} GiB [{swap/totalswap * 100:.2f}%]
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
