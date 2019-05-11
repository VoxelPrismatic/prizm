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
async def rick(self, ctx):
    try: await ctx.send(embed=embedify('''Never gonna give you up!
Never gonna let you down!
Never gonna run around and, desert you!
Never gonna make you cry!
Never gonna say goodbye!
Never gonna run around and, desert you!'''))
    except: ctx.send('''Never gonna give you up!
Never gonna let you down!
Never gonna run around and, desert you!
Never gonna make you cry!
Never gonna say goodbye!
Never gonna run around and, desert you!''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rick)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rick')
    print('GOOD')
