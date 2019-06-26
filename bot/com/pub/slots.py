#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import random
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)
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
async def slots(ctx):
    slot = ["[*]","[X]","[Y]","[Z]","[1]","[2]",
            "[3]","[0]","[V]","[U]","[@]",
            "[%]","[#]","[P]","[+]","[/]",
            "[*]","[>]","[<]","[;]","[!]",
            "[]]","[?]","[+]","[[]","[*]","[X]"]
    slot1 = rand(1,len(slot)-1)
    slot2 = rand(1,len(slot)-1)
    slot3 = rand(1,len(slot)-1)
    slotsend = f'''
> {slot[slot1-1]}{slot[slot2-1]}{slot[slot3-1]}
# {slot[slot1]}{slot[slot2]}{slot[slot3]}<
> {slot[slot1+1]}{slot[slot2+1]}{slot[slot3+1]}'''
    if slot1 == slot2 and slot2 == slot3:
        await ctx.send(embed=embedify.embedify(desc=f'```md\n{slotsend}``````diff\n+] WIN!```'))
    else:
        await ctx.send(embed=embedify.embedify(desc=f'```md\n{slotsend}``````diff\n-] LOSS```'))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(slots)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('slots')
    print('GOOD')

