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
def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def rng(ctx, rngl: int, rngh: int, *nums: int):
    try:
        if len(nums) == 0: num = 1
        else: num = int(nums[0])
        if num > 2000:
            await ctx.send('```]To prevent spam, MAX = 2000```')
            num = 2000
        send = ""; temp = 0; ttl = []
        await ctx.send(f'```diff\n-] RNG BETWEEN {rngl} & {rngh}```')
        for x in range(num):
            temp = random.randint(rngl,rngh)
            if len(f'{send} {temp} ')<=1994:
                send += f'{temp} '; ttl.append(temp)
            else:
                await ctx.send(f'```{send}```')
                send = f'{temp} '; ttl.append(temp)
        if len(send) != 0: await ctx.send(f'```{send}```')
        await ctx.send(f'```COUNT // {len(ttl)}\nAVRGE // {sum(ttl)/len(ttl)}\nRANGE // {max(ttl)-min(ttl)}```')
    except discord.HTTPException: await exc(ctx, 1)
    except discord.Forbidden: await exc(ctx, 2)
    except discord.NotFound: await exc(ctx, 3)


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rng)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rng')
    print('GOOD')

