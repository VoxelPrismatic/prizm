#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import typing
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = [],
    help = 'fun',
    brief = 'Adds reactions quickly and easily',
    usage = ';]react {message} {reactions...}',
    description = '''\
MESSAGE   [MESSAGE] - The message, URL or ID
REACTIONS [ANY    ] - The reaction[s], can be letters, custom, or default
'''
)
@commands.check(enbl)
async def react(ctx, message: typing.Optional[discord.Message] = None, *reactions):
    await ctx.message.delete()
    if message is None:
        message = (await ctx.channel.history(limit = 1).flatten())[0]
    for reaction in reactions:
        if reaction.lower() in 'abcdefghijklmnopqrstuvwxyz':
            await message.add_reaction(
                eval('"\\N{REGIONAL INDICATOR SYMBOL LETTER ' + reaction.strip().upper() + '}"')
            )
        elif reaction.lower() in "0123456789":
            numbers = {
                "0": "zero",
                "1": "one",
                "2": "two",
                "3": "three",
                "4": "four",
                "5": "five",
                "6": "six",
                "7": "seven",
                "8": "eight",
                "9": "nine"
            }
            await message.add_reaction(
                eval('"\\N{DIGIT ' + numbers[reaction].upper() + '}\ufe0f\u20e3"')
            )
        else:
            try:
                await message.add_reaction(reaction)
            except:
                await message.add_reaction(
                    ctx.bot.get_emoji(int(reaction.split(":")[2][:-1]))
                )

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
