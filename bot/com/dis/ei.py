#!/emj/bin/env python3
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

@commands.command(aliases = ["emojiinfo", "infoemoji", "iemoji", "emojii", "iemj"],
                  help = 'dis',
                  brief = 'Sends info about a given {emoji}',
                  usage = ';]ei {emoji}',
                  description = '''\
EMOJI [EMOJI] - The CUSTOM emoji in question
''')
@commands.check(enbl)
async def emj(ctx, emoji:discord.Emoji):
    await ctx.send(embed=embedify.embedify(desc=f'''```
#] INFO FOR :{emoji.name}
     ID ] {_emj.id}
  ROLES ] {_emj.roles}
CREATED ] {_emj.created_at}
MANAGED ] {_emj.managed}```''',
        thumb=str(_emj.url).replace('webp','png')))


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(emj)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('emj')
    print('GOOD')
