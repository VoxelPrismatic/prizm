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
                  help = 'mod',
                  brief = 'Clears {num} messages from chat',
                  usage = ';]clr {num}',
                  description = 'NUM [NUMBER] - The number of messages to clear')
@has_permissions(manage_messages=True)
@commands.check(enbl)
async def clr(ctx, num: int):
    await ctx.channel.purge(limit=num+1)

@commands.command(aliases=[],
                  help = 'mod',
                  brief = 'Clears messages from {message1} to {message2} in chat [exclusively]',
                  usage = ';]clrin {message1} {message2}',
                  description = 'MESSAGEx [MESSAGE] - The messages to clear between, ID or URL')
@commands.check(enbl)
@commands.has_permissions(manage_messages=True)
async def clrin(ctx, message1: discord.Message, message2: discord.Message):
    await ctx.message.delete()
    if message1.created_at > message2.created_at:
        message1, message2 = message2, message1
    await ctx.channel.purge(limit=2000, before=clrl, after=clrh)

@commands.command(aliases=[],
                  help = 'mod',
                  brief = 'Clears all messages to a given {message} [exclusively]',
                  usage = ';]clrto {message}',
                  description = 'MESSAGE [MESSAGE] - The message to clear to, ID or URL')
@commands.check(enbl)
@commands.has_permissions(manage_messages=True)
async def clrto(ctx, message: discord.Message):
    await ctx.channel.purge(limit=2000, before=ctx.message, after=message)
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
