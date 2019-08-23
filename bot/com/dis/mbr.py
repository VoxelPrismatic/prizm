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

@commands.command(help='dis',
                  brief='Shows info on a given {member}',
                  usage=';]mbr {mbr}',
                  description='MBR [MEMBER] - The target member, ID or ping or name')
@commands.check(enbl)
async def mbr(ctx, _mbr:discord.Member=None):
    if _mbr==None:
        _mbr=ctx.author
    gperms = ', '.join(perm for perm, value in _mbr.guild_permissions if value)
    cperms = ', '.join(perm for perm, value in _mbr.permissions_in(ctx.channel) if value)
    await ctx.send(embed=embedify.embedify(desc=f'''```
     ID // {_mbr.id}
    BOT // {_mbr.bot}
   USER // {_mbr.name}
   NICK // {_mbr.display_name}
  COLOR // {_mbr.color}
  ROLES // {', '.join(role.name for role in _mbr.roles)}
 JOINED // {_mbr.joined_at}
 MOBILE // {_mbr.is_on_mobile()}
 STATUS // {_mbr.status}
CREATED // {_mbr.created_at}
DISCRIM // {_mbr.discriminator}``````diff
+ GLD PERM // {gperms}``````diff
- CNL PERM // {cperms}```''',
        thumb = str(_mbr.avatar_url).replace('webp','png')))


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(mbr)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('mbr')
    print('GOOD')
