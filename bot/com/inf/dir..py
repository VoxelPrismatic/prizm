#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import os
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def dir(ctx, loc:str=""):
    if ".." in loc: return await ctx.send('```diff\n-]INVALID PATH```')
    try: dr = os.listdir(path=f"/home/priz/Desktop/PrizAI/{loc}")
    except: return await ctx.send('```diff\n-]THAT ISN\'T A DIRECTORY UwU```')
    dr.sort(key=len)
    di = ""
    for do in dr:
        if '.' in do: 
            de = do.split('.')[0]; dp = do.split('.')[1].upper()
            if do == ".directory": de = "."
            if do == "..directory": de = ".."
            if len(de) > 7: de = de[0:7]+f" ~{len(de)-7}"
            if len(dp) > 3: dp = dp[0:3]
            di = di+"> {:>10}".format(de)+f" // TYPE: {dp}\n"
        else:
            da = do; tru = f"{loc}/{do}"
            if len(do) > 7: da = do[0:7]+f" ~{len(do)-7}"
            if loc == "": tru = do
            try: 
                os.listdir(path=f"/home/priz/Desktop/PrizAI/{tru}")
                di = di+"> {:>10} // TYPE: DIR\n".format(da)
            except NotADirectoryError: di = di+"> {:>10} // TYPE: TXT\n".format(da)
    await ctx.send(embed=embedify.embedify(desc=f'''```md
#] !] PRIZ AI ;] [! DIR
{di}```'''))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(dir)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command(dir)
    print('GOOD')