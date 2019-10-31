#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, random, asyncio
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                  help = 'fun',
                  brief = 'iM nOt MoCkInG yOu',
                  usage = ';]mock {?message}',
                  description = '''\
MESSAGE [MESSAGE] - The message you want me to mock, ID or URL
> Will use the latest message in chat if not specified
''')
@commands.check(enbl)
async def mock(ctx,msg:discord.Message=None):
    await ctx.message.delete()
    if not msg:
        msg = (await ctx.channel.history(limit=1).flatten())[0]
    await ctx.send(''.join([x.upper() if random.randint(0,1) else x.lower() for x in msg.content]))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(mock)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('mock')
    print('GOOD')
