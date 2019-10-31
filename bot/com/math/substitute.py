#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord
import typing, re
import logging
import numexpr as ne
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##
@commands.command(aliases = ['sub'],
                  help = 'math',
                  brief = 'Substitutes a number in for X',
                  usage = ';]substitute {num} {eq}',
                  description = '''\
NUM [NUMBER] - The thing X is equal to
EQ  [TEXT  ] - The equation to solve
''')
@commands.check(enbl)
async def substitute(ctx, num: float, *, eq: str):
    eq = eq.replace('^','**').lower().strip()
    eq = re.sub(r"(\d+)([xy\(])", r"\1*\2", re.sub(r"([xy\)])(\d+)",r"\1*\2",eq))
    eq = eq.replace('pi', str(np.pi)).replace('\u03c0', str(np.pi)).replace("e", str(math.e))
    eq = re.sub(r"(^[xy][^><]=[^><])?([^><]=[^><][xy]$)?", "", eq)
    eq = re.sub(r"([xy\d])\(", r"\1*(", re.sub(r"\)([xy\d])", r")*\1", eq))
    eq = re.sub(r"(\d+)root\((.*)\)", r"(\2)^(1/\1)", eq)
    async with ctx.channel.typing():
        await ctx.send(f'```md\n#] {ne.evaluate(eq.replace("x", f"({num})"))}```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(substitute)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('substitute')
    print('GOOD')
