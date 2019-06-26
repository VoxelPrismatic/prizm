#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["helpmini"])
@commands.check(enbl)
async def hlepmini(ctx):
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
> graph {xmin} {xmax} {eq1} {eq2} {eq3} {...}
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
> unpin {mID}
> enable {command}  // SERVER OWNER ONLY
> disable {command} // SERVER OWNER ONLY
> prefix {prefix}   // SERVER OWNER ONLY""",
            """#] PUBLIC [1/2]
> md {mID}
> dnd
> snd {cID} {txt}
> djq
> rng {min} {max} {?count}
> rev {txt}
> poll {txt}
> rick
> coin {?count}
> asci
> optn {a} {b} {c} {...}
> echo {txt}
> spam {amount}
> cool {uID}
> emj {emoji} // LIMITED
> react {mID} {a} {b} {c} {...}
> slots
> blkjck
> binary {txt}
> char {txt}
> vox {text}
> mines {?size} {?num}
> tag
> tag + {name} {stuff}
> tag - {name}         // TAG CREATOR ONLY
> tag / {name} {stuff} // TAG CREATOR ONLY
"""]
    await pages.PageThis(ctx, lit, "MINI COMMANDS LIST", '''```md
#] To see mod commands, use ";]hlepmod"
#] To have a conversation, use "]<your text here>""
#] Some of your data is stored, use ";]data" to see more
```''')

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