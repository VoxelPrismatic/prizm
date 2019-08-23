#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions


##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def iedit(ctx, loc:str, mID: discord.Message):
    with open(f"/home/priz/Desktop/PRIZM/{loc}", "wb+") as end:
        end.write(mID.content.encode())
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(iedit)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('iedit')
    print('GOOD')
