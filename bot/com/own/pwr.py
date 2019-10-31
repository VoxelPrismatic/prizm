#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import sys
from dyn import refresh
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

def uext(name, bot): bot.unload_extension(name); print(f'>Uext {name}')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def pwr(ctx):
        allext, lodtxt = refresh.refresh()
        for ext in range(len(allext)):
            for com in allext[ext]: 
                try:
                    uext(f"{lodtxt[ext]}{com}", ctx.bot)
                except: pass
        msg = await ctx.send('```md\n#] UNLOADING EXTENSIONS```')
        channel = ctx.bot.get_channel(556247032701124650)
        await channel.purge(limit=10)
        await msg.edit(content='```md\n#] LOGGING OUT```')
        await ctx.bot.close()

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(pwr)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('pwr')
    print('GOOD')

