#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)
def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)
async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
    return msgs

async def com(bot, command):
    msgs = await log(bot, "COMMAND USED", f'COMMAND // {command}')
    print(f']{command}')
    return msgs
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["helpown"])
@commands.is_owner()
async def hlepown(ctx):
    result = 0
    def check(reaction, user): return user == ctx.author
    lit = ["""
] ";]hlepown"
> Brings up this message :)
] ";]clrin0"
> An override for ";]clrin"
] ";]clr0"
> An override for ";]clr"
] ";]calc"
> A calculator
] ";]exe"
> Executables""",
            """] ";]pwr"
> Shuts down
] ";]rld"
> Reloads extensions
] ";]ld"
> Loads extensions
] ";]uld"
> Unloads extensions""",
            """] ";]pin0"
> An override for ";]pin"
] ";]unpin0"
> An override for ";]unpin" """]
    msg = await ctx.send(embed=embedify(f'''```diff
+] !] PRIZ AI ;] [! OWNER STUFF``````md
{lit[result]}``````diff
+] To see commands, use ";]hlep"
+] To have a conversation, use "]<your text here>""
+] Some of your data is stored, use ";]data" to see more
```'''))
    await msg.add_reaction('⏪')
    await msg.add_reaction('◀')
    await msg.add_reaction('⏹')
    await msg.add_reaction('▶')
    await msg.add_reaction('⏩')
    while True:
        try: reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError: return await msg.clear_reactions()
        else:
            if str(reaction.emoji) == '⏪':
                result = 0
                await msg.remove_reaction('⏪', ctx.author)
            elif str(reaction.emoji) == '◀':
                await msg.remove_reaction('◀', ctx.author)
                result = result - 1
                if result < 0: result = len(lit) - 1
            elif str(reaction.emoji) == '⏹':
                return await msg.clear_reactions()
            elif str(reaction.emoji) == '▶':
                await msg.remove_reaction('▶', ctx.author)
                result = result+1
                if result > (len(lit) - 1): result = 0
            elif str(reaction.emoji) == '⏩':
                result = len(lit) - 1
                await msg.remove_reaction('⏩', ctx.author)
            await msg.edit(embed=embedify(f'''```diff
+] !] PRIZ AI ;] [! OWNER STUFF``````md
{lit[result]}``````diff
+] To see commands, use ";]hlep"
+] To have a conversation, use "]<your text here>""
+] Some of your data is stored, use ";]data" to see more
```'''))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hlepown)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hlepown')
    print('GOOD')
