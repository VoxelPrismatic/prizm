#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from util.embedify import embedify
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = ['invite'], 
                      help = 'inf',
                      brief = 'Invite for me and my support server',
                      usage = ';]inv',
                      description = '''    [NO ARGS FOR THIS COMMAND]
    ''')
@commands.check(enbl)
async def inv(ctx):
    perms = discord.Permissions()
    vals = {'create_instant_invite': False,
            'kick_members': True,
            'ban_members': True,
            'administrator': False,
            'manage_channels': True,
            'manage_guild': True,
            'add_reactions': True,
            'view_audit_log': True,
            'priority_speaker': False,
            'stream': True,
            'read_messages': True,
            'send_messages': True,
            'send_tts_messages': False,
            'manage_messages': True,
            'embed_links': True,
            'attach_files': True,
            'read_message_history': True,
            'mention_everyone': False,
            'external_emojis': True,
            'connect': True,
            'speak': True,
            'mute_members': True,
            'deafen_members': True,
            'use_voice_activation': True,
            'change_nickname': False,
            'manage_nicknames': True,
            'manage_roles': True,
            'manage_webhooks': False,
            'manage_emojis': True }
    perms.update(**vals)
    await ctx.send(embed=embedify(desc=f'''```md
#] INVITE ;]
> Thanks for letting me be a part of your server!```
[BOT ;]]({discord.utils.oauth_url(ctx.bot.user.id, perms)}) // [GUILD ;]](https://discord.gg/Z84Nm6n) // [SITE ;]](https://aka.re/Prizm)'''))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(inv)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('inv')
    print('GOOD')
