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

@commands.command(
    aliases = [
        'memberinfo', 
        'infomember',
        'imember',
        'memberi',
        'infombr',
        'mbrinfo', 
        'mbri',
        'imbr'
        ],
    help = 'dis',
    brief = 'Shows info on a given {member}',
    usage = ';]mi {member}',
    description = '''\
MEMBER [MEMBER] - The target member, ID or ping or name
'''
)
@commands.check(enbl)
async def mi(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    allowed_perms = []
    denied_perms = []
    default_perms = []
    for perm, val in member.permissions_in(ctx.channel):
        if val is True:
            allowed_perms.append(perm)
        elif val is False:
            denied_perms.append(perm)
        else:
            default_perms.append(perm)
    for perm, val in member.guild_permissions:
        if val is True and val not in allowed_perms and val not in denied_perms:
            allowed_perms.append(perm)
            if perm in default_perms:
                default_perms.remove(perm)
        elif val is False and val not in allowed_perms and val not in denied_perms:
            denied_perms.append(perm)
            if perm in default_perms:
                default_perms.remove(perm)
        elif perm not in default_perms:
            default_perms.append(perm)
    roles = []
    for role in member.roles:
        if len(roles) % 2:
            roles.append("> " + role.name)
        else:
            roles.append("] " + role.name)
    await ctx.send(
        embed = embedify.embedify(
            desc = f'''```md
#] INFO FOR @{member.name}#{member.discriminator}
     ID ] {member.id}
    BOT ] {member.bot}
   NICK ] {member.display_name}
  COLOR ] {member.color}
 JOINED ] {member.joined_at}
 STATUS ] {member.status} on {ez.ifstr(member.desktop_status, "", "PC")} | \
{ez.ifstr(member.web_status, "", "WEB")} | \
{ez.ifstr(member.mobile_status, "", "PHONE")}
BOOSTED ] Since {ez.ifstr(member.premium_since, 'never')} UTC
CREATED ] {member.created_at}```''',
            fields = [
                [
                    "PERMISSIONS IN THIS CHANNEL", 
                    f'''```diff
+] {', '.join(allowed_perms) or "[NONE]"}
-] {', '.join(denied_perms) or "[NONE]"}
=] {', '.join(default_perms) or "[NONE]"}```''',
                    False
                ], [
                    "ROLES",
                    "```md\n" + "\n".join(roles) + "```",
                    False
                ]
            ],
            thumb = str(member.avatar_url).replace('webp','png')
        )
    )


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
