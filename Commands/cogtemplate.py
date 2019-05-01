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

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

class cogname(commands.Cog):
    def __init__(self, bot): self.bot = bot
    async def cog_command_error(self, ctx, error):
        await log("It fucked up :C", f'ERROR // {error}\n> TRACE // {sys.exc_info()}')
        await ctx.send(embed=embedify('GG, It fucked up. [Hopefully] all data was logged'))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    bot.add_cog(cogname(bot))
