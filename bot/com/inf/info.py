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

@commands.command(help = 'inf',
                  brief = 'Shows aditional bot info',
                  usage = ';]info',
                  description = '[NO ARGS FOR THIS COMMAND]')
@commands.check(enbl)
async def info(ctx):
    await ctx.send('''```md
#] PRIZM
=] THE CODE
>  Prizm is 100% open source and available for anybody to use
>  This bot is just a project I started in my spare time, and
>  now it has grown to something I would've never thought
>  would happen. Due to bad habits and things, this bot has
>  been rewritten twice already, and oh boy is it [not] fun!
-
=] THE AI
>  Version 1 of the AI just compared strings and actually
>  originated from a side project on the TI-84+CSE, which btw
>  is where I got all the bad habits
-
>  Version 2 of the AI uses custom Markov chains to generate
>  text, and it isn't very good
-
>  Version 3 of the AI will be using TensorFlow, which means
>  that it's an actual AI. I am not done with it but I assure
>  you that it will come... eventually
-
=] THE PC
>  This bot is being run on a laptop with only 8GB of ram
>  and it's using more than 100 files for commands and more
>  This is not meant to be a high demanding bot, but I'm
>  already sure that it's more than just a side project
-
=] OTHER STUFF
>  If you would like to invite me to your server, use ';]inv'
>  If you would like to join my support server, use ';]inv'
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

