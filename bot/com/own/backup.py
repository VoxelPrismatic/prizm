#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import math, cmath
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
import zipfile as zp
import bz2
from datetime import datetime as dt
import os

valid_exts = [
    ".py",
    ".kdev4",
    ".sqlite3",
    ".pickle",
    ".json",
    ".txt",
    ".md",
    ".mplstyle",
]

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

def grab_dirs(lvl = "./"):
    ls = []
    for f in os.listdir(lvl):
        if "." in f and f != ".kdev4":
            if any(f.endswith(x) for x in valid_exts):
                ls.append(lvl + f)
        elif f != "__pycache__":
            try:
                ls.extend(grab_dirs(lvl + f + "/"))
            except NotADirectoryError:
                pass
    return ls

@commands.command()
@commands.is_owner()
async def backup(ctx):
    now = dt.now()
    name = f"PRIZM_{now.month:02}-{now.day:02}-{now.year:04}.zip"
    msg = await ctx.send(f"```md\n#] BACKING UP TO '{name}'```")
    zf = zp.ZipFile(
        "/home/priz/Desktop/" + name, "w",
        compresslevel = 9, compression = zp.ZIP_BZIP2
    )
    for f in grab_dirs():
        zf.write(f)
    zf.close()
    await ctx.send(
        "```md\n#] ZIPPED ;]```",
        file = discord.File("/home/priz/Desktop/" + name, name)
    )
    await msg.delete()

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(backup)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('backup')
    print('GOOD')
