#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text, thumb): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d).set_thumbnail(url=thumb)
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def mbr(ctx, *, _mbr:discord.Member):
    try:
        gperms = ', '.join(perm for perm, value in _mbr.guild_permissions if value)
        cperms = ', '.join(perm for perm, value in _mbr.permissions_in(ctx.channel) if value)
        await ctx.send(embed=embedify(f'''```
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
- CNL PERM // {cperms}```''', _mbr.avatar_url))
    except discord.HTTPException: await exc(ctx, 1)
    except discord.Forbidden: await exc(ctx, 2)
    except discord.NotFound: await exc(ctx, 3)


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

