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

@commands.command(aliases = ["steal"],
                  help = 'fun',
                  brief = 'Steals an emoji for you',
                  usage = ';]emji {emoji1} {emoji2} {...}',
                  description = '''\
EMOJIx [EMOJI] - The emoji you want to steal, must be custom
''')
@commands.check(enbl)
async def emji(ctx, *emot:discord.Emoji):
    for icon in emot:
        try:
            await ctx.author.send('https://cdn.discordapp.com/emojis/'+icon.split(':')[1]+('.gif' if '<a:' in icon else '.png'))
        except:
            await ctx.send('```diff\n-] MAKE SURE YOUR DMS ARE OPEN```')

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
