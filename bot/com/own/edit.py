#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
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

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def edit(ctx, loc:str):
    if loc.endswith('edit.py'): return await ctx.send('```diff\n-] DO NOT EDIT THE EDITOR YA DINGUS!!!```')
    if loc.endswith('dump.py'): return await ctx.send('```diff\n-] DO NOT EDIT THE DUMPER YA DINGUS!!!```')
    with open(f"/home/priz/Desktop/PrizAI/{loc}", "wb+") as end:
        end.write(await ctx.message.attachments[0].read())
    await ctx.message.add_reaction("\N{OK HAND SIGN}")

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(edit)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('edit')
    print('GOOD')