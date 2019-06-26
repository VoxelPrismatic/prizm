#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["help"])
async def hlep(ctx):
    lit = ["""#] INFO [1/2]
] ";]hlep"
> Brings up this message :)
] ";]ping"
> Shows the ping time :L
] ";]git"
> Shows the github/gitlab repo ;]
] ";]info"
> Shows additional info 9.6
""",
            """#] INFO [2/2]
] ";]os"
> Shows you what im running on >.>
] ";]hlepmini"
> A mini menu with no descriptions UwU
] ";]dir {path}" [Option: {path}]
> C:\>dir 0.0
""",
            """#] FUN [1/4]
] ";]md {mID}"
> Sends the escaped contents of {messageID} :D
] ";]dnd"
> Roles all dice from Dragons and Dungeons 0w0
] ";]snd {cID} {txt}"
> I send {text} into a {channelID} UwU
] ";]djq"
> In rememberance of DJ Quzingler [BOT] 9.6
] ";]rng {x} {y} {z}" [Option: {z}]
> Prints an RNG from {x} to {y}, {z} times :P """,
            """#] FUN [2/4]
] ";]rev {text}"
> 0.0 esreveR
] ";]poll {text}"
> Creates a Poll ;]
] ";]rick"
> Rick Roll! 0w0
] ";]coin {x}" [Option: {x}]
> Flips a virtual coin {x} times 0.0
] ";]asci"
> Just prints one of these cool ASCIImoji! >.>""",
            """#] FUN [3/4]
] ";]optn {options}" [ex: ';]echo hi "good bye"'-> hi, good bye]
> I choose for you >:D
] ";]echo {text}"
> ^self explanitory tbh :D
] ";]spam {x}"
> Spams {x} amount of chars >.<
] ";]cool {uID}"
> Gives someone [{userID}] a sneaky surpise ;D
] ";]emji {emoji}"
> Emoji stealin' time ;] """,
            """#] FUN [4/4]
] ";]slots"
> Slot machine :D
] ";]react {mID} {reactions}" [{reaction}.split " "]
> Adds {reactions} to a given {mID} .-.
] ";]blkjck"
> BLACKJACK! 0o0
] ";]binary {text}"
> Converts {text} into binary, or in reverse! 9.6
""",
            """#] MATHS
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
] ";]msg {mID}"
> Outputs message info given a {messageID} UwU
""",
            """#] TAGS
] ";]tag"
> Shows all the tags on the server Usually
] ";]tag + {name} {content}"
> Creates a tag, {name}, with {content} 0.0
] ";]tag - {name}"
> Deletes the tag, {name} 9.6 // Tag creator only
] ";]tag / {name} {content}"
> Edits the tag, {name}, with {content} // Tag creator only
"""]
    await pages.PageThis(ctx, lit, "COMMANDS LIST", """```md
#] To see mod commands, use ";]hlepmod"
#] To have a conversation, use "]<your text here>"
#] Some of your data is stored, use ";]data" to see more```""")


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