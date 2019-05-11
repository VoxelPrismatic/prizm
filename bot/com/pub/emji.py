#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def emji(ctx, *emot:discord.Emoji):
    for icon in emot:
        try:
            await ctx.author.send(icon.url)
        except discord.NotFound:
            await ctx.send('```I couldn\'t find that emoji >~<```')
        except:
            await ctx.send('```Something wrong happened... Make sure your DMs are open 0.0```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(emji)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('emji')
    print('GOOD')

