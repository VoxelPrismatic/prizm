#!/emj/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'dis',
                  brief = 'Displays info on a given {message}',
                  usage = ';]msg {msg}',
                  description = 'MSG [INT] - The ID of the target message')
@commands.check(enbl)
async def msg(ctx, _msg:discord.Message):
    lit = [f"""
     ID // {_msg.id}
    TTS // {_msg.tts}
    URL // {_msg.jump_url}
   USER // {_msg.author}
   CHNL // {_msg.channel}
 PINNED // {_msg.pinned}
 EDITED // {_msg.edited_at}
CREATED // {_msg.created_at}""", f"""
MENTION //
> USER ] {', '.join([mbr.name for mbr in _msg.mentions])}
> CHNL ] {', '.join([cnl.name for cnl in _msg.channel_mentions])}
> ROLE ] {', '.join([cnl.name for cnl in _msg.role_mentions])}
"""]
    if len(_msg.reactions) > 0:
        for r in _msg.reactions:
            usrs = await r.users().flatten()
            lit.append(f"REACTIONS [{r.emoji.name if r.custom_emoji else r.emoji}] // \n{', '.join(usr.name for usr in usrs)}")
    await pages.PageThis(ctx, lit, "MESSAGE INFO")

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(msg)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('msg')
    print('GOOD')

