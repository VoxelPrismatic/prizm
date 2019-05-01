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

class maths(commands.Cog):
    def __init__(self, bot): self.bot = bot
    async def cog_command_error(self, ctx, error):
        await log("It fucked up :C", f'ERROR // {error}\n> TRACE // {sys.exc_info()}')
        await ctx.send(embed=embedify('GG, It fucked up. [Hopefully] all data was logged'))

    @commands.command()
    async def graph(self, ctx, eq, xmin: int, xmax: int):
        msg = await ctx.send('`]GRAPHING`')
        await com(f'GRAPH {eq} -X[{xmin}] +X[{xmax}]')
        try:
            x = np.array(range(xmin, xmax))
            y = ne.evaluate(eq.replace("^", "**"))
            fig = pyplt.figure()
            fig, ax = pyplt.subplots()
            ax.set_facecolor('#002823')
            ax.tick_params(labelcolor='#0000ff')
            pyplt.plot(x, y)
            fig.patch.set_facecolor('#002823')
            plotimg = io.BytesIO()
            pyplt.savefig(plotimg, format='png')
            plotimg.seek(0)
            await msg.delete()
            await ctx.send(file=discord.File(plotimg, 'img.png'))
            pyplt.close()
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def stats(self, ctx, *data: int):
        try: mod = str(statistics.mode(data))
        except: mod = "[NONE]"
        await ctx.send(embed=embedify(f'''```md
#] STATS
>   MAX // {max(data)}
>   MIN // {min(data)}
>   AVG // {statistics.mean(data)}
>   MOD // {mod}
>   MED // {statistics.median(data)}
> RANGE // {max(data)-min(data)}
> STDEV // {statistics.stdev(data)}
> LOMED // {statistics.median_low(data)}
> HIMED // {statistics.median_high(data)}
```'''))
        await com(f'STATS {data}')
        
        @commands.command()
    async def rto(self, ctx, int1: int, int2: int):
        factor = math.gcd(int1, int2)
        await ctx.send(f'```]FACT // {factor}\n]INT1 // {int1/factor}\n]INT2 // {int2/factor}```')
        await com('RTOLO')

    @commands.command()
    async def rad(self, ctx, D: int):
        K = 1
        for I in range(1,500):
            for J in range(2,1000):
                if not math.remainder(D, J**2):
                    D = D/(J**2); K = K*J
            if D == 1: break
        if D == 1: await ctx.send(f'```]ANS // {K}```')
        elif K == 1: await ctx.send(f'```]ANS // √{D}```')
        else: await ctx.send(f'```]ANS // {K}√{D}```')
        await com('RADRED')
    
    @commands.command()
    async def quad(self, ctx, A: int, B: int, C: int):
        D = B**2 - 4*A*C; K = 1
        for I in range(1,500):
            for J in range(2,1000):
                if not math.remainder(D, J**2):
                    D = D/(J**2); K = K*J
            if D == 1:break
        if D == 1: STR = f'{K}'
        elif K == 1: STR = f'√{D}'
        else: STR = f'{K}√{D}'
        await ctx.send(embed=embedify(f'''```md
#]QUADRATICS``````
{-B}+-{STR}
------------
{2*A}``````diff
+] [{-B/(2*A)} + {K/(2*A)}√{D}] {(-B+((B**2)-2*A*C)**.5)/(2*A)}
-] [{-B/(2*A)} - {K/(2*A)}√{D}] {(-B-((B**2)-2*A*C)**.5)/(2*A)}```'''))
        await com('QUAD FORM')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    bot.add_cog(maths(bot))
