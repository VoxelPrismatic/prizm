#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback
from util import embedify, jsonSave, getPre
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

bot = commands.Bot(command_prefix=getPre.getPre)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen()
async def on_command_completion(ctx):
    jsonSave.saver(ctx.bot)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+LIS')
    bot.add_listener(on_command_completion)
    print('GOOD')

def teardown(bot):
    print('-LIS')
    bot.remove_listener('on_command_completion')
    print('GOOD')
