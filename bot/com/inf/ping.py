#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
async def ping(ctx):
    await ctx.send(embed=embedify.embedify(desc=f'```md\n#] !] PONG ;] [!\n> Ping Time: {str(float(ctx.bot.latency)*1000)[:10]}ms```'))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(ping)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('ping')
    print('GOOD')
