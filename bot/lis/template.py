#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback
from util import embedify, pages, json, getPre
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

bot = commands.Bot(command_prefix=getPre.getPre)

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##



##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+LIS')
    bot.add_listener(name)
    print('GOOD')

def teardown(bot):
    print('-LIS')
    bot.remove_listener('name')
    print('GOOD')

