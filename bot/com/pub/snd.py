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

@commands.command(aliases = ['send'],
                  help = 'fun',
                  brief = 'I send {text} to a given {channel}',
                  usage = ';]snd {channel} {text}',
                  description = '''\
CHANNEL [CHANNEL] - The channel you want the message in, name or ping or ID
TEXT    [TEXT   ] - The text to send
''')
@commands.check(enbl)
async def snd(ctx, channel: discord.TextChannel, *, text):
    await ctx.message.delete()
    try:
        await channel.send(content=text)
    except:
        await channel.send('```diff\n-] I CAN\'T ACCESS THAT CHANNEL```')


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
