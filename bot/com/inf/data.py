#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [], 
                  help = 'inf',
                  brief = 'Shows the data usage',
                  usage = ';]data',
                  description = '''\
[NO INPUT FOR THIS COMMAND]
''')
@commands.check(enbl)
async def data(ctx): 
    await ctx.send(
        embed = embedify.embedify(
            desc = '''```md
#] HOW YOUR DATA IS USED
-
When you talk to the AI, your message is stored permanentally
on the computer. Only the message content is stored, no other
identifiable information.
-
Data is also stored when you request/set up server specific
info like tags, logging options, etc. This of course lets the
bot remember your settings when it restarts.
-
Lastly, any logging info, converted files, or mixed images
can be stored either temporarily in ram or permanentally
until the next time that file is changed.
-
#] TL;DR
>  Your messages are only used for AI, server specific
>  data, or when a file is directly uploaded/downloaded.
```''',
            title = "DATA ;]",
            foot = "PRIZM ;] // Your data is safe"
        )
    )

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(data)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('data')
    print('GOOD')

