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

@commands.command()
@commands.check(enbl)
async def info(ctx): await ctx.send('''```md
#] PRIZM
> An RNG based AI that compares strings... literally
> Originally written for the TI84+CSE and adapted into a way better Discord Bot!
> This is version [0]-RW, a rewritten version
> Yes, the above version number is a joke 0.0
>
> This bot is being run on a laptop with only 8GB of ram
> and its using more than 100 files for commands and more
> It has also been made from scratch and therefore is 100% OG
>
> I am currently in the testing phase, but my ai has gotten much better
> If you would like to invite me to your server, use ';]inv'
> If you would like to join my support server, use ';]inv'
```''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(info)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('info')
    print('GOOD')

