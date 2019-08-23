#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def dump(ctx, loc:str):
    if 'secrets.txt' in loc.lower():
        return await ctx.send('```diff\n-] FILE NOT ALLOWED```')
    try:
        await ctx.send(file=discord.File(fp=open(f"/home/priz/Desktop/PRIZM/{loc}", "rb")))
    except FileNotFoundError:
        await ctx.send('```diff\n-] FILE NOT FOUND```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(dump)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('dump')
    print('GOOD')
