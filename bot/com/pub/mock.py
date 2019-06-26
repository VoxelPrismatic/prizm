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

@commands.command()
@commands.check(enbl)
async def mock(ctx,msg:discord.Message=None):
    await ctx.message.delete()
    await asyncio.sleep(.5)
    if not msg: msg = (await ctx.channel.history(limit=1).flatten())[0]
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