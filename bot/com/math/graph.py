#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import io
import discord                    #python3.7 -m pip install -U discord.py
import logging
import typing, math
import numpy as np                #python3.7 -m pip install -U numpy
import numexpr as ne              #python3.7 -m pip install -U numexpr
import matplotlib.pyplot as pyplt #python3.7 -m pip install -U matplotlib // SEE SITE FOR MORE
import matplotlib
from mpl_toolkits.axisartist.axislines import SubplotZero
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help='math',
                  brief = 'Your personal graphing calculator',
                  usage = ';]graph {xmin} {xmax} {eq1} {eq2} {...}',
                  description = 'XMAX [INT] - Maximum value of X\nXMIN [INT] - Minimum value of X\nEQx  [STR] - The equation in question')
@commands.check(enbl)
async def graph(ctx, xmin:int,xmax:int,*eqs):
    msg = await ctx.send('```#] JUST A SEC\n> PARSING```')
    xmin =min(xmin,xmax)
    xmax = max(xmax,xmin)
    eqs = list(eqs)
    for a in range(len(eqs)):
        for b in 'xy':
            for z in '0123456789)':
                eqs[a] = eqs[a].replace(z+b,z+'*'+b)
    async with ctx.channel.typing():
        styles = [('C4','--')]

        await msg.edit(content='```#] JUST A SEC\n> SETTING UP```')
        pyplt.style.use('dark_background')
        fig, ax = pyplt.subplots(facecolor='#003333', edgecolor='#002222')
        ax.set_facecolor('#003333')
        ax.grid(b=True, color='#004444', linewidth=1)
        ax.tick_params(labelcolor='#00ffff')
        ax.set_facecolor=('#00ffff')
        ax.set_ylim(top=xmax, bottom=xmin)
        ax.set_xlim(left=xmin, right=xmax)
        #fig.add_subplot(ax)

        await msg.edit(content='```#] JUST A SEC\n> GRAPHING```')
        for eq in eqs:
            eq = eq.replace("^", "**").replace(')(',')*(')
            x = np.array(np.arange(xmin, xmax+1,0.01))
            y = np.array(np.arange(xmin, xmax+1,0.01))
            if 'x' in eq and 'y' in eq:
                xp = []
                yp = []
                xx = np.array(np.arange(xmin, xmax+1,0.5))
                yy = np.array(np.arange(xmin, xmax+1,0.5))
                for x in xx:
                    for y in yy:
                        if ne.evaluate(eq.split('=')[0]) == ne.evaluate(eq.split('=')[-1]):
                            xp.append(xx)
                            yp.append(yy)
                x, y = xp, yp
            elif 'x' in eq:
                y = ne.evaluate(eq)
            else:
                x = ne.evaluate(eq)
            ax.plot(x, y, label=eq)

        await msg.edit(content='```#] JUST A SEC\n> CREATING LEGEND```')
        ax.legend(loc=3, fontsize='xx-small', facecolor='#005555', edgecolor='#001111')
        fig = ax.get_figure()
        plotimg = io.BytesIO()
        fig.set_edgecolor('#001111')
        fig.patch.set_facecolor('#002222')
        fig.savefig(plotimg, format='png')
        plotimg.seek(0)
    await msg.edit(content='```#] JUST A SEC\n> UPLOADING TO DISCORD```')
    await ctx.send(file=discord.File(plotimg, f'{eq}.png'))
    await msg.delete()
    pyplt.close()

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