#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'dis',
                  brief = 'Shows info for a given {user}',
                  usage = ';]usr {usr}',
                  description = 'USR [MEMBER] - The member you want info on')
@commands.check(enbl)
async def usr(ctx, _usr:discord.User=None):
    if _usr==None: _usr=ctx.author
    await ctx.send(embed=embedify.embedify(desc=f'''```
     ID // {_usr.id}
    BOT // {_usr.bot}
   USER // {_usr.name}
   NICK // {_usr.display_name}
  COLOR // {_usr.color}
 JOINED // {_usr.joined_at}
CREATED // {_usr.created_at}
DISCRIM // {_usr.discriminator}```''',
    thumb=str(_usr.avatar_url)))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(usr)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('usr')
    print('GOOD')

