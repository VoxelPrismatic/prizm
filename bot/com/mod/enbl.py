#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from chk.gen import is_mod
from util import dbman
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl as en

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = ['enable'],
                      help = 'mod',
                      brief = 'Enables a {command}',
                      usage = ';]enbl {command}',
                      description = '''\
COMMAND [TEXT] - The name of the command you want to enable
''')
@commands.guild_only()
@commands.check(is_mod)
async def enbl(ctx, command):
    if not ctx.bot.get_command(nam):
        return ctx.send('```diff\n-] COMMAND DOESNT EXIST```')
    dbman.update('com', ctx.bot.get_command(command).name, 1, id=ctx.guild.id)
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

@commands.command(aliases=['disable'],
                  help = 'mod',
                  brief = 'Disables a {command}',
                  usage = ';]dsbl {command}',
                  description = '''\
COMMAND [TEXT] - The name of the command you want to disable
''')
@commands.guild_only()
@commands.check(is_mod)
async def dsbl(ctx, command):
    if not ctx.bot.get_command(nam):
        return ctx.send('```diff\n-] COMMAND DOESNT EXIST```')
    dbman.update('com', ctx.bot.get_command(command).name, 0, id=ctx.guild.id)
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

@commands.command(aliases=['prefix'],
                  help = 'mod',
                  brief = 'Changes the prefix to {pre}',
                  usage = ';]pre {pre}',
                  description = '''
PRE [TEXT] - The new prefix
''')
@commands.guild_only()
@commands.check(is_mod)
async def pre(ctx, pre):
    dbman.update('pre', 'pre', pre, id=ctx.guild.id)
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(enbl)
    bot.add_command(dsbl)
    bot.add_command(pre)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('enbl')
    bot.remove_command('dsbl')
    bot.remove_command('pre')
    print('GOOD')
