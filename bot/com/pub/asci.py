#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback
import random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from dyn.faces import faces

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                  help = 'fun',
                  brief = 'Just prints one of these cool ASCIImoji!',
                  usage = ';]asci',
                  description = '''\
[NO INPUT FOR THIS COMMAND]
''')
@commands.check(enbl)
async def asci(ctx):
    await ctx.send(random.choice(faces()))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(asci)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('asci')
    print('GOOD')

