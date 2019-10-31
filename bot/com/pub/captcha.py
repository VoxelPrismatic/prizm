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

@commands.command(aliases = [],
                  help = 'fun',
                  brief = 'Are you a bot?',
                  usage = ';]captcha {member}',
                  description = '''\
MEMBER [MEMBER] - The member to test, they may fail
''')
@commands.check(enbl)
async def captcha(ctx, mbr: discord.Member):
    if mbr.bot or not random.randint(0, 2):
        await ctx.send('''```diff
- ______________________________
- |                            |
- | [X] You are a robot        |
- |____________________________|```''')
    else:
        await ctx.send('''```md
# ______________________________
# |                            |
# | [\u221a] You are a human        |
# |____________________________|```''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(captcha)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('captcha')
    print('GOOD')
