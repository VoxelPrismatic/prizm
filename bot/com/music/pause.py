#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
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

@commands.command(aliases = ['resume', 'continue', 'stop'],
                  help = 'music',
                  brief = 'Toggles the music',
                  usage = ';]pause',
                  description = '''[NO INPUT FOR THIS COMMAND]''')
@commands.check(enbl)
async def pause(ctx):
    vcC = ctx.voice_client
    if vcC.is_playing():
        vcC.pause()
    else:
        vcC.resume()

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(pause)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('pause')
    print('GOOD')

