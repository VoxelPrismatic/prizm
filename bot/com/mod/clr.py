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

@commands.command(help = 'mod',
                  brief = 'Clears {x} messages from chat',
                  usage = ';]clr {x}',
                  description = 'X [INT] - The number of messages to clear')
@has_permissions(manage_messages=True)
@commands.check(enbl)
async def clr(ctx, arg: int):
    await ctx.channel.purge(limit=arg+1)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(clr)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('clr')
    print('GOOD')
