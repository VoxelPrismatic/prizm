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

@commands.command(aliases=['send'],
                  help = 'fun',
                  brief = 'I send {text} to a given {channel}',
                  usage = ';]snd {cID} {mCTX}',
                  description = 'cID  [INT] - The Channel ID\nmCTX [STR] - The text to send')
@commands.check(enbl)
async def snd(ctx, cID: discord.TextChannel, *, mCTX):
    await ctx.message.delete()
    try:
        await cID.send(content=mCTX)
    except:
        await ctx.send('```diff\n-]WOOPS\n=]Make sure i have access to that channel UwU```')


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(snd)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('snd')
    print('GOOD')