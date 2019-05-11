#!/emj/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text, thumb): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d).set_thumbnail(url=thumb)
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def emj(ctx, _emj:discord.Emoji):
    try:
        await ctx.send(embed=embedify(f'''```
     ID // {_emj.id}
   NAME // {_emj.name}
  ROLES // {_emj.roles}
 COLONS // {_emj.require_colons}
CREATED // {_emj.created_at}
MANAGED // {_emj.managed}```''', _emj.url))
    except discord.HTTPException: await exc(ctx, 1)
    except discord.Forbidden: await exc(ctx, 2)
    except discord.NotFound: await exc(ctx, 3)


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

