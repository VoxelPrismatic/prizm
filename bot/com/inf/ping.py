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

@commands.command(help = 'inf',
                  brief = 'Sends the ping time',
                  usage = ';]ping',
                  description = '[NO ARGS FOR THIS COMMAND]')
@commands.check(enbl)
async def ping(ctx):
    b = time.monotonic()
    msg = await ctx.send('```md\n#] PINGING\n> Please wait...```')
    ttl = time.monotonic() - b
    await msg.delete()
    await ctx.send(embed=embedify.embedify(desc=f'''```md\n#] PONG ;]
> PING // {str(float(ctx.bot.latency)*1000)[:10]}ms
>  ACK // {str(ttl*1000)[:10]}ms```'''))

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
