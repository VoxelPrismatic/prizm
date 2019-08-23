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

@commands.command()
@commands.check(enbl)
@commands.has_permissions(manage_messages=True)
async def clrin(ctx, int1: int, int2: int):
    await ctx.channel.purge(limit=1)
    clrh = await ctx.fetch_message(min(int1, int2))
    clrl = await ctx.fetch_message(max(int1, int2))
    await ctx.channel.purge(limit=2000, before=clrl, after=clrh)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(clrin)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('clrin')
    print('GOOD')

