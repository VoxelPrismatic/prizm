#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from discord.ext.commands import Greedy as Grab
from util.ez import ifstr
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                      help = 'mod',
                      brief = 'Kicks {member} for {reason}',
                      usage = ';]kick {member1} {member2} {...} {memberX} {?reason}',
                      description = '''\
MEMBERx [MEMBER] - The target member[s], name or ping or ID
REASON  [TEXT  ] - The reason for the ban
''')
@commands.check(enbl)
async def kick(ctx, members: Grab[discord.Member], *, reason: str = None):
    for member in members:
        await member.kick(reason = ifstr(reason, f'REQUESTED BY ] {str(ctx.author)}'))
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(kick)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('kick')
    print('GOOD')

