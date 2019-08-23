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
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'fun',
                  brief = 'Virtual Slot Machine',
                  usage = ';]slots',
                  description = '[NO ARGS FOR THIS COMMAND]')
@commands.check(enbl)
async def slots(ctx):
    slot = ["[*]","[X]","[Y]","[Z]","[1]","[2]",
                  "[3]","[0]","[V]","[U]","[@]",
                  "[%]","[#]","[P]","[+]","[/]",
                  "[*]","[>]","[<]","[;]","[!]",
                  "[]]","[?]","[+]","[[]","[*]",
                  "[A]","[B]","[C]","[:]","[-]","[X]"]
    slot1 = rand(1,len(slot)-1)
    slot2 = rand(1,len(slot)-1)
    slot3 = rand(1,len(slot)-1)
    slotsend = f'''
>  {slot[slot1-1]} {slot[slot2-1]} {slot[slot3-1]}
#] {slot[slot1]} {slot[slot2]} {slot[slot3]}
>  {slot[slot1+1]} {slot[slot2+1]} {slot[slot3+1]}'''
    if slot1 == slot2 == slot3:
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

