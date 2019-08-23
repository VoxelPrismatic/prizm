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

@commands.command(help = 'dis',
                  brief = 'Displays info about a given {role}',
                  usage = ';]rol {role}',
                  description = 'ROLE [ROLE] - The target role, ping or name or ID')
@commands.check(enbl)
async def rol(ctx, *, _rol:discord.Role):
    perms = [perm for perm, val in list(_rol.permissions) if val]
    await ctx.send(embed=embedify.embedify(desc=f'''```
      ID // {_rol.id}
     POS // {_rol.position}
    NAME // {_rol.name}
   COLOR // {_rol.color}
   HOIST // {_rol.hoist}
   PERMS // {', '.join(perms)}
 CREATED // {_rol.created_at}
 MANAGED // {_rol.managed}
 MENTION // {_rol.mentionable}
PERM VAL // {_rol.permissions.value}
```'''))


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rol)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rol')
    print('GOOD')