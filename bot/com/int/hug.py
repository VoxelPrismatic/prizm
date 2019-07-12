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
async def hug(ctx, mbr:discord.Member, *, txt=' '):
    gifs = ["https://media.giphy.com/media/ZBQhoZC0nqknSviPqT/giphy.gif",
            "https://media.giphy.com/media/EvYHHSntaIl5m/giphy.gif",
            "https://media.giphy.com/media/42YlR8u9gV5Cw/giphy.gif",
            "https://media.giphy.com/media/3M4NpbLCTxBqU/giphy.gif",
            "https://media.giphy.com/media/xT39CXg70nNS0MFNLy/giphy.gif",
            "https://media.giphy.com/media/143v0Z4767T15e/giphy.gif",
            "https://media.giphy.com/media/wnsgren9NtITS/giphy.gif",
            "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
            "https://media.giphy.com/media/yziFo5qYAOgY8/giphy.gif",
            "https://media.giphy.com/media/13YrHUvPzUUmkM/giphy.gif",
            "https://media.giphy.com/media/qscdhWs5o3yb6/giphy.gif",
            "https://media.giphy.com/media/VIPdgcooFJHtC/giphy.gif",
            "https://media.giphy.com/media/45Lg3ECIw25Fe/giphy.gif",
            "https://media.giphy.com/media/ZuOiqNL4k5UWY/giphy.gif",
            "https://media.giphy.com/media/LON1BhW6JdFrG/giphy.gif",
]
    await ctx.send(embed=embedify(desc=f'```md\n#] {ctx.author.name} HUGGED {mbr.name}'+(f'\n> BECAUSE {txt.upper()}```' if txt != ' ' else '```'),
                                  img=random.choice(gifs)))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hug)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hug')
    print('GOOD')

