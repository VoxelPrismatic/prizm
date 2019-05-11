
#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import subprocess
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def tempcog(ctx):
    await ctx.send('hi')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(tempcog)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('tempcog')
    print('GOOD')