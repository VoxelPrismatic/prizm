#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def info(ctx): await ctx.send('''```md
#] PRIZ AI
> An RNG based AI that compares strings... literally
> Originally written for the TI84+CSE and adapted into a way better Discord Bot!
> This is version [0]-RW, a rewritten version
> Yes, the above version number is a joke 0.0```''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(info)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('info')
    print('GOOD')

