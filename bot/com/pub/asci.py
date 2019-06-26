#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback
import random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl


##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
async def asci(ctx):
    face = ["0.0",">.<","0o0","9.6","@.@",
            ";-;","!-!","S:Γ","UwU",";]",
            ";n;",",,,;n;,,,",";u;","\\\\[T]/",
            ">~<","=-=","B)",":D","q.p"]
    await ctx.send(random.choice(face))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(asci)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('asci')
    print('GOOD')

