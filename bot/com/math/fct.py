#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import typing
import math
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def fct(ctx, num:int):
    fctr = prm = ""
    async with ctx.channel.typing():
        for lel in range(1,int(num**.5)+1):
            if not math.remainder(num,lel): fctr = fctr + f"[{int(num/lel)},{lel}]"
    await ctx.send(f'```md\n#] FACTORS\n> {fctr}```')
    async with ctx.channel.typing():
        while num !=1:
            lol = 2
            for lel in range(2,num+1):
                print(num, lol, lel)
                if not math.remainder(num,lol):
                    prm = prm + f"{lol}, "; num = int(num/lol); lol = lol*num
                else:
                    lol +=1
                if lol > num: break

    await ctx.send(f'```md\n#] PRIME FACTORS\n> {prm}```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(fct)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('fct')
    print('GOOD')

