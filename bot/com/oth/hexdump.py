#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import io
from discord.ext import commands
from util.hexdump import hexdump as hd
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = ["hexedit"],
    help = 'oth',
    brief = 'A hex editor, without the editor',
    usage = ';]hexdump',
    description = '''\
FILE [ATTACHMENT] - The file to dump the hex data of
'''
)
@commands.check(enbl)
async def hexdump(ctx):
    files = ctx.message.attachments
    if not len(files):
        return await ctx.send("```diff\n-] PLEASE ATTACH A FILE```")
    data = await files[0].read()
    ls = [f"{byte:02x}" for byte in data]
    stdout = hd(ls)[0]
    file = io.BytesIO(stdout.encode())
    await ctx.send(
        "```md\n#] HERE YE GO, MATE```",
        file = discord.File(file, "hexdata.txt")
    )

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hexdump)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hexdump')
    print('GOOD')

