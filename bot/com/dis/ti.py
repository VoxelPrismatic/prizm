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

@commands.command(aliases = ["textinfo", "infotext", "texti", "itext",
                             "txti", "itxt"],
                  help = 'dis',
                  brief = 'Displays info on a given {message}',
                  usage = ';]ti {message}',
                  description = '''\
MSG [MESSAGE] - The target message, ID or URL
''')
@commands.check(enbl)
async def ti(ctx, message:discord.Message):
    lit = [f"""
#] MESSAGE BY @{str(message.author)} IN #{str(message.channel)}
     ID ] {message.id}
    TTS ] {message.tts}
    URL ] {message.jump_url}
   SENT ] {message.created_at}
 PINNED ] {message.pinned}
 EDITED ] {message.edited_at}
"""]
    if len(_msg.reactions) > 0:
        for r in _msg.reactions:
            usrs = await r.users().flatten()
            lit.append(f"REACTIONS [{r.emoji.name if r.custom_emoji else r.emoji}] ] \n{', '.join(usr.name for usr in usrs)}")
    await pages.PageThis(ctx, lit, "MESSAGE INFO")

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(ti)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('ti')
    print('GOOD')

