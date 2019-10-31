#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util import ez

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=['memberinfo', 'infomember', 'imember', 'memberi',
                           'infombr', 'mbrinfo', 'mbri', 'imbr'],
                  help='dis',
                  brief='Shows info on a given {member}',
                  usage=';]mi {mbr}',
                  description='MBR [MEMBER] - The target member, ID or ping or name')
@commands.check(enbl)
async def mi(ctx, _mbr:discord.Member=None):
    if _mbr==None:
        _mbr=ctx.author
    Tgp = [perm for perm, value in _mbr.guild_permissions if value == True]
    Tcp = [perm for perm, value in _mbr.permissions_in(ctx.channel) if value == True]
    Ftp = [perm for perm, value in _mbr.guild_permissions if value == False]
    Fcp = [perm for perm, value in _mbr.permissions_in(ctx.channel) if value == False]
    Ngp = [perm for perm, value in _mbr.guild_permissions if value == None]
    Ncp = [perm for perm, value in _mbr.permissions_in(ctx.channel) if value == None]
    await ctx.send(embed=embedify.embedify(desc=f'''```md
#] INFO FOR @{_mbr.name}#{_mbr.discriminator}
     ID ] {_mbr.id}
    BOT ] {_mbr.bot}
   NICK ] {_mbr.display_name}
  COLOR ] {_mbr.color}
  ROLES ] {', '.join('&'+role.name for role in _mbr.roles)}
 JOINED ] {_mbr.joined_at}
 STATUS ] {_mbr.status} on {ez.ifstr(_mbr.desktop_status, "", "PC")} | \
{ez.ifstr(_mbr.web_status, "", "WEB")} | \
{ez.ifstr(_mbr.mobile_status, "", "PHONE")}
BOOSTED ] Since {ez.ifstr(_mbr.premium_since, 'never')} UTC
CREATED ] {_mbr.created_at}``````diff
+] {', '.join(set(Tgp) | set(Tcp))}``````diff
-] {', '.join(set(Fgp) | set(Fcp))}
=] {', '.join(set(Ngp) | set(Ncp))}```''',
        thumb = str(_mbr.avatar_url).replace('webp','png')))


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(mi)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('mi')
    print('GOOD')
