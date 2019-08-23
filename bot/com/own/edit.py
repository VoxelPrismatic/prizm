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
async def edit(ctx, loc:str):
    if loc == 'com/own/edit.py':
        return await ctx.send('```diff\n-] DO NOT EDIT THE EDITOR YA DINGUS!!!```')
    elif loc == 'com/own/dump.py':
        return await ctx.send('```diff\n-] DO NOT EDIT THE DUMPER YA DINGUS!!!```')
    with open(f"/home/priz/Desktop/PRIZM/{loc}", "wb+") as end:
        end.write(await ctx.message.attachments[0].read())
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

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
