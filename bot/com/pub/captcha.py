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

@commands.command(help='fun',
                  brief='Are you a bot?',
                  usage=';]captcha {mbr}',
                  description='MBR [MEMBER] A member, ping or name or ID')
@commands.check(enbl)
async def captcha(ctx, mbr: discord.Member):
    if mbr.bot:
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
