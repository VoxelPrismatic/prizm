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

@commands.command()
@commands.check(enbl)
async def mines(ctx, size:int=10, mines:int=10):
    if mines >= size*size-1: return await ctx.send('```diff\n-] TOO MANY MINES```')
    if size > 15: return await ctx.send('```diff\n-] SIZE TOO BIG```')
    def add(x,y,x2,y2,tbl):
        if x==x2 and y==y2: return tbl
        if x==-1 or y==-1: return tbl
        if tbl[x][y] == 'X': tbl[x2][y2] = str(int(tbl[x2][y2])+1)
        return tbl
    table = []
    for x in range(size):
       table.append([])
       for y in range(size): table[x].append('0')
    for z in range(mines): 
        x,y=rng(0,size-1),rng(0,size-1)
        while table[x][y] == 'X': x,y=rng(0,size-1),rng(0,size-1)
        table[x][y] = 'X'
    for x in range(size):
        for y in range(size):
            try: table = add(x,y+1,x,y,table);print(x,y)
            except: pass
            try: table = add(x,y-1,x,y,table)
            except: pass
            try: table = add(x+1,y,x,y,table)
            except: pass
            try: table = add(x-1,y,x,y,table)
            except: pass
            try: table = add(x+1,y+1,x,y,table)
            except: pass
            try: table = add(x+1,y-1,x,y,table)
            except: pass
            try: table = add(x-1,y+1,x,y,table)
            except: pass
            try: table = add(x-1,y-1,x,y,table)
            except: pass
    await ctx.send(embed=embedify.embedify(desc='||`['+']`||\n||`['.join(']`||||`['.join(x) for x in table)+']`||',foot=f'SIZE // {size}x{size} || MINES // {mines}'))


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
