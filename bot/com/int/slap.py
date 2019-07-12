#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging, random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.embedify import embedify

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
async def slap(ctx, mbr:discord.Member, *, txt=' '):
    gifs = ["https://media.giphy.com/media/gSIz6gGLhguOY/giphy.gif",
            "https://media.giphy.com/media/rCftUAVPLExZC/giphy.gif",
            "https://media.giphy.com/media/vxvNnIYFcYqEE/giphy.gif",
            "https://media.giphy.com/media/s5zXKfeXaa6ZO/giphy.gif",
            "https://media.giphy.com/media/mEtSQlxqBtWWA/giphy.gif",
            "https://media.giphy.com/media/3wtc9qlgBxaq4/giphy.gif",
            "https://media.giphy.com/media/IAAXyr5GU73xK/giphy.gif",
            "https://media.giphy.com/media/Y6c59hTH3TJoA/giphy.gif",
            "https://media.giphy.com/media/KyIfvvHvEefAxjW26o/giphy.gif",
            "https://media.giphy.com/media/Ji03RBamoDhtK/giphy.gif",
            "https://media.giphy.com/media/UCyuDunJK0l6U/giphy.gif",
            "https://media.giphy.com/media/6Fad0loHc6Cbe/giphy.gif",
            "https://media.giphy.com/media/WLXO8OZmq0JK8/giphy.gif",
            "https://media.giphy.com/media/vlH0dqH8DiZa0/giphy.gif",
            "https://media.giphy.com/media/RY4tWACV5NjiM/giphy.gif",
            "https://media.giphy.com/media/TyedlhnUI6aNG/giphy.gif",
            "https://media.giphy.com/media/IoNEzxDswko6c/giphy.gif",
            "https://media.giphy.com/media/PgqHnJPeZHxv2/giphy.gif",
            "https://media.giphy.com/media/t1CsJ1o1sdOHm/giphy.gif",
            "https://media.giphy.com/media/8BJtJUceqxaoM/giphy.gif",
            "https://media.giphy.com/media/3XlEk2RxPS1m8/giphy.gif",
            "https://media.giphy.com/media/AkKEOnHxc4IU0/giphy.gif",
            "https://media.giphy.com/media/vA7QzAS5bjfwc/giphy.gif",
            "https://media.giphy.com/media/q87sL36RwERJC/giphy.gif",
            "https://media.giphy.com/media/a1TLhXDBTB0xq/giphy.gif",
            "https://media.giphy.com/media/iVKn5ZEhadTHy/giphy.gif",
            "https://media.giphy.com/media/RrLbvyvatbi36/giphy.gif",
            "https://media.giphy.com/media/tV0HkQju9zHR6/giphy.gif",
            "https://media.giphy.com/media/4nHsalgvIblUk/giphy.gif",
            "https://media.giphy.com/media/gSVp80uysLOb6/giphy.gif",
            "https://media.giphy.com/media/tV0HkQju9zHR6/giphy.gif",
            "https://media.giphy.com/media/3vDS40HZxJwFGTbXoI/giphy.gif",
            "https://media.giphy.com/media/10jmkQ3gZXBUbe/giphy.gif",
            "https://media.giphy.com/media/dICjAqixKQFnG/giphy.gif",
]
    await ctx.send(embed=embedify(desc=f'```md\n#] {ctx.author.name} SLAPPED {mbr.name}'+(f'\n> FOR {txt.upper()}```' if txt != ' ' else '```'),
                                  img=random.choice(gifs)))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(slap)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('slap')
    print('GOOD')

