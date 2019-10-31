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

@commands.command(aliases = ['choose'],
                  help = 'fun',
                  brief = 'I choose something for you!',
                  usage = ';]choose {option1} | {option2} | {...}',
                  description = '''
OPTIONx [TEXT] - The option... duh
''')
@commands.check(enbl)
async def optn(ctx, *, options = "nothing... there was nothing to choose"):
    await ctx.send(f'```I choose >>{random.choice(options.split("|"))}<< {random.choice(["0.0",">.<","9.6",":P",":D",";]"])}```')

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

