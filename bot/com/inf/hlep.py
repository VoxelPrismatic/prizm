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

@commands.command(aliases=["help"])
async def hlep(ctx):
    result = 0
    def check(reaction, user): return user == ctx.author
    lit = ["""#] INFO
] ";]hlep"
> Brings up this message :)
] ";]ping"
> Shows the ping time :L
] ";]git"
> Shows the github/gitlab repo ;]
] ";]info"
> Shows additional info 9.6
] ";]os"
> Shows you what im running on >.>
] ";]hlepmini"
> A mini menu with no descriptions UwU
""",
            """#] FUN [1/3]
] ";]coin {x}" [Option: {x}]
> Flips a virtual coin {x} times 0.0
] ";]rng {x} {y} {z}" [Option: {z}]
> Prints an RNG from {x} to {y}, {z} times :P
] ";]dnd"
> Roles all dice from Dragons and Dungeons owo
] ";]cool {uID}"
> Gives someone [{userID}] a sneaky surpise ;D
] ";]rick"
> Rick Roll! °ω°
""",
            """#] FUN [2/3]
] ";]blkjck"
> BLACKJACK! 0o0
] ";]spam {x}"
> Spams {x} amount of chars >.<
] ";]react {mID} {reactions}" [{reaction}.split " "]
> Adds {reactions} to a given {mID} .-.
] ";]binary {text}"
> Converts {text} into binary, or in reverse! 9.6
] ";]echo {text}"
> ^self explanitory tbh :D
""",
            """#] FUN [3/3]
] ";]optn {options}"
> I choose for you >:D
] ";]rev {text}"
> 0.0 esreveR
] ";]emji {emoji}"
> Emoji stealin' time ;]
] ";]asci"
> Just prints one of these cool ASCIImoji! >.>
] ";]slots"
> Slot machine :D
] ";]snd {cID} {txt}"
> I send {text} into a {channelID} UwU
""",
            """ #] MATHS
] ";]graph {eq} {xmin} {xmax}"
> Graphs {eq} from {xmin} to {xmax} 9.6
] ";]rto {x} {y}"
> Reduces the ratio of {x} and {y} ;-;
] ";]rad {x}"
> Reduces a radical, {x}! >:D
] ";]stats {data}"
> Gives stats given {data} ._.
] ";]quad {a} {b} {c}"
> Uses {a}, {b}, and {c} to solve the Quad Formula 0o0
] ";]fct {int}"
> Factors {int} into factors and prime factors ;-;
""",
            """#] DISCORD CLASSES
] ";]chnl {cID}"
> Outputs channel info given a {channelID} -.-
] ";]mbr {mID}"
> Outputs member info given a {memberID} 0o0
] ";]usr {uID}"
> Outputs user info given a {userID} >.<
] ";]emj {emoji}"
> Outputs emoji info given {emoji} '.'
] ";]rol {rID}"
> Outputs role info given a {roleID} >:D
"""]
    msghlep = await ctx.send(content=f"[{result}//{len(lit)}]",embed=embedify(f'''```md
#] !] PRIZ AI ;] [! COMMANDS LIST``````md
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
            await msghlep.edit(content=f"[{result}//{len(lit)}]",embed=embedify(f'''```md
#] !] PRIZ AI ;] [! COMMANDS LIST``````md
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
    bot.add_command(hlep)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hlep')
    print('GOOD')

