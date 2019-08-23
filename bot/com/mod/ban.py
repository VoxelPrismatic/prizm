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

@commands.command(help = 'mod',
                  brief = 'Bans {member} for {reason} and deletes their messages from the past {x} days',
                  usage = ';]ban {mbr1} {mbr2} {...} {?num} {?rsn}',
                  description = '''\
MBRx [MEMBER] - The target member, ID or ping or name
NUM  [INT   ] - Delete messages from the past {x} days
RSN  [STR   ] - The reason for the ban''')
@commands.check(enbl)
@has_permissions(ban_members=True)
async def ban(ctx, members: commands.Greedy[discord.Member],
                delete_days: typing.Optional[int] = 0, *, reason: str):
    for member in members:
        await member.ban(reason=reason if reason else f'REQUESTED BY ] {str(ctx.author)}')
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(ban)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('ban')
    print('GOOD')

