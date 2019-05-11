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

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["helpmini"])
async def hlepmini(ctx):
    result = 0
    def check(reaction, user): return user == ctx.author
    lit = ["""#] INFO
> data
> git
> hlep
> hlepmini
> hlepmod
> info
> os
> ping""",
            """#] DISCORD CLASS
> chnl {cID}
> emj {eID}
> gld
> mbr {uID}
> rol {rID}
> usr {uID}""",
            """#] MATHS
> fact {n}
> fct {n}
> graph {eq} {xmin} {xmax}
> quad {a} {b} {c}
> rad {n}
> rto {x} {y}
> stats {a} {b} {c} {...}""",
            """#] MOD
> ban {uID} {del} {reason}
> clr {n}
> clrin {mID} {mID}
> kick {uID}
> pin {mID}
> unpin {mID}""",
            """#] PUBLIC
> asci
> binary
> blkjck
> coin {[n]}
> cool {uID}
> dnd
> echo {txt}
> emji {eID}
> optn {a} {b} {c} {...}
> react {mID} {a} {b} {c} {...}
> rev {txt}
> rick
> rng {min} {max} {count}
> slots
> snd {cID} {text}
> spam {count}
"""]
    msghlep = await ctx.send(embed=embedify(f'''```md
#] !] PRIZ AI ;] [! MINI COMMANDS LIST``````md
{lit[result]}``````md
#] To see mod commands, use ";]hlepmod"
#] To have a conversation, use "]<your text here>""
#] Some of your data is stored, use ";]data" to see more
```'''))
    await msghlep.add_reaction('⏪')
    await msghlep.add_reaction('◀')
    await msghlep.add_reaction('⏹')
    await msghlep.add_reaction('▶')
    await msghlep.add_reaction('⏩')
    while True:
        try: reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError: return await msghlep.clear_reactions()
        else:
            if str(reaction.emoji) == '⏪':
                result = 0
                await msghlep.remove_reaction('⏪', ctx.author)
            elif str(reaction.emoji) == '◀':
                await msghlep.remove_reaction('◀', ctx.author)
                result = result - 1
                if result < 0: result = len(lit) - 1
            elif str(reaction.emoji) == '⏹':
                return await msghlep.clear_reactions()
            elif str(reaction.emoji) == '▶':
                await msghlep.remove_reaction('▶', ctx.author)
                result = result+1
                if result > (len(lit) - 1): result = 0
            elif str(reaction.emoji) == '⏩':
                result = len(lit) - 1
                await msghlep.remove_reaction('⏩', ctx.author)
            await msghlep.edit(embed=embedify(f'''```md
#] !] PRIZ AI ;] [! MINI COMMANDS LIST``````md
{lit[result]}``````md
#] To see mod commands, use ";]hlepmod"
#] To have a conversation, use "]<your text here>"
#] Some of your data is stored, use ";]data" to see more
```'''))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hlepmini)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hlepmini')
    print('GOOD')

