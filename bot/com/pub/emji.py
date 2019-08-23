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

@commands.command(help = 'fun',
                  brief = 'Steals an emoji for you',
                  usage = ';]emji {emj1} {emj2} {...}',
                  description = 'EMJx [EMOJI] - The emoji you want to steal')
@commands.check(enbl)
async def emji(ctx, *emot:discord.Emoji):
    for icon in emot:
        try:
            await ctx.author.send(icon.url)
        except discord.NotFound:
            await ctx.send(f'```diff\n-] I couldn\'t find that emoji >~< [{str(icon)}]\n=] Make sure it is a custom emoji and I am in it\'s respective server```')
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

