#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing, praw
import discord                    #python3.7 -m pip install -U discord.py
import logging, random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.embedify import embedify
from util.prawUser import usr as pruw

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'int',
                  brief = 'Cuddle with a {member} for a {reason}!',
                  usage = ';]cuddle {mbr} {?reason}',
                  description = 'MBR    [INT or PING] - The member you want to slap\nREASON [STR        ] - The reason for the slap')
@commands.check(enbl)
async def cuddle(ctx, mbr:discord.Member, *, txt=' '):
    red = pruw()
    async with ctx.channel.typing():
        sub = list(red.subreddit('gifs').search('cuddle',sort=random.choice(['hot','top','new','relevance']),limit=100))
        sbn = random.choice(sub)
        while sbn.over_18 or sbn.is_self or 'https://gfycat' in sbn.url or 'v.redd' in sbn.url:
            sbn = random.choice(sub)

    await ctx.send(embed=embedify(desc=f'```md\n#] {ctx.author.name} THREW {mbr.name}'+(f'\n> FOR {txt.upper()}```' if txt != ' ' else '```'),
                                  img=sbn.url.replace('.gifv','.gif')))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(cuddle)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('cuddle')
    print('GOOD')

