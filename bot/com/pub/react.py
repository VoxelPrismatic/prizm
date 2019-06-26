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

@commands.command()
@commands.check(enbl)
async def react(ctx, mID: int, *reactions):
    await ctx.channel.purge(limit = 1)
    message = await ctx.fetch_message(mID)
    for reaction in reactions:
        if reaction.lower() in 'abcdefghijklmnopqrstuvwxyz': await message.add_reaction({
                'a':'\N{REGIONAL INDICATOR SYMBOL LETTER A}',
                'b':'\N{REGIONAL INDICATOR SYMBOL LETTER B}',
                'c':'\N{REGIONAL INDICATOR SYMBOL LETTER C}',
                'd':'\N{REGIONAL INDICATOR SYMBOL LETTER D}',
                'e':'\N{REGIONAL INDICATOR SYMBOL LETTER E}',
                'f':'\N{REGIONAL INDICATOR SYMBOL LETTER F}',
                'g':'\N{REGIONAL INDICATOR SYMBOL LETTER G}',
                'h':'\N{REGIONAL INDICATOR SYMBOL LETTER H}',
                'i':'\N{REGIONAL INDICATOR SYMBOL LETTER I}',
                'j':'\N{REGIONAL INDICATOR SYMBOL LETTER J}',
                'k':'\N{REGIONAL INDICATOR SYMBOL LETTER K}',
                'l':'\N{REGIONAL INDICATOR SYMBOL LETTER L}',
                'm':'\N{REGIONAL INDICATOR SYMBOL LETTER M}',
                'n':'\N{REGIONAL INDICATOR SYMBOL LETTER N}',
                'o':'\N{REGIONAL INDICATOR SYMBOL LETTER O}',
                'p':'\N{REGIONAL INDICATOR SYMBOL LETTER P}',
                'q':'\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
                'r':'\N{REGIONAL INDICATOR SYMBOL LETTER R}',
                's':'\N{REGIONAL INDICATOR SYMBOL LETTER S}',
                't':'\N{REGIONAL INDICATOR SYMBOL LETTER T}',
                'u':'\N{REGIONAL INDICATOR SYMBOL LETTER U}',
                'v':'\N{REGIONAL INDICATOR SYMBOL LETTER V}',
                'w':'\N{REGIONAL INDICATOR SYMBOL LETTER W}',
                'x':'\N{REGIONAL INDICATOR SYMBOL LETTER X}',
                'y':'\N{REGIONAL INDICATOR SYMBOL LETTER Y}',
                'z':'\N{REGIONAL INDICATOR SYMBOL LETTER Z}'}[reaction.lower()])
        else:
            try: await message.add_reaction(reaction)
            except:await message.add_reaction(ctx.bot.get_emoji(int(reaction.split(":")[2][:-1])))

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

