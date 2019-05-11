#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def blkjck(ctx):
    try:
        heart = ['🂱','🂲','🂳','🂴','🂵','🂶','🂷','🂸','🂹','🂺','🂻','🂽','🂾']
        spade = ['🂡','🂢','🂣','🂤','🂥','🂦','🂧','🂨','🂩','🂪','🂫','🂭','🂮']
        diam = ['🃁','🃂','🃃','🃄','🃅','🃆','🃇','🃈','🃉','🃊','🃋','🃍','🃎']
        club = ['🃑','🃒','🃓','🃔','🃕','🃖','🃗','🃘','🃙','🃚','🃛','🃝','🃞']
        ttl1 = ttl2 = temp = stu = 0
        usr = cpu = cputxt = usrtxt = ""
        while ttl1 <= 18:
            temp = rand(0,12)
            if temp + ttl1 + 1 != 21:
                stu = rand(0,3)
                if stu == 1: usr = usr+heart.pop[temp]+' '
                elif stu == 2: usr = usr+spade.pop[temp]+' '
                elif stu == 3: usr = usr+diam.pop[temp]+' '
                elif stu == 3: usr = usr+club.pop[temp]+' '
                temp += 1
                if temp > 10: temp = 10
                ttl1 += temp
        while ttl2 <= 18:
            temp = rand(0,12)
            if temp + ttl2 + 1 != 21:
                if stu == 1: cpu = cpu+heart.pop[temp]+' '
                elif stu == 2: cpu = cpu+spade.pop[temp]+' '
                elif stu == 3: cpu = cpu+diam.pop[temp]+' '
                elif stu == 3: cpu = cpu+club.pop[temp]+' '
                temp += 1
                if temp > 10: temp = 10
                ttl2 += temp
        if ttl1 > 21: usrtxt = f'USER // {usr} [{ttl1}] [BUST]'
        elif ttl1 > ttl2: usrtxt = f'USER // {usr} [{ttl1}] [WIN]'
        elif ttl1 < ttl2: usrtxt = f'USER // {usr} [{ttl1}] [LOSS]'
        if ttl2 > 21: cputxt = f'COMP // {cpu} [{ttl2}] [BUST]'
        elif ttl2 > ttl1: cputxt = f'COMP // {cpu} [{ttl2}] [WIN]'
        elif ttl2 < ttl1: cputxt = f'COMP // {cpu} [{ttl2}] [LOSS]'
        if ttl1 == ttl2:
            usrtxt = f'USER // {usr} [{ttl1}] [TIE]'
            cputxt = f'COMP // {cpu} [{ttl2}] [TIE]'
        await ctx.send(f'```md\n#]BLACK JACK!\n \n{usrtxt}\n \n{cputxt}```')
    except discord.HTTPException: await exc(ctx, 1)
    except discord.Forbidden: await exc(ctx, 2)
    except discord.NotFound: await exc(ctx, 3)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(blkjck)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('blkjck')
    print('GOOD')

