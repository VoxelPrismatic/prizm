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

@commands.command(help='mod',
                  brief = 'Kicks a {member}',
                  usage = ';]kick {mbr1} {mbr2} {...}',
                  description = 'MBRx [MEMBER] - The target member, ID or ping or name')
@commands.check(enbl)
@has_permissions(kick_members=True)
async def kick(ctx, *members: discord.Member):
    for member in members:
        await kick(member, reason=f"REQUESTED BY {ctx.author}")
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

