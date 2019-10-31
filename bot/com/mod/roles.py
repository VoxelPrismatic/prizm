#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from discord.ext.commands import Greedy as Grab
from chk.enbl import enbl
from util import ez

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                  help = 'mod',
                  brief = 'Adds or removes {role} from {user} for a {reason}',
                  usage = ';]role {member1} {?member2} {...member} {role1} {?role2} {...role} {?reason}',
                  description = '''\
MEMBER [MEMBER] - The target user, mention or name or ID
ROLE   [ROLE  ] - The target role, mention or name or ID
REASON [TEXT  ] - The reason for the action DEFAULT: "REQUESTED BY ] <name>"
*All roles given will toggle the role presence on ALL members given''')
@commands.check(enbl)
@commands.has_permissions(manage_roles=True)
async def roles(ctx, members: Grab[discord.Member], roles: Grab[discord.Role], *, reason=None):
    for mbr in members:
        mbr_roles = mbr.roles
        await mbr.remove_roles(*[role for role in roles if role in mbr_roles], reason = ez.ifstr(reason, f'REQUESTED BY ] @{str(ctx.author)}'))
        await mbr.add_roles(*[role for role in roles if role not in mbr_roles], reason = ez.ifstr(reason, f'REQUESTED BY ] @{str(ctx.author)}'))
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(roles)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('roles')
    print('GOOD')
