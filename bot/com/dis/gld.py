#!/gld/bin/env python3
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
                  brief = 'Shows info about this guild',
                  usage = ';]gld',
                  description = '[NO ARGS FOR THS COMMAND]')
@commands.check(enbl)
async def gld(ctx):
    _gld = ctx.guild
    chnls = []
    rols = []
    emjs = []
    lit = [f"""
      ID // {_gld.id}
     AFK // {_gld.afk_timeout} - {_gld.afk_channel}
    NAME // {_gld.name}
    DESC // {_gld.description}
  BANNER // {_gld.banner_url}
  REGION // {_gld.region}
  NOTIFS // {_gld.default_notifications}
 CREATED // {_gld.created_at}""",
            f""" MFA LVL // {_gld.mfa_level}
   OWNER // {_gld.owner}
   LARGE // {_gld.large}
FEATURES // {_gld.features}
VRFY LVL // {_gld.verification_level}
NUM MBRS // {_gld.member_count}"""]

    for channel in _gld.channels:
        if len(f"{', '.join(chnls)}, {channel.name}") > 2000:
            lit.append(f"CHANNELS // {', '.join(chnls)}")
            chnls = []
            chnls.append(f"{channel.name}")
        else:
            chnls.append(f"{channel.name}")

    if len(chnls) > 0:
        lit.append(f"CHANNELS // {', '.join(chnls)}")

    for role in _gld.roles:
        if len(f"{', '.join(rols)},{role.name}") > 2000:
            lit.append(f"ROLES // {', '.join(rols)}")
            rols = []
            rols.append(f"{role.name}")
        else:
            rols.append(f"{role.name}")

    if len(rols) > 0:
        lit.append(f"ROLES // {', '.join(rols)}")

    for emot in _gld.emojis:
        if len(f"{', '.join(emjs)},{emot.name}") > 2000:
            lit.append(f"EMOJI // {', '.join(emjs)}")
            emjs = []
            emjs.append(f"{emot.name}")
        else:
            emjs.append(f"{emot.name}")

    if len(emjs) > 0:
        lit.append(f"EMOJI // {', '.join(emjs)}")
    await pages.PageThis(ctx, lit, "GUILD INFO", thumb=str(_gld.icon_url).replace('webp','png'))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(gld)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('gld')
    print('GOOD')
