#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import math, cmath
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
import json
import io
import re

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    help = 'own',
    brief = 'Backs up commands to a JSON file',
    usage = ';]dumpcoms',
    description = '''
[NO INPUT FOR THIS COMMAND]
'''
)
@commands.is_owner()
async def dumpcoms(ctx):
    msg = await ctx.send("```md\n#] SAVING COMMAND INDEX```")
    dic = {}
    for com in ctx.bot.commands:
        if com.help and com.help != "own":
            dic[com.name] = {
                "alias": com.aliases,
                "inp": com.description,
                "cat": com.help,
                "desc": com.brief,
                "use": com.usage,
            }
    st = json.dumps(dic, indent = 4).replace("\\n", "\\\n")
    st = re.sub(r"\\n +", r" ", st)
    await ctx.send(
        "```md\n#] COMMAND INDEX```",
        file = discord.File(
            io.BytesIO(st.encode()),
            "commands.json"
        )
    )
    await msg.delete()

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(dumpcoms)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('dumpcoms')
    print('GOOD')
