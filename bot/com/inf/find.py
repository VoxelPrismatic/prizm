#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from discord.utils import find

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = [], 
    help = 'inf',
    brief = 'Finds a meta object given an ID or name',
    usage = ';]find {name/id}',
    description = '''\
name/id [TEXT] - The name or ID of the thing to find
'''
)
@commands.check(enbl)
async def find(ctx, *, name_id):
    send = ''
    stuff = [
        [ctx.guild.channels, "#", ""],
        [ctx.guild.members, "@", ""],
        [ctx.guild.emojis, ":", ":"],
        [ctx.guild.rules, "&", ""]
    ]
    for ls, prefix, suffix in stuff:
        for thing in ctx.guild.channels:
            if name_id in [str(thing.id), thing.name]:
                send += f'> {prefix}{str(thing)}{suffix}\n'
    if fID == ctx.guild.name: 
        send += f'> GLD ] {ctx.guild.name}'
    await ctx.send('```md\n' + (send if send else '[NONE FOUND]') + '```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(find)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('find')
    print('GOOD')
