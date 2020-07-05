#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
from discord.ext import commands
import unicodedata as unidata
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = [],
    help = 'oth',
    brief = 'Dezalgoifies {text}',
    usage = ';]dezalgo {text}',
    description = '''\
TEXT [TEXT] - The content to dezalgoify
'''
)
@commands.check(enbl)
async def dezalgo(ctx, *, text):
    st = ""
    for ch in text:
        if "COMBINING" not in unidata.name(ch).upper():
            st += ch
    await ctx.send(st)


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(dezalgo)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('dezalgo')
    print('GOOD')
