#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from discord.utils import find

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help='inf',
                  brief='Finds a meta object given an ID or name',
                  usage=';]find {fID}',
                  description = 'fID [STR] - The name or ID of the thing to find')
@commands.check(enbl)
async def find(ctx, *, fID):
    send = ''
    for chn in ctx.guild.channels: send+=f'> CHN ] #{str(chn)}\n' if fID in [str(chn.id),chn.name] else ''
    for usr in ctx.guild.members: send+=f'> USR ] @{str(usr)}\n' if fID in [str(usr.id),usr.name] else ''
    for emj in ctx.guild.emojis: send+=f'> EMJ ] :{emj.name}:\n' if fID in [str(emj.id),emj.name] else ''
    for rol in ctx.guild.roles: send+=f'> ROL ] @'+str(rol).replace('@','')+'\n' if fID in [str(rol.id),rol.name] else ''
    if fID == ctx.guild.name: send += f'> GLD ] {ctx.guild.name}'
    await ctx.send('```md\n'+(send if send else '> [NONE]')+'```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(find)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('find')
    print('GOOD')
