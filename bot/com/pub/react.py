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
async def react(ctx, mID: int, *reactions):
    await ctx.channel.purge(limit = 1)
    message = await ctx.fetch_message(mID)
    for reaction in reactions:
        try: await message.add_reaction(reaction)
        except:
            try: await message.add_reaction(ctx.bot.get_emoji(int(reaction.split(":")[2][:-1])))
            except discord.HTTPException: await exc(ctx, 1)
            except discord.Forbidden: await exc(ctx, 2)
            except discord.NotFound: await exc(ctx, 3)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(react)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('react')
    print('GOOD')

