#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from random import randint as rng
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = ["minesweeper"],
    help = 'fun',
    brief = 'Sweep mines away',
    usage = ';]mines {?size} {?mines}',
    description = '''\
SIZE  [NUMBER] - X by X tiles
MINES [NUMBER] - How many mines
'''
)
@commands.check(enbl)
async def mines(ctx, size:int=10, mines:int=10):
    if mines >= size*size-1:
        return await ctx.send('```diff\n-] TOO MANY MINES```')
    if size > 15:
        return await ctx.send('```diff\n-] SIZE TOO BIG```')
    table = []
    for y in range(size):
        table.append([])
        for x in range(size):
           table[y].append(0)
    for z in range(mines):
        x, y = rng(0, size - 1), rng(0, size - 1)
        while table[y][x] == 'X':
            x, y = rng(0, size - 1), rng(0, size - 1)
        table[y][x] = 'X'
        for dX in [-1, 0, 1]:
            for dY in [-1, 0, 1]:
                if (dX == 0 and dY == 0) or y + dY < 0 or x + dX < 0:
                    continue
                try:
                    table[y + dY][x + dX] += 1
                except (IndexError, TypeError):
                    pass
    st = ""
    for y in range(size):
        for x in range(size):
            if table[y][x] == "X":
                st += "||***`[X]`***||"
            else:
                st += f"||`[{table[y][x]}]`||"
        st += "\n"
    await ctx.send(
        embed = embedify.embedify(
            desc = st,
            foot = f'SIZE ] {size}x{size} || MINES ] {mines}'
        )
    )


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(mines)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command(mines)
    print('GOOD')
