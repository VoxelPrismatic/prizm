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
                      brief = 'Sends the escaped contents of {message}',
                      usage = ';]md {message}',
                      description = '''\
MESSAGE [MESSAGE] - The target message, ID or URL
''')
@commands.check(enbl)
async def md(ctx, message: discord.Message):
    special = "*_~|`\\:#"
    x = message.content
    for y in special: x.replace(y,'\\'+y)
    await ctx.send(x)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(md)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('md')
    print('GOOD')

