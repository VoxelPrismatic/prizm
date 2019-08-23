#!/chnl/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help='dis',
                  brief='Shows info about a given {text_channel}',
                  usage=';]chnl {txt_chnl}',
                  description='TXT CHNL [TEXT CHANNEL] - The target channel')
@commands.check(enbl)
async def chnl(ctx, _chnl:discord.TextChannel=None):
    if _chnl == None:
        _chnl = ctx.channel
    lit = [f"""
     ID // {_chnl.id}
    POS // {_chnl.position}
   NAME // {_chnl.name}
  GROUP // {_chnl.category.name}
CREATED // {_chnl.created_at}"""]
    for thing in _chnl.overwrites:
        st = f"```diff\nOVERRIDE [{thing}] //\n"
        for perm, val in _chnl.overwrites_for(thing):
            if str(val) == 'None':
                st += f'=] {perm} - [/] {str(val)}'
            elif str(val) == 'True':
                st += f'+] {perm} - [+] {str(val)}'
            elif str(val) == 'False':
                st += f'-] {perm} - [-] {str(val)}'
        lit.append(st+'```')
    await pages.PageThis(ctx, lit, "CHANNEL INFO")


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(chnl)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('chnl')
    print('GOOD')

