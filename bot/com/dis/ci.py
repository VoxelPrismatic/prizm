#!/chnl/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from typing import Union as Any
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = ["channelinfo", "infochannel", "ichannel", "channeli", "ichnl", "chnli"],
                  help = 'dis',
                  brief = 'Shows info about a given {channel}',
                  usage = ';]ci {channel}',
                  description = '''\
CHANNEL [CHANNEL] - The target channel, name or ping or ID
''')
@commands.check(enbl)
async def chnl(ctx, channel:Any[discord.VoiceChannel, discord.TextChannel]=None):
    if channel == None:
        channel = ctx.channel
    lit = [f"""
#] INFO FOR #{channel.name}
      ID ] {_chnl.id}
     POS ] {_chnl.position}
 CREATED ] {_chnl.created_at}
CATAGORY ] {_chnl.category.name}
"""]
    for thing in channel.overwrites:
        st = f"```diff\nOVERRIDE [{thing}] ]\n"
        for perm, val in channel.overwrites_for(thing):
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

