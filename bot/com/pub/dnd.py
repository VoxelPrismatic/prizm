#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from random import randint as rand
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                  help = 'fun',
                  brief = 'Rolls all the dice from DnD',
                  usage = ';]dnd',
                  description = '''\
[NO INPUT FOR THIS COMMAND]
''')
@commands.check(enbl)
async def dnd(ctx):
    await ctx.send(embed=embedify.embedify(desc=f"""```md
#] DND!
>  D4 ] {rand(1,4)}
>  D6 ] {rand(1,6)}
>  D8 ] {rand(1,8)}
> D10 ] {rand(1,10)}
> D12 ] {rand(1,12)}
> D20 ] {rand(1,20)}```"""))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(dnd)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('dnd')
    print('GOOD')

