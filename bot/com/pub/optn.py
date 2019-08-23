#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["choose"],
                  help = 'fun',
                  brief = 'I choose something for you!',
                  usage = ';]choose {arg1} "{multi word arg2}" {...}',
                  description = 'ARGx [STR] - The choice itself')
@commands.check(enbl)
async def optn(ctx, *options):
    await ctx.send(f'```I choose >>{random.choice(options)}<< {random.choice(["0.0",">.<","9.6",":P",":D",";]"])}```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(optn)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('optn')
    print('GOOD')

