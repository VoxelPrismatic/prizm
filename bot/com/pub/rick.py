#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
async def rick(ctx):
    try: await ctx.send(embed=embedify.embedify(title = "!] RICK ROLL ;] [!", desc='''Never gonna give you up!
Never gonna let you down!
Never gonna run around and, desert you!
Never gonna make you cry!
Never gonna say goodbye!
Never gonna run around and, desert you!'''))
    except: ctx.send('''Never gonna give you up!
Never gonna let you down!
Never gonna run around and, desert you!
Never gonna make you cry!
Never gonna say goodbye!
Never gonna run around and, desert you!''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rick)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rick')
    print('GOOD')
