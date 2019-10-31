#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback, json
from util import pages, getPre, dbman
from util.embedify import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

bot = commands.Bot(command_prefix=getPre.getPre)

def rtn(gID, nam, mbr:discord.Member=None):
    itm = dbman.get('log','bot',id=int(gID), rtn = bool)
    if not mbr:
        bt = False
    else:
        bt = mbr.bot
    lBOT = True
    if not itm and bt:
        lBOT = False
    try:
        return dbman.get('log','bot',id=int(gID), rtn=bool) and dbman.get('oth','lCH',id=int(gID),rtn=int) \
               and lBOT, dbman.get('oth','lCH',id=int(gID),rtn=int)
    except Exception as ex:
        print(ex)
        return False, None

def lnk(msg):
    return f'https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}'

def clnk(chn):
    return f'https://discordapp.com/channels/{chn.guild.id}/{chn.id}'

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

#@bot.listen('on_guild_channel_create')
#@bot.listen('on_guild_channel_delete')
#@bot.listen('on_guild_channel_update')
#@bot.listen('on_guild_integrations_update')
#@bot.listen('on_member_ban')
#@bot.listen('on_member_unban')
#@bot.listen('on_member_update')
#@bot.listen('on_guild_update')
#@bot.listen('on_guild_role_create')
#@bot.listen('on_guild_role_delete')
#@bot.listen('on_guild_role_update')
#@bot.listen('on_webhooks_update')
async def audit_log(*args):
    print('something happened...')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+LIS [LOG]')
    for x in ['on_guild_channel_create', 'on_guild_channel_delete',
              'on_guild_channel_update', 'on_guild_integrations_update',
              'on_member_ban', 'on_member_unban', 'on_member_update',
              'on_guild_update', 'on_guild_role_create',
              'on_guild_role_update', 'on_guild_role_delete',
              'on_webhooks_update']:
        bot.add_listener(audit_log, x)
    print('GOOD')

def teardown(bot):
    print('-LIS [LOG]')
    for x in ['on_guild_channel_create', 'on_guild_channel_delete',
              'on_guild_channel_update', 'on_guild_integrations_update',
              'on_member_ban', 'on_member_unban', 'on_member_update',
              'on_guild_update', 'on_guild_role_create',
              'on_guild_role_update', 'on_guild_role_delete',
              'on_webhooks_update']:
        bot.remove_listener(audit_log, x)
    print('GOOD')
