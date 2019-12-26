#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
import io

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = ["hex"],
                  help = 'fun',
                  brief = 'Converts hex to text, and text to hex',
                  usage = ';]hexadecimal {text}',
                  description = '''\
TEXT [TEXT] - The stuff to convert to/from hex
''')
@commands.check(enbl)
async def hexadecimal(ctx, *, text):
    try:
        b = False
        st = ""
        sr = text.replace(' ', '').replace('\n', '')
        if len(sr) % 2:
            raise ValueError #Invalid hex
        for i in range(0, len(sr), 2):
            st += chr(int(sr[i:i+2], 16))
    except ValueError:
        b = True
        y = 0
        for x in text:
            z = hex(ord(x))[2:].zfill(2)
            if not(y % 16 and y != 0):
                st += "\n"
            y += 1
            st += z + " "
    t = io.BytesIO(st.encode("utf-8"))
    if b:
        if len(st) > 2040:
            await ctx.send(embed = embedify.embedify(
                      desc = "```diff\n-] TOO LONG TO SEND```", 
                      foot = "TXT -> HEX ;]"
                  ), file = discord.File(t, "HEX.TXT"))
        else:
            await ctx.send(embed = embedify.embedify(
                      desc = f"```\n{st}```", 
                      foot = "TXT -> HEX ;]"
                  ), file = discord.File(t, "HEX.TXT"))
    else:
        await ctx.send(embed = embedify.embedify(
                      desc = f"```\n{st}```", 
                      foot = "HEX -> TXT ;]"
                  ), file = discord.File(t, "HEX.TXT"))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hexadecimal)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hexadecimal')
    print('GOOD')

