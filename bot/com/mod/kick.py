#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@has_permissions(kick_members=True)
async def kick(ctx, *members: discord.Member):
    await ctx.channel.purge(limit=1)
    for member in members:
        try: await kick(member, reason=f"REQUESTED BY {ctx.author}")
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(kick)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('kick')
    print('GOOD')

