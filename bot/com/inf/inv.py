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

@commands.command(aliases=['invite'])
async def inv(ctx): await ctx.send(embed=embedify(desc='```md\n#] INVITE ;]\n> Thanks for letting me be a part of your server!```[BOT ;]](https://discordapp.com/oauth2/authorize?client_id=555862187403378699&scope=bot&permissions=67497152) // [GUILD ;]](https://discord.gg/Z84Nm6n)'))

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
