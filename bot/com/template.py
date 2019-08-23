#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os
import ast
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import numpy as np                #python3.7 -m pip install -U numpy
import numexpr as ne              #python3.7 -m pip install -U numexpr
import datetime, time
import aiofiles, io, asyncio      #python3.7 -m pip install -U aiofiles
import matplotlib.pyplot as pyplt #python3.7 -m pip install -U matplotlib // SEE SITE FOR MORE
import matplotlib, math, statistics, random
import platform, sys, sysconfig, traceback, shlex
from shlex import quote
from ast import literal_eval
from util import embedify, pages
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help='cat',
                  brief='',
                  usage=';]',
                  description='[NO ARGS FOR THIS COMMAND]')
@commands.check(enbl)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(name)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('name')
    print('GOOD')

