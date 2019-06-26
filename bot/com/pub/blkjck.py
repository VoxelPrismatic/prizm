#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

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

@commands.command(aliases=["blackjack","bj"])
@commands.check(enbl)
async def blkjck(ctx):
        heart = ['A<3','2<3','3<3','4<3','5<3','6<3','7<3','8<3','9<3','T<3','J<3','Q<3','K<3']
        spade = ['A>)','2>)','3>)','4>)','5>)','6>)','7>)','8>)','9>)','T>)','J>)','Q>)','K>)']
        diam = ['A<>','2<>','3<>','4<>','5<>','6<>','7<>','8<>','9<>','T<>','J<>','Q<>','K<>']
        club = ['A>3','2>3','3>3','4>3','5>3','6>3','7>3','8>3','9>3','T>3','J>3','Q>3','K>3']
        ttl1 = 0; ttl2 = 0; stu = 0; usr = ""; cpu = ""; cputxt = ""; usrtxt = ""
        while ttl1 <= 18:
            stu = rand(0,3)
            if stu == 0: temp = random.randint(0, len(heart)-1); usr = usr+heart.pop(temp)+' '
            elif stu == 1: temp = random.randint(0, len(spade)-1); usr = usr+spade.pop(temp)+' '
            elif stu == 2: temp = random.randint(0, len(diam)-1); usr = usr+diam.pop(temp)+' '
            elif stu == 3: temp = random.randint(0, len(club)-1); usr = usr+club.pop(temp)+' '
            ttl1 += temp
        while ttl2 <= 18:
            stu = rand(0,3)
            if stu == 0: temp = random.randint(0, len(heart)-1); cpu = cpu+heart.pop(temp)+' '
            elif stu == 1: temp = random.randint(0, len(spade)-1); cpu = cpu+spade.pop(temp)+' '
            elif stu == 2: temp = random.randint(0, len(diam)-1); cpu = cpu+diam.pop(temp)+' '
            elif stu == 3: temp = random.randint(0, len(club)-1); cpu = cpu+club.pop(temp)+' '
            ttl2 += temp
        def rep(h): return h.replace('A','1').replace('T','10').replace('J','11').replace('Q','11').replace('K','11')
        ttl1 = sum([int(x[:-2]) for x in rep(usr).split(' ')])
        ttl2 = sum([int(x[:-2]) for x in rep(cpu).split(' ')])
        if ttl1 > 21: usrtxt = f'USER // {usr} [{ttl1}] [BUST]'
        elif ttl1 > ttl2: usrtxt = f'USER // {usr} [{ttl1}] [WIN]'
        elif ttl1 < ttl2: usrtxt = f'USER // {usr} [{ttl1}] [LOSS]'
        if ttl2 > 21: cputxt = f'COMP // {cpu} [{ttl2}] [BUST]'
        elif ttl2 > ttl1: cputxt = f'COMP // {cpu} [{ttl2}] [WIN]'
        elif ttl2 < ttl1: cputxt = f'COMP // {cpu} [{ttl2}] [LOSS]'
        if ttl1 == ttl2:
            usrtxt = f'USER // {usr} [{ttl1}] [TIE]'
            cputxt = f'COMP // {cpu} [{ttl2}] [TIE]'
        await ctx.send(f'```md\n#]BLACK JACK!``````diff\n+] {usrtxt}\n-] {cputxt}```')

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
