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

@commands.command(aliases=["userinfo", "useri", "usri", "iuser", "iusr"],
                  help = 'dis',
                  brief = 'Shows info for a given {user}',
                  usage = ';]ui {usr}',
                  description = 'USR [MEMBER] - The member you want info on')
@commands.check(enbl)
async def ui(ctx, _usr:discord.User=None):
    if _usr==None: _usr=ctx.author
    await ctx.send(embed=embedify.embedify(title='USER INFO ;]', desc=f'''```md
#] INFO FOR @{_usr.name}#{_usr.discriminator}
     ID ] {_usr.id}
    BOT ] {_usr.bot}
   NICK ] {_usr.display_name}
  COLOR ] {_usr.color}
CREATED ] {_usr.created_at}```''',
    thumb=_usr.avatar_url))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(ui)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('ui')
    print('GOOD')

