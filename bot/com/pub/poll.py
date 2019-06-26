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

@commands.command()
@commands.check(enbl)
async def poll(ctx, *, txt):
        await ctx.channel.purge(limit=1)
        msg = await ctx.send(embed=embedify.embedify(desc=f'```md\n#] POLL!\n> {txt}```',foot="React √ If You Agree ;]"))
        await msg.add_reaction('\u2705')
        await msg.add_reaction('\u274C')

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
