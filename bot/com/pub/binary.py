#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'fun',
                  brief = 'Converts binary to text, and text to binary',
                  usage = ';]binary {st}',
                  description = 'ST [STR] - The stuff to convert to/from binary')
@commands.check(enbl)
async def binary(ctx, *, st):
    try:
        try:
           sr = st.replace(' ', '')
           await ctx.send(embed=embedify.embedify(desc=f'{"".join([chr(int(sr[i:i+8], 2)) for i in range(0, len(sr), 8)])}'))
        except:
            await ctx.send(f'{"".join([chr(int(sr[i:i+8], 2)) for i in range(0, len(sr), 8)])}')
    except ValueError:
        try:
            await ctx.send(embed=embedify.embedify(desc=f'{"".join((bin(ord(x))[2:].zfill(8) for x in st))}'))
        except:
            await ctx.send(f'{"".join((bin(ord(x))[2:].zfill(8) for x in st))}')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(binary)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('binary')
    print('GOOD')

