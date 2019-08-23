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

@commands.command(help='mod',
                  brief = 'Changes the nickname of a {member} to {this}',
                  usage = ';]nick {mbr} {this}',
                  description = 'MBR  [MEMBER] - The target member, ID or ping or name\nTHIS [STR   ] - The nickname')
@has_permissions(manage_nicknames=True)
@commands.check(enbl)
async def nick(ctx, mbr: discord.Member, *, nm: str=''):
    await mbr.edit(nick=nm)
    await ctx.send(f'```md\n#] SUCCESS\n> {mbr.name} >> {nm}```')

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

