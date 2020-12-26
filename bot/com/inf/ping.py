#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, time
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = [],
    help = 'inf',
    brief = 'Sends the ping time',
    usage = ';]ping',
    description = '''\
[NO INPUT FOR THIS COMMAND]
'''
)
@commands.check(enbl)
async def ping(ctx):
    start = time.monotonic()
    msg = await ctx.send('```md\n#] PINGING...```')
    send = time.monotonic() - start
    start = time.monotonic()
    await msg.add_reaction("\U0001f3d3")
    react = time.monotonic() - start
    start = time.monotonic()
    await msg.edit(content="```diff\n-] PINGING...```")
    edit = time.monotonic() - start
    start = time.monotonic()
    await msg.delete()
    delete = time.monotonic() - start
    await ctx.send(embed=embedify.embedify(desc=f'''```md\n#] PONG ;]
>   PING ] {float(ctx.bot.latency)*1000:.3f}ms
>   SEND ] {send*1000:.2f}ms
>   EDIT ] {edit*1000:.2f}ms
>  REACT ] {react*1000:.2f}ms
> DELETE ] {delete*1000:.2f}ms
```'''))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(ping)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('ping')
    print('GOOD')
