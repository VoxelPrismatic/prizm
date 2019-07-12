#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio, json
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["helpmini","minihlep","minihelp","mini"])
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
> ping
> bug {report}
> inv""",
            """#] DISCORD CLASS
> chnl {cID}
> emj {eID}
> gld
> mbr {uID}
> rol {rID}
> usr {uID}
> msg {mID}""",
            """#] MATHS
> fact {n}
> fct {n}
> graph {xmin} {xmax} {eq1} {eq2} {eq3} {...}
> quad {a} {b} {c}
> rad {n}
> rto {x} {y}
> stats {a} {b} {c} {...}
> rpn {eq}""",
            """#] PUBLIC
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
> slap {member} {?reason}
> hug {member} {?reason}
> mock {?mID}
"""]
    await pages.PageThis(ctx, lit, "MINI COMMANDS LIST", f"""```md
#] {'{?stuff}'} - Optional argument
#] To see mod commands, use "{json.load(open('prefixes.json'))[str(ctx.guild.id)] if isinstance(ctx.channel, discord.TextChannel) else ';]'}hlepmod"
#] To have a conversation, use "]<txt>" or "{'}<txt>'}"
#] Some of your data is stored, use "{json.load(open('prefixes.json'))[str(ctx.guild.id)] if isinstance(ctx.channel, discord.TextChannel) else ';]'}data" to see more```""")

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