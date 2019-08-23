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
@commands.has_permissions(manage_messages=True)
@commands.check(enbl)
async def pin(ctx, mID: discord.Message):
    await message.pin()

@commands.command()
@commands.has_permissions(manage_messages=True)
@commands.check(enbl)
async def unpin(ctx, mID: discord.Message):
    message = await ctx.fetch_message(mID)
    await ctx.send('```md\n#] UNPINNED```')


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

