#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
async def find(ctx, fID:int):
    send = ''
    for chn in ctx.guild.channels: send+=f'> CHN ] #{str(chn)}\n' if chn.id==fID else ''
    for usr in ctx.guild.members: send+=f'> USR ] @{str(usr)}\n' if usr.id==fID else ''
    for emj in ctx.guild.emojis: send+=f'> EMJ ] :{emj.name}:\n' if emj.id==fID else ''
    for rol in ctx.guild.roles: send+=f'> ROL ] @'+str(rol).replace('@','')+'\n' if rol.id==fID else ''
    if fID == ctx.guild.id: send += f'> GLD ] {ctx.guild.name}'
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