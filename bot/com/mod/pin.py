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

@commands.command(aliases = [],
                  help = 'mod',
                  brief = 'Pins a message for you, useful on mobile',
                  usage = ';]pin {message}',
                  description = '''\
MESSAGE [MESSAGE] - The message you wish to pin, ID or URL
''')
@commands.check(enbl)
async def pin(ctx, message: discord.Message):
    await message.pin()

@commands.command(aliases = [],
                  help = 'mod',
                  brief = 'Pins a message for you, useful on mobile',
                  usage = ';]unpin {message}',
                  description = '''\
MESSAGE [MESSAGE] - The message you wish to unpin, ID or URL
''')
@commands.has_permissions(manage_messages=True)
@commands.check(enbl)
async def unpin(ctx, message: discord.Message):
    await message.unpin()
    await ctx.send('```md\n#] UNPINNED```', delete_after = 10.0)


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(pin)
    bot.add_command(unpin)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('pin')
    bot.remove_command('unpin')
    print('GOOD')

