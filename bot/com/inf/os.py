#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os, psutil, tensorflow, dbl, scipy, cv2
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
from util.pages import PageThis

async def grab_dirs(lvl = "/home/priz/Desktop/PRIZM/"):
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
                os.listdir(lvl + f)
                a, b, c, d, e, f = await grab_dirs(lvl + f + "/")
                lines += a
                comment += b
                blank += c
                files += d
                dirs += e + 1
                byte += f
            except NotADirectoryError:
                pass
            except Exception as ex:
                print(ex)
    return lines, comment, blank, files, dirs, byte

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = ["system", "os", "sys"],
    help = 'inf',
    brief = 'Shows what I\'m running on',
    usage = ';]os',
    description = '''\
[NO INPUT FOR THIS COMMAND]
'''
)
@commands.check(enbl)
async def _sysinfo(ctx):

    lines, comment, blank, files, dirs, byte = await grab_dirs()

    platform = str(sysconfig.get_platform())
    pyver = str(sysconfig.get_python_version())
    cpu = psutil.cpu_percent(interval = None, percpu = True)
    spu = psutil.cpu_freq(percpu = True)
    tpu = psutil.sensors_temperatures()['coretemp']
    swap = psutil.swap_memory()
    ram = psutil.virtual_memory()
    ramU = f"{ram.used / 1048576:.2f}"
    ramT = f"{ram.total / 1048576:.2f}"
    ramP = ram.percent
    swapU = f"{swap.used / 1048576:.2f}"
    swapT = f"{swap.total / 1048576:.2f}"
    swapP = swap.percent
    await PageThis(
        ctx,
        [
            f'''#] SYSTEM
  PLATFORM ] {platform}
    PYTHON ] {pyver}
#] DEPENDENCIES
       CV2 ] {cv2.__version__}
      PRAW ] {praw.__version__}
     NUMPY ] {np.__version__}
     DBLPY ] {dbl.__version__}
     SCIPY ] {scipy.__version__}
    PSUTIL ] {psutil.__version__}
   NUMEXPR ] {ne.__version__}
   LOGGING ] {logging.__version__}
  AIOFILES ] {aiofiles.__version__}
DISCORD.PY ] {discord.__version__} [hate this]
MATPLOTLIB ] {matplotlib.__version__}
TENSORFLOW ] {tensorflow.__version__}''',
            f'''#] FILES AND THINGS
      DIRS ] {dirs}
     LINES ] {lines}
     BLANK ] {blank}
     FILES ] {files}
     BYTES ] {byte / (1024 ** 1):.3f} KiB
  COMMENTS ] {comment}
CODE LINES ] {lines-blank-comment}''',
            f'''#] RESOURCES
     CPU 0 ] {cpu[0]}% [{spu[0].current} Mhz - {tpu[0].current}C]
     CPU 1 ] {cpu[1]}% [{spu[1].current} Mhz - {tpu[0].current}C]
     CPU 2 ] {cpu[2]}% [{spu[2].current} Mhz - {tpu[1].current}C]
     CPU 3 ] {cpu[3]}% [{spu[3].current} Mhz - {tpu[1].current}C]
 RAM USAGE ] {ramU} MiB/{ramT} MiB [{ramP}%]
SWAP USAGE ] {swapU} MiB/{swapT} MiB [{swapP}%]
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
