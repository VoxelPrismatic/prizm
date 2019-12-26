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
async def emji(ctx, *emojis:discord.Emoji):
    ls = [[]]
    for emoji in emojis:
        id = emoji.id
        typ = ".gif" if emoji.animated else ".png"
        ls[-1].append(f'https://cdn.discordapp.com/emojis/{id}{typ}')
        if len(ls[-1]) >= 5:
            ls.append([])
    for l in ls:
        await ctx.author.send("\n".join(l))
    await ctx.message.add_reaction("<:wrk:608810652756344851>")
    

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
