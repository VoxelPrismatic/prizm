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

@commands.command(aliases = ["bin"],
                  help = 'fun',
                  brief = 'Converts binary to text, and text to binary',
                  usage = ';]binary {text}',
                  description = '''\
TEXT [TEXT] - The stuff to convert to/from binary
''')
@commands.check(enbl)
async def binary(ctx, *, text):
    try:
        b = False
        st = ""
        sr = text.replace(' ', '').replace('\n', '')
        if len(sr) % 8:
            raise ValueError #If each byte is not 8 bits long
        for i in range(0, len(sr), 8):
            st += chr(int(sr[i:i+8], 2))
    except ValueError:
        b = True
        y = 0
        for x in text:
            z = bin(ord(x))[2:].zfill(8)
            if not(y % 8 and y != 0):
                st += "\n"
            y += 1
            st += z + " "
    t = io.BytesIO(st.encode("utf-8"))
    if b:
        if len(st) > 2040:
            await ctx.send(embed = embedify.embedify(
                      desc = "```diff\n-] TOO LONG TO SEND```", 
                      foot = "TXT -> BIN ;]"
                  ), file = discord.File(t, "BIN.TXT"))
        else:
            await ctx.send(embed = embedify.embedify(
                      desc = f"```\n{st}```", 
                      foot = "TXT -> BIN ;]"
                  ), file = discord.File(t, "BIN.TXT"))
    else:
        await ctx.send(embed = embedify.embedify(
                      desc = f"```\n{st}```", 
                      foot = "BIN -> TXT ;]"
                  ), file = discord.File(t, "BIN.TXT"))

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

