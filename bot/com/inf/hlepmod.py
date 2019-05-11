#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
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

@commands.command(aliases=["helpmod"])
async def hlepmod(ctx):
    result = 0
    def check(reaction, user): return user == ctx.author
    lit = ["""
] ";]hlepmod"
> Brings up this message :)
] ";]ban {user} {delete days} {reason}"
> Bans a {user} and removes messages from {delete days} ago for a {reason}
] ";]kick {user}"
> Kicks a {user} from the server
] ";]clr {int}"
> Deletes a {int} amount of messages
] ";]clrin {messageID1} {messageID2}"
> Deletes messages between {messageID1} and {messageID2}""",
            """] ";]pin {mID}"
> Pins {mID}
] ";]unpin {mID}"
> Unpins {mID}"""]
    msghlepmod = await ctx.send(embed=embedify(f'''```diff
-] !] PRIZ AI ;] [! MOD STUFF``````md
{lit[result]}``````diff
-] To see mod commands, use ";]hlepmod"
-] To have a conversation, use "]<your text here>""
-] Some of your data is stored, use ";]data" to see more
```'''))
    await msghlepmod.add_reaction('⏪')
    await msghlepmod.add_reaction('◀')
    await msghlepmod.add_reaction('⏹')
    await msghlepmod.add_reaction('▶')
    await msghlepmod.add_reaction('⏩')
    while True:
        reactions = ['⏪','◀','⏹','▶','⏩']
        for rct in reactions: await msghlepmod.add_reaction(rct)
        while True:
            try: reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError: return await msghlepmod.clear_reactions()
            else:
                if str(reaction.emoji) == '⏪': result = 0
                elif str(reaction.emoji) == '◀': result = result - 1
                elif str(reaction.emoji) == '⏹': return await msghlepmod.clear_reactions()
                elif str(reaction.emoji) == '▶': result = result+1
                elif str(reaction.emoji) == '⏩': result = len(lit) - 1
                await msghlepmod.remove_reaction(reaction, ctx.author)
                if result < 0: result = 0
                elif result > (len(lit) - 1): result = len(lit) - 1
                await msghlepmod.edit(embed=embedify(f'''```diff
-] !] PRIZ AI ;] [! MOD STUFF``````md
{lit[result]}``````diff
-] To see mod commands, use ";]hlepmod"
-] To have a conversation, use "]<your text here>""
-] Some of your data is stored, use ";]data" to see more
```'''))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hlepmod)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hlepmod')
    print('GOOD')

