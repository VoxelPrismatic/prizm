#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

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

@commands.command(help = 'fun',
                  brief = 'Adds reactions quickly and easily',
                  usage = ';]react {mID} {rct1} {rct2} {...}',
                  description = 'mID  [INT] - The message\nRCTx [ANY] - The reaction[s]')
@commands.check(enbl)
async def react(ctx, mID: discord.Message, *reactions):
    await ctx.message.delete()
    for reaction in reactions:
        if reaction.lower() in 'abcdefghijklmnopqrstuvwxyz':
            await message.add_reaction(eval('\\N{REGIONAL INDICATOR SYMBOL LETTER'+reaction.upper()+'}'))
        else:
            try:
                await message.add_reaction(reaction)
            except:
                await message.add_reaction(ctx.bot.get_emoji(int(reaction.split(":")[2][:-1])))

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

