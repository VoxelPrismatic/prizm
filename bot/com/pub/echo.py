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

@commands.command(aliases=[],
                  help = "fun",
                  brief = "Echo echo echo!",
                  usage = ";]echo {text}",
                  description = '''\
TEXT [TEXT] - What to echo
''')
@commands.check(enbl)
async def echo(ctx, *, text):
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(content=text)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(echo)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('echo')
    print('GOOD')

