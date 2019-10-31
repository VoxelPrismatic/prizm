#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                  help = 'fun',
                  brief = 'Adds reactions quickly and easily',
                  usage = ';]react {message} {reactions...}',
                  description = '''\
MESSAGE   [MESSAGE] - The message, URL or ID
REACTIONS [ANY    ] - The reaction[s], can be letters, custom, or default
    ''')
@commands.check(enbl)
async def react(ctx, mID: discord.Message, *reactions):
    await ctx.message.delete()
    for reaction in reactions:
        if reaction.lower() in 'abcdefghijklmnopqrstuvwxyz':
            await mID.add_reaction(eval('"\\N{REGIONAL INDICATOR SYMBOL LETTER '+reaction.strip().upper()+'}"'))
        else:
            try:
                await mID.add_reaction(reaction)
            except:
                await mID.add_reaction(ctx.bot.get_emoji(int(reaction.split(":")[2][:-1])))

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
