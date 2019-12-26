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

@commands.command(aliases = [], 
                  help = 'inf',
                  brief = 'Shows aditional bot info',
                  usage = ';]info',
                  description = '''\
[NO INPUT FOR THIS COMMAND]
''')
@commands.check(enbl)
async def info(ctx):
    await ctx.send('''```md
#] PRIZM INFO ;]
=] Thanks for wanting to learn how I work!
``````md
#] THE CODE
>  PRIZM is 100% open source and is hosted on GitHub.
>  There are over 100 commands as of writing this.
>  PRIZM is using a library called discord.py to interact
>  - with Discord, and this library sucks. So, I'm making
>  - my own. Therefore PRIZM is under a complete rewrite
>  - and not all of the commands will be formatted the
>  - same way.
``````md
=] THE AI
>  The AI uses NLTK and your responses to learn. If you
>  - want the bot to learn faster, you can use the ;]learn
>  - command and send a full 2 person conversation
`````md
#] THE PC
>  This bot is being run on a laptop with only 8GB of ram
>  and it's using more than 100 files for commands and more
>  This is not meant to be a high demanding bot, but I'm
>  already sure that it's more than just a side project
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

