#!/rol/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["roleinfo", "irole", "rolei", "irol", "roli"],
                  help = 'dis',
                  brief = 'Displays info about a given {role}',
                  usage = ';]rol {role}',
                  description = 'ROLE [ROLE] - The target role, ping or name or ID')
@commands.check(enbl)
async def ri(ctx, *, _rol:discord.Role):
    yeperms = [perm for perm, val in list(_rol.permissions) if val == True]
    noperms = [perm for perm, val in list(_rol.permissions) if val == False]
    okperms = [perm for perm, val in list(_rol.permissions) if val == None]
    await ctx.send(embed=embedify.embedify(title='ROLE INFO ;]', desc=f'''```md
#] INFO FOR &{_rol.name}
      ID ] {_rol.id}
     POS ] {_rol.position}
   COLOR ] {_rol.color}
   HOIST ] {_rol.hoist}
 CREATED ] {_rol.created_at}
 MANAGED ] {_rol.managed}
 MENTION ] {_rol.mentionable}
PERM VAL ] {_rol.permissions.value}
``````diff
+] {', '.join(perms)}
-] {', '.join(noperms)}
=] {', '.join(okperms)}
```''', thumb=ctx.guild.icon))


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(ri)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('ri')
    print('GOOD')