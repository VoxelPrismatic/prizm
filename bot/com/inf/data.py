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
async def data(ctx): await ctx.send(embed=embedify.embedify(desc='''```md
#] HOW YOUR DATA IS USED
Data is only stored when talking to the bot directly,
using "]{message}" or using commands
This data is stored forever on the owner's computer
This data only stores your message content, and nothing
more.
If you do not feel comfortable with this, dont talk to
this bot, or just dont say bad things.
#] TL;DR // Only messages are stored when using "]{msg}" or "}{msg}"
#] and when you use commands or you create en/disable a command or
#] create a tag
>  but that data is only used for this bot, i [PRIZ#9244] not selling it```'''))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(data)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('data')
    print('GOOD')

