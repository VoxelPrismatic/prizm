#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                  help = 'fun',
                  brief = 'esreveR',
                  usage = ';]rev {phrase}',
                  description = '''\
PHRASE [TEXT] - The stuff to reverse
''')
@commands.check(enbl)
async def rev(ctx, *, phrase):
    await ctx.send(phrase[::-1])

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rev)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rev')
    print('GOOD')

