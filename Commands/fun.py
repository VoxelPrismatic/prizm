#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import ast
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import numpy as np                #python3.7 -m pip install -U numpy
import numexpr as ne              #python3.7 -m pip install -U numexpr
import datetime, time
import aiofiles, io, asyncio      #python3.7 -m pip install -U aiofiles
import matplotlib.pyplot as pyplt #python3.7 -m pip install -U matplotlib // SEE SITE FOR MORE
import matplotlib, math, statistics, random
import platform, sys, sysconfig, traceback, shlex
from shlex import quote
from ast import literal_eval
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions
bot = commands.Bot(command_prefix=";]")
bot.remove_command("help")
logging.basicConfig(level='INFO')

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)
def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)
async def log(head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
    return msgs
async def _io(TxT):
    msgs = await log("AI I/O", f'{TxT}')
    print(f']{TxT}')
    return msgs
async def com(command):
    msgs = await log("COMMAND USED", f'COMMAND // {command}')
    print(f']{command}')
    return msgs
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

class cogname(commands.Cog):
    def __init__(self, bot): self.bot = bot
    async def cog_command_error(self, ctx, error):
        await log("It fucked up :C", f'ERROR // {error}\n> TRACE // {sys.exc_info()}')
        await ctx.send(embed=embedify('GG, It fucked up. [Hopefully] all data was logged'))

    @commands.command()
    async def cool(self, ctx, user: int):
        strtemp = '////////'
        await com('DELAYED RICK')
        await ctx.channel.purge(limit = 1)
        coolthing = await ctx.send(strtemp)
        varslol = True
        rickroll = f'''
Never gonna give <@{user}> up!
Never gonna let <@{user}> down!
Never gonna run around, and, desert you!
Never gonna make <@{user}> cry!
Never gonna say goodbye!
Never gonna run around, and, desert you!
'''
        while varslol == True:
            try:
                for x in range(125):
                    strtemp = f'{strtemp}////////'
                    await coolthing.edit(content = f'{strtemp}')
                varslol = False
                await ctx.send(rickroll)
            except:
                if varslol == False: await coolthing.edit(rickroll)
                else:
                    await ctx.send('YOU WILL NOT END THIS!')
                    strtemp = '////////'
                    coolthing = await ctx.send(strtemp)

    @commands.command()
    async def react(self, ctx, mID: int, *reactions):
        await ctx.channel.purge(limit = 1)
        await com(f"REACTIONS [{reactions}] TO mID[{mID}]")
        message = await ctx.fetch_message(mID)
        for reaction in reactions:
            try: await message.add_reaction(reaction)
            except discord.HTTPException: await exc(ctx, 1)
            except discord.Forbidden: await exc(ctx, 2)
            except discord.NotFound: await exc(ctx, 3)
    
    @commands.command()
    async def blkjck(self, ctx):
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
            await com('BJ')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def spam(self, ctx, num: int):
        if num > 10000: num = 10000
        send = ""
        data = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcsdefghgijklmnopqrstuvwxyz1234567890!@#$%^&*()-_=+[]{}\"\'<,>./?\\|`~"
        for x in range(num):
            send = send+(data[rand(0,len(data)-1)])
            if len(send) == 2000:
                await ctx.send(send)
                send = ""
        if len(send) > 0: await ctx.send(send)
        await com('SPAM')
    
    @commands.command()
    async def dnd(self, ctx):
        await com(']DND')
        try: await ctx.send(embed=embedify(f"```md\n# DND!\nD4 ~ {rand(1,4)}\nD6 ~ {rand(1,6)}\nD8 ~ {rand(1,8)}\nD10 ~ {rand(1,10)}\nD12 ~ {rand(1,12)}\nD20 ~ {rand(1,20)}\n```"))
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def rick(self, ctx):
        await com('RICKROLLD')
        await ctx.send(embed=embedify('''Never gonna give you up!
Never gonna let you down!
Never gonna run around and, desert you!
Never gonna make you cry!
Never gonna say goodbye!
Never gonna run around and, desert you!'''))

    @commands.command()
    async def binary(self, ctx, *, st):
        try:
            sr = st.replace(' ', '')
            await ctx.send(embed=embedify(f'{"".join([chr(int(sr[i:i+8], 2)) for i in range(0, len(sr), 8)])}'))
        except ValueError:
            await ctx.send(embed=embedify(f'{"".join((bin(ord(x))[2:].zfill(8) for x in st))}'))
        await com("BINARY <> ASCII")

    @commands.command()
    async def coin(ctx, *nums: int):
        try:
            if len(nums) == 0: num = 1
            else: num = int(nums[0])
            tcnt = y = hcnt = 0
            outp = ""
            if num > 5000:
                await ctx.send('```]To prevent spam, MAX = 5000```')
                num = 5000
            await com("COIN FLIP")
            for x in range(num):
                if rand(0,1) == 1:
                    tcnt+=1; outp = outp+"[T] "
                else:
                    hcnt+=1; outp = outp+"[H] "
                if y == 497:
                    await ctx.send(f'```{outp}```')
                    outp = ""; y = 0
                else: y+=1
            if y != 0: await ctx.send(f'```{outp}```')
            await ctx.send(f'```]HEAD // {hcnt}\n]TAIL // {tcnt}```')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def rng(self, ctx, rngl: int, rngh: int, *nums: int):
        try:
            if len(nums) == 0: num = 1
            else: num = int(nums[0])
            if num > 2000:
                await ctx.send('```]To prevent spam, MAX = 2000```')
                num = 2000
            send = ""; temp = 0; ttl = []
            await ctx.send(f'```diff\n-] RNG BETWEEN {rngl} & {rngh}```')
            await com(f'RNG BETWEEN {rngl} & {rngh}')
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

    @commands.command()
    async def slots(self, ctx):
        try:
            slot = ["[X]","[Y]","[Z]","[1]","[2]",
                    "[3]","[0]","[V]","[U]","[@]",
                    "[%]","[#]","[P]","[+]","[/]",
                    "[*]","[>]","[<]","[;]","[!]",
                    "[]]","[?]","[+]","[[]","[*]"]
            slot1 = rand(0,len(slot)-1)
            slot2 = rand(0,len(slot)-1)
            slot3 = rand(0,len(slot)-1)
            slotsend = f'''
-] {slot[slot1-1]}{slot[slot2-1]}{slot[slot3-1]}
+]>{slot[slot1]}{slot[slot2]}{slot[slot3]}<
-] {slot[slot1+1]}{slot[slot2+1]}{slot[slot3+1]}'''
            if slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
                await ctx.send(embed=embedify(f'```diff\n-{slotsend}\n \n-] WIN!```'))
            else:
                await ctx.send(embed=embedify(f'```diff\n{slotsend}\n \n-] LOST```'))
            await com("SLOTS")
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)
    
##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    bot.add_cog(cogname(bot))
