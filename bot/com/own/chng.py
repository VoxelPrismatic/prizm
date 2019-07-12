#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import random
import discord                    #python3.7 -m pip install -U discord.py
import logging
from dyn import faces
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def chng(ctx, *, name:str=None):
    if len(name) != 0: 
        await ctx.bot.change_presence(activity=discord.Activity(type=3, name=name,url='https://discord.gg/Z84Nm6n'))
        return await ctx.message.add_reaction('\N{OK HAND SIGN}')
    face = faces.faces()
    texts = faces.texts()
    await ctx.bot.change_presence(activity=discord.Activity(type=3,
                              name=f"{random.choice(texts)} {random.choice(face)}",
                              url='https://discord.gg/Z84Nm6n'))
    await ctx.message.add_reaction('\N{OK HAND SIGN}')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(chng)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('chng')
    print('GOOD')
