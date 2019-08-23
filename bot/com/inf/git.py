#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'inf',
                  brief = 'Shows the git repo',
                  usage = ';]git',
                  description = '[NO ARGS FOR THIS COMMAND]')
@commands.check(enbl)
async def git(ctx):
    await ctx.send('`]GITHUB PAGE` https://github.com/VoxelPrismatic/prizai/')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(git)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('git')
    print('GOOD')
