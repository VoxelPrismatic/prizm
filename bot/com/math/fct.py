#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import typing
import math
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=['fct'],
                  help = 'math',
                  brief = 'Finds the factors and prime factors of {num}',
                  usage = ';]factor {num}',
                  description = '''\
NUM [NUMBER] - The number to find the factors of
''')
@commands.check(enbl)
async def factor(ctx, num:int):
    fctr = []; prm = []
    async with ctx.channel.typing():
        for lel in range(1,int(num**.5)+1):
            if not math.remainder(num,lel): 
                fctr.extend([str(lel),str(int(num/lel))])
    async with ctx.channel.typing():
        ognum=num
        while num !=1:
            x = 1
            for y in prm: x*=int(y)
            if x>=ognum:break
            for lel in range(2,num+1):
                if not math.remainder(num,lel):
                    prm.append(str(lel)); num = int(num/lel); break

    await ctx.send(f'```md\n#] PRIME FACTORS\n> {",".join(prm)}\n#] FACTORS\n> {",".join(fctr)}```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(factor)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('factor')
    print('GOOD')
