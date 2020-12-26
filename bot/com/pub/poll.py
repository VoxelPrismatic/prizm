#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import os
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = [],
    help = 'fun',
    brief = 'Creates a poll',
    usage = ';]poll {text}',
    description = '''\
TEXT [TEXT] - The poll description
''')
@commands.check(enbl)
async def poll(ctx, *, text = ""):
    if not text:
        text = f"@{str(ctx.author)} should probably add a better description here..."
    msg = await ctx.send(
        embed = embedify.embedify(
            desc = f'```md\n#] POLL!```{text}',
            foot = "React √ If You Agree ;]"
        )
    )
    await msg.add_reaction('<:yes:614129663693946884>')
    await msg.add_reaction('<:no:614129709197819908>')
    await ctx.message.delete()

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(poll)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command(poll)
    print('GOOD')
