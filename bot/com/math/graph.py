#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import io
import discord                    #python3.7 -m pip install -U discord.py
import logging
import typing
import numpy as np                #python3.7 -m pip install -U numpy
import numexpr as ne              #python3.7 -m pip install -U numexpr
import matplotlib.pyplot as pyplt #python3.7 -m pip install -U matplotlib // SEE SITE FOR MORE
import matplotlib
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
async def graph(ctx, xmin:int,xmax:int,*eqs):
    xmin =min(xmin,xmax); xmax = max(xmax,xmin); eqs = list(eqs)
    msg = await ctx.send('`]GRAPHING`')
    for a in range(len(eqs)):
        for b in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            for z in '0123456789)': eqs[a] = eqs[a].replace(z+b,z+'*'+b)
    try:
        async with ctx.channel.typing():
            x = np.array(range(xmin, xmax))
            await msg.edit(content='`]EQUATION`')
            fig = pyplt.figure()
            fig, ax = pyplt.subplots()
            ax.tick_params(labelcolor='#0000ff')
            for eq in eqs: y = ne.evaluate(eq.replace("^", "**").replace(')(',')*(')) ; pyplt.plot(x, y)
            await msg.edit(content='`]PLOTTING`')
            fig.patch.set_facecolor('#002823')
            plotimg = io.BytesIO()
            pyplt.savefig(plotimg, format='png')
            plotimg.seek(0)
        await msg.delete()
        await ctx.send(file=discord.File(plotimg, f'{eq}.png'))
        pyplt.close()
    except discord.HTTPException: await exc(ctx, 1)
    except discord.Forbidden: await exc(ctx, 2)
    except discord.NotFound: await exc(ctx, 3)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(graph)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('graph')
    print('GOOD')
