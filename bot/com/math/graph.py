#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import io, re
import discord                    #python3.7 -m pip install -U discord.py
import logging, random
import sympy as sp
import typing, math, cmath
from typing import Optional as Opt
import numpy as np                #python3.7 -m pip install -U numpy
import numexpr as ne              #python3.7 -m pip install -U numexpr
import matplotlib.pyplot as pyplt #python3.7 -m pip install -U matplotlib // SEE SITE FOR MORE 
import matplotlib
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from numpy import nanargmax as NAmax, nanargmin as NAmin, argmax as Amax, \
                  argmin as Amin, nanmax as Nmax, nanmin as Nmin
##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

def arc(st: str):
    return re.sub(r"a((sin|cos|tan))", r"arc\1", st)
def nrc(st: str):
    return re.sub(r"arc((sin|cos|tan))", r"a\1", st)
def y0(st: str):
    return st.replace('y', '0')
def x0(st: str):
    return st.replace('x', '0')
def rf(itm, by=4):
    try:
        return round(float(itm), by)
    except:
        return str(itm)
def slvr0(itm):
    return sp.solve(itm[0][0], itm[0][1])
def slvr1(itm):
    return sp.solve(itm[1][0], itm[1][1])
def evl(itm):
    return ne.evaluate(arc(itm))
def fmt(itm):
    return itm.replace('**', '^').replace(str(np.pi), '\u03c0')

async def multilabels(ctx, x, y, eq0, eq1, eq2, solved, maximum, minimum, zeros, yinter):
    eqA = eq0
    if maximum:
        itm1, itm2 = NAmax(eq1), NAmax(eq2)
        if max(eq1[itm1], eq2[itm2]) == eq1[itm1]: iX, iY = itm1, eq1[itm1]
        else: iX, iY = itm2, eq2[itm2]
        eqA += f" // MAX ] [{rf(x[iX])}, {rf(iY)}]"
    if minimum:
        itm1, itm2 = NAmin(eq1), NAmin(eq2)
        if min(eq1[itm1], eq2[itm2]) == eq1[itm1]: iX, iY = itm1, eq1[itm1]
        else: iX, iY = itm2, eq2[itm2]
        eq0 += f" // MIN ] [{rf(x[iX])}, {rf(iY)}]"
    if zeros:
        st1, st2 = "", ""
        if str(solved[0][1]) == 'y':
            st1 = f"[{rf(evl(y0(eq1)))}, 0.0]"
            st2 = f"[{rf(evl(y0(eq2)))}, 0.0]"
        else:
            st1 = ', '.join(f'[{rf(z)}, 0.0]' for z in slvr0(solved))
            st2 = ', '.join(f'[{rf(z)}, 0.0]' for z in slvr1(solved))
        eq0 += " // ZEROS ] "+(', '.join([st1, st2]) if st1 or st2 else 'NONE')
    if yinter:
        st1, st2 = "", ""
        if str(solved[0][1]) == 'x':
            st1 = f"[0.0, {rf(evl(x0(eq1)))}]"
            st2 = f"[0.0, {rf(evl(x0(eq2)))}]"
        else:
            st1 = ', '.join(f'[0.0, {rf(z)}]' for z in slvr0(solved))
            st2 = ', '.join(f'[0.0, {rf(z)}]' for z in slvr1(solved))
        eq0 += " // Y-INT ] "+(', '.join([st1, st2]) if st1 or st2 else 'NONE')
    return fmt(eq0)

async def labels(ctx, x, y, eq, maximum, minimum, zeros, yinter):
    gx = evl(str(sp.simplify(eq))).round(8)
    gr = gx.flatten()
    label = fmt(eq)
    if minimum: 
        label += f" // MIN ] [{rf(x[NAmin(gr)])}, {rf(Nmin(gr))}]"
    if maximum: 
        label += f" // MAX ] [{rf(x[NAmax(gr)])}, {rf(Nmax(gr))}]"
    if zeros:
        if 'y' in eq:
            st = f"[{rf(evl(y0(eq)))}, 0.0]"
        else:
            x = sp.Symbol('x')
            st = ', '.join(f'[{rf(z)}, 0.0]' for z in sp.solve(eq, x))
        label += f" // ZEROS ] {st if st else 'NONE'}"
    if yinter:
        if 'x' in eq:
            st = f"[0.0, {rf(evl(x0(eq)))}]"
        else:
            y = sp.Symbol('y')
            st = ', '.join(f'[0.0, {rf(z)}]' for z in sp.solve(eq, y))
        label += f" // Y-INT ] {st if st else 'NONE'}"
    return label, gx

@commands.command(help='math',
                  brief = 'Your personal graphing calculator',
                  usage = ';]graph {?window} {eq1} | {eq2} | {...}',
                  description = 'WINDOW [INT x 4] - Set XMIN, XMAX, YMIN, YMAX in that order\nEQx  [STR] - The equation in question')
@commands.check(enbl)
async def graph(ctx, xmin: Opt[int] = -10, xmax: Opt[int] = 10, 
                ymin: Opt[int] = 0, ymax: Opt[int] = 0, *, eqs):
    msg = await ctx.send('```#] JUST A SEC\n> PARSING```')
    xmin, xmax = min(xmin, xmax), max(xmax, xmin)
    ymin, ymax = min(ymin, ymax), max(ymax, ymin)
    if not (ymin and ymax):
        ymin, ymax = xmin, xmax
    eqA = []
    eqs = eqs.split('|')
    for eq in eqs:
        eq = re.sub(r"(\d+)([xy\(])", r"\1*\2", re.sub(r"([xy\)])(\d+)",r"\1*\2",eq))
        eq = eq.replace('^','**').lower().strip()
        eq = eq.replace('pi', str(np.pi)).replace('\u03c0', str(np.pi))
        eq = re.sub(r"(^[xy][^><]=[^><])?([^><]=[^><][xy]$)?",r"",eq)
        mx, mn, zr, yi = 0, 0, 0, 0
        if '--max' in eq: mx = 1; eq = eq.replace('--max','')
        if '--min' in eq: mn = 1; eq = eq.replace('--min','')
        if '--zero' in eq: zr = 1; eq = eq.replace('--zero','')
        if '--yint' in eq: yi = 1; eq = eq.replace('--yint','')
        eqA.append((eq, mx, mn, zr, yi))
    async with ctx.channel.typing():
        await msg.edit(content='```#] JUST A SEC\n> SETTING UP```')
        pyplt.style.use(['dark_background','seaborn-pastel'])
        fig, ax = pyplt.subplots(facecolor='#003333', edgecolor='#002222')
        ax.set_facecolor('#003333')
        ax.grid(b=True, color='#004444', linewidth=1)
        ax.tick_params(labelcolor='#00ffff')
        ax.set_facecolor=('#00ffff')
        ax.set_ylim(top=ymax, bottom=ymin)
        ax.set_xlim(left=xmin, right=xmax)
        size = np.arange(min(xmin, ymin), max(xmax, ymax)+1, 
                         (abs(min(xmin, ymin)) + abs(max(xmax, ymax)))/10000)
        array = np.array(size)
        x, y = array, array
        z = ne.evaluate('y-y' if max(xmax, ymax) == ymax else 'x-x')
        ax.plot(x, z, 'w', z, y, 'w', linewidth=1) #Grid Lines

        await msg.edit(content='```#] JUST A SEC\n> GRAPHING```')
        for eq, maximum, minimum, zeros, yinter in eqA:
            x, y= array, array
            if ('x' in eq and 'y' in eq) or ('>' in eq or '<' in eq):
                x, y = sp.symbols('x y')
                itm = [z for z in ['>=','<=','=>', '=<', '>','<','='] if z in eq][0]
                solved = sp.solvers.solve(f"({eq.split(itm)[0]})-({eq.split(itm)[1]})",x,y)
                x, y = array, array
                color = '#' + ''.join(random.choice('2468ACE') for z in range(6))
                eq1, eq2 = evl(str(solved[0][0])).round(8), None
                if len(solved) == 2:
                    eq2 = evl(str(solved[1][0]))
                elif str(solved[0][0]).startswith('-') or '>' in eq:
                    eq2 = evl(f'x-x+{xmin}' if min(xmin, ymin) == xmin else f'y-y+{ymin}').round(8)
                elif not str(solved[0][0]).startswith('-') or '<' in eq:
                    eq2 = evl(f'0*x+{xmax}' if max(xmax, ymax) == xmax else f'0*y+{ymax}').round(8)
                if itm in ['>=', '=>']:
                    inequal = eq1 >= eq2
                elif itm in ['<=', '=<']:
                    inequal = eq1 <= eq2
                elif itm == '<':
                    inequal = eq1 < eq2
                elif itm == '>':
                     inequal = eq1 > eq2
                label = await multilabels(ctx, x, y, eq, eq1, eq2, solved, maximum, minimum, zeros, yinter)
                if str(solved[0][1]) == 'x':
                    ax.plot(x, eq1, color=color)
                    ax.plot(x, eq2, color=color, label=label)
                    if '>' in itm or '<' in itm:
                        ax.fill_between(x, eq1, eq2,facecolor=color, alpha=.4, where=inequal)
                else:
                    ax.plot(eq1, y, color=color)
                    ax.plot(eq2, y, color=color, label=label)
                    if '>' in itm or '<' in itm:
                        ax.fill_between(y, eq1, eq2, facecolor=color, alpha=.4, where=inequal)
            elif 'x' in eq:
                label, gr = await labels(ctx, x, y, eq, maximum, minimum, zeros, yinter)
                ax.plot(x, gr, label=label)
            elif 'y' in eq:
                label, gr = await labels(ctx, x, y, eq, maximum, minimum, zeros, yinter)
                ax.plot(gr, y, label=label)

        await msg.edit(content='```#] JUST A SEC\n> FINISHING UP```')
        ax.legend(loc=3, fontsize='xx-small', facecolor='#005555', edgecolor='#001111')
        fig = ax.get_figure()
        plotimg = io.BytesIO()
        fig.set_edgecolor('#001111')
        fig.patch.set_facecolor('#002222')
        fig.savefig(plotimg, format='png', dpi=600)
        plotimg.seek(0)
    await msg.edit(content='```#] JUST A SEC\n> UPLOADING TO DISCORD```')
    await ctx.send("```md\n#] HERE IS YOUR GRAPH!```", file=discord.File(plotimg, 'PRIZM_graph.png'))
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