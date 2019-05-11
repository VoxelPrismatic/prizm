#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import math
import typing
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x00ffff)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["factorial"])
async def fact(ctx, num: int):
    if num > 100000: return await ctx.send('```Do you really need that big of a number?```')
    async with ctx.channel.typing(): string = str(math.factorial(num))
    lit = []
    def check(reaction, user): return user == ctx.author
    for strt in range(0, len(string), 2000): lit.append(string[strt:strt+2000])
    result = 0
    msgfact = await ctx.send(embed=embedify(f'''```md
#] FACTORIAL``````
{lit[result]}
```'''))
    if not not len(lit)-1:
        reactions = ['⏪','◀','⏹','▶','⏩']
        for rct in reactions: await msgfact.add_reaction(rct)
        while True:
            try: reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError: return await msgfact.clear_reactions()
            else:
                if str(reaction.emoji) == '⏪': result = 0
                elif str(reaction.emoji) == '◀': result = result - 1
                elif str(reaction.emoji) == '⏹': return await msgfact.clear_reactions()
                elif str(reaction.emoji) == '▶': result = result+1
                elif str(reaction.emoji) == '⏩': result = len(lit) - 1
                await msgfact.remove_reaction(reaction, ctx.author)
                if result < 0: result = 0
                elif result > (len(lit) - 1): result = len(lit) - 1
                await msgfact.edit(embed=embedify(f'''```md
#] FACTORIAL``````
{lit[result]}
```'''))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(fact)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('fact')
    print('GOOD')
