#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import typing
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                      help = 'mod',
                      brief = 'Changes the nickname of a {member} to {this}',
                      usage = ';]nick {member} {nickname}',
                      description = '''\
MEMBER   [MEMBER] - The target member, name or ping or ID
NICKNAME [TEXT  ] - The nickname
''')
@commands.check(enbl)
async def nick(ctx, member: discord.Member, *, nickname: str=''):
    await mbr.edit(nick=nickname)
    await ctx.send(f'```md\n#] SUCCESS\n> @{str(member)} >> {nickname}```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(nick)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('nick')
    print('GOOD')

