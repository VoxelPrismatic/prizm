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

@commands.command(help = 'mod',
                  brief = 'Clears {x} messages from chat',
                  usage = ';]clr {x}',
                  description = 'X [INT] - The number of messages to clear')
@has_permissions(manage_messages=True)
@commands.check(enbl)
async def clr(ctx, arg: int):
    await ctx.channel.purge(limit=arg+1)

@commands.command(help = 'mod',
                  brief = 'Clears messages from {int1} to {int2} in chat',
                  usage = ';]clrin {int1} {int2}',
                  description = 'INTx [INT] - The message IDs to clear in between')
@commands.check(enbl)
@commands.has_permissions(manage_messages=True)
async def clrin(ctx, int1: int, int2: int):
    await ctx.message.delete()
    clrh = await ctx.fetch_message(min(int1, int2))
    clrl = await ctx.fetch_message(max(int1, int2))
    await ctx.channel.purge(limit=2000, before=clrl, after=clrh)

@commands.command(help = 'mod',
                  brief = 'Clears messages from {int1} to {int2} in chat',
                  usage = ';]clrto {mID}',
                  description = 'mID [INT] - The message ID to clear to')
@commands.check(enbl)
@commands.has_permissions(manage_messages=True)
async def clrto(ctx, mID: discord.Message):
    await ctx.channel.purge(limit=2000, before=ctx.message, after=mID)
    await ctx.message.delete()

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(clr)
    bot.add_command(clrin)
    bot.add_command(clrto)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('clr')
    bot.remove_command('clrin')
    bot.remove_command('clrto')
    print('GOOD')