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
def evl(itm, x, y):
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
            st1 = f"[{rf(evl(y0(eq1), x, y))}, 0.0]"
            st2 = f"[{rf(evl(y0(eq2), x, y))}, 0.0]"
        else:
            st1 = ', '.join(f'[{rf(z)}, 0.0]' for z in slvr0(solved))
            st2 = ', '.join(f'[{rf(z)}, 0.0]' for z in slvr1(solved))
        eq0 += " // ZEROS ] "+(', '.join([st1, st2]) if st1 or st2 else 'NONE')
    if yinter:
        st1, st2 = "", ""
        if str(solved[0][1]) == 'x':
            st1 = f"[0.0, {rf(evl(x0(eq1), x, y))}]"
            st2 = f"[0.0, {rf(evl(x0(eq2), x, y))}]"
        else:
            st1 = ', '.join(f'[0.0, {rf(z)}]' for z in slvr0(solved))
            st2 = ', '.join(f'[0.0, {rf(z)}]' for z in slvr1(solved))
        eq0 += " // Y-INT ] "+(', '.join([st1, st2]) if st1 or st2 else 'NONE')
    return fmt(eq0)

def asymptote(ln, ls, eq, lt):
    ls = list(ls)
    cur = [([],[])]
    for i in range(1, len(ls)-1):
        j, k = float(ls[i]), float(ls[i+1])
        cur[-1][0].append(ln[i])
        cur[-1][1].append(ls[i])
        if ((j > 1 and k < -1) or (j < -1 and k > -1)) and j != np.nan and k != np.nan:
            z = np.arange(ln[i], ln[i+1], 0.00001)
            fn = ne.evaluate(arc(eq.replace(lt, "z")))
            if NAmin(fn) == NAmax(fn) + 1 or NAmin(fn) == NAmax(fn) - 1:
                cur.append(([],[]))
    return cur

async def labels(ctx, x, y, eq, maximum, minimum, zeros, yinter):
    gx = evl(str(sp.simplify(eq)), x, y).round(8)
    gr = gx.flatten()
    label = fmt(eq)
    if minimum:
        label += f" // MIN ] [{rf(x[NAmin(gr)])}, {rf(Nmin(gr))}]"
    if maximum:
        label += f" // MAX ] [{rf(x[NAmax(gr)])}, {rf(Nmax(gr))}]"
    if zeros:
        if 'y' in eq:
            st = f"[{rf(evl(y0(eq), x, y))}, 0.0]"
        else:
            x = sp.Symbol('x')
            st = ', '.join(f'[{rf(z)}, 0.0]' for z in sp.solve(eq, x))
        label += f" // ZEROS ] {st if st else 'NONE'}"
    if yinter:
        if 'x' in eq:
            st = f"[0.0, {rf(evl(x0(eq), x, y))}]"
        else:
            y = sp.Symbol('y')
            st = ', '.join(f'[0.0, {rf(z)}]' for z in sp.solve(eq, y))
        label += f" // Y-INT ] {st if st else 'NONE'}"
    return label, gx

@commands.command(aliases = [],
                      help = 'math',
                      brief = 'Your personal graphing calculator',
                      usage = ';]graph {?window} {eq1} {?ops} | {eq2} {?ops} | {...} {?ops}',
                      description = '''\
WINDOW [NUMBERS] - Set XMIN, XMAX, YMIN, YMAX in that order
EQx    [TEXT   ] - The equation to graph
OPS    [TEXT   ] - Other arguments
> This list is long, check online for more details
*Use '>=' and '<=' for 'at least' and 'at most' graphs [respectively]
*XY equations like `x^2+y^2` MUST have an equal sign
''')
@commands.check(enbl)
async def graph(ctx, xmin: Opt[float] = -10, xmax: Opt[float] = 10,
                ymin: Opt[float] = 0, ymax: Opt[float] = 0, *, eqs):
    msg = await ctx.send('```md\n#] JUST A SEC\n> INITIALIZING```')
    ##/// INITIALIZE THINGS
    xmin, xmax = min(xmin, xmax), max(xmax, xmin)
    ymin, ymax = min(ymin, ymax), max(ymax, ymin)
    _color = ["#642b26", "#0d0a69", "#0e4bc5", "#c3c532", "#b2bfc8",
              "#9aabcd", "#7a87ae", "#555880", "#313446", "#0000c0",
              "#c43c24", "#1d1c24", "#c503f3", "#29742c", "#d98034"]
    _BandW = ["#333333", "#444444", "#353535", "#666666", "#777777",
              "#eeeeee", "#ffffff", "#888888", "#989898", "#999999",
              "#787878", "#797979", "#676767", "#595959", "#aaaaaa"]
    colors = ["#ff0000", "#ff8800", "#ffff00", "#88ff00", "#00ff00",
              "#00ff88", "#00ffff", "#0088ff", "#0000ff", "#8800ff",
              "#ff00ff", "#ff0088", "#888888", "#aaffff", "#88aaaa"]
    xr = abs(xmin)+abs(xmax)
    try:
        cstep = int(eqs.split('---step=')[1].split(' ')[0])
    except IndexError:
        cstep = 0
    calculators = {
        ##/// OTHERS
        r"---zoom": [640, colors, 'prizm'],
        r"---smol": [64, colors, 'prizm'],
        r"---step=\d+": [cstep, colors, 'prizm'],

        ##/// TI
        r"---ti8[43]p?cs?e": [132, _color, 'ti84ce'],
        r"---ti8[4321]p?(se)?": [47, _BandW, 'ti82'],
        r"---ti73p?(se)?": [47, _BandW, 'ti73'],
        r"---ti8[56](se)?": [64, _BandW, 'ti85'],
        r"---ti89t?": [80, _BandW, 'ti89t'],
        r"---ti80": [32, _BandW, 'ti80'],
        r"---nspirecx(ii)?(-t)?(cas)?": [160, _color, 'nspirecx'],
        r"---nspire(cas)?": [160, _BandW, 'nspire'],
        r"---ti92(ii|p)?": [120, _BandW, 'ti92'],

        ##/// CASIO
        r"---fx7000ga?": [96, _BandW, 'fx7000g'],
        r"---fx2p": [128, _BandW, 'fx2p'],
        r"---cfx9850gbp": [128, _BandW, 'fx2p'],

        ##/// HP
        r"---hp28[cs]": [137, _BandW, 'hp28c'],
        r"---hp48(g|gii|gp|gx|s|sx)": [131, _BandW, 'hp48'],
        r"---hp49gp?": [131, _BandW, 'hp48'],
        r"---hp50g?p?": [131, _BandW, 'hp48'],
        r"---(hp)?prime": [320, _BandW, 'hpprime'],
        r"---hp3[98]g(ii|s|p)?": [131, _BandW, 'hp48'],
        r"---hp40gs?": [131, _BandW, 'hp48'],
        r"---hp9g": [35, _BandW, 'hp9g'],
        r"---hp42s": [131, _BandW, 'hp42s']
    }
    for calc in calculators:
        if re.search(calc, eqs):
            step = xr / calculators[calc][0]
            colors = calculators[calc][1]
            eqs = re.sub(calc, "", eqs)
            styler = calculators[calc][2]
            break
    else:
        step = (abs(max(xmax, ymax)) + abs(min(xmin, ymin))) / 10000
        styler = 'prizm'
    if not (ymin and ymax):
        ymin, ymax = xmin, xmax
    eqA = []
    eqs = eqs.split('|')
    await msg.edit(content='```md\n#] JUST A SEC\n> PARSING EQUATIONS```')
    for eq in eqs:
        mx, mn, zr, yi, dt = 0, 0, 0, 0, 0
        eq = eq.replace('^','**').lower().strip()
        if '--max' in eq: mx = 1; eq = eq.replace('--max','')
        if '--min' in eq: mn = 1; eq = eq.replace('--min','')
        if '--zero' in eq: zr = 1; eq = eq.replace('--zero','')
        if '--yint' in eq: yi = 1; eq = eq.replace('--yint','')
        if '--detect' in eq: dt = 1; eq = eq.replace('--detect','')
        if '--asymptote' in eq: dt = 1; eq = eq.replace('--asymptote','')
        if '--det' in eq: dt = 1; eq = eq.replace('--det','')
        if '--asym' in eq: dt = 1; eq = eq.replace('--asym','')
        eq = re.sub(r"(\d+)([xy\(])", r"\1*\2", re.sub(r"([xy\)])(\d+)",r"\1*\2",eq))
        eq = eq.replace('pi', str(np.pi)).replace('\u03c0', str(np.pi)).replace("e", str(math.e))
        eq = re.sub(r"(^[xy][^><]=[^><])?([^><]=[^><][xy]$)?", "", eq)
        eq = re.sub(r"([xy\d])\(", r"\1*(", re.sub(r"\)([xy\d])", r")*\1", eq))
        eq = re.sub(r"(\d+)root\((.*)\)", r"(\2)^(1/\1)", eq)
        eqA.append((nrc(eq), mx, mn, zr, yi, dt))

    ##/// STYLIZE
    async with ctx.channel.typing():
        await msg.edit(content='```md\n#] JUST A SEC\n> STYLIZING```')
        pyplt.style.use(styler)
        fig, ax = pyplt.subplots()
        ax.set_ylim(top=ymax, bottom=ymin)
        ax.set_xlim(left=xmin, right=xmax)
        mn, mx = min(xmin, ymin), max(xmax, ymax)
        size = np.arange(mn, mx, step)
        array = np.array(size)
        x, y = array, array
        z = ne.evaluate('y-y' if max(xmax, ymax) == ymax else 'x-x')
        ax.plot(x, z, 'w', z, y, 'w', linewidth=1) #Grid Lines

        await msg.edit(content='```md\n#] JUST A SEC\n> GRAPHING```')
        for eq, maximum, minimum, zeros, yinter, asymp in eqA:
            color = random.choice(colors)
            x, y= array, array

            ##/// X and Y EQUATIONS
            if ('x' in eq and 'y' in eq) or ('>' in eq or '<' in eq):
                x, y = sp.symbols('x y')
                itm = [z for z in ['>=','<=','=>', '=<', '>','<','='] if z in eq][0]
                solved = sp.solvers.solve(f"({eq.split(itm)[0]})-({eq.split(itm)[1]})",x,y)
                x, y = array, array
                eq1, eq2 = evl(str(solved[0][0]), x, y).round(8), None
                if len(solved) == 2:
                    eq2 = evl(str(solved[1][0]), x, y)
                elif str(solved[0][0]).startswith('-') or '>' in eq:
                    eq2 = evl(f'x-x+{xmin}' if min(xmin, ymin) == xmin else f'y-y+{ymin}', x, y).round(8)
                elif not str(solved[0][0]).startswith('-') or '<' in eq:
                    eq2 = evl(f'0*x+{xmax}' if max(xmax, ymax) == xmax else f'0*y+{ymax}', x, y).round(8)
                if itm in ['>=', '=>']: inequal = eq1 >= eq2
                elif itm in ['<=', '=<']: inequal = eq1 <= eq2
                elif itm == '<': inequal = eq1 < eq2
                elif itm == '>': inequal = eq1 > eq2
                label = await multilabels(ctx, x, y, eq, eq1, eq2, solved,
                                          maximum, minimum, zeros, yinter)
                if str(solved[0][1]) == 'x':
                    if not asymp:
                        ax.plot(x, eq1, color=color)
                        ax.plot(x, eq2, color=color, label=label)
                    else:
                        for line, sect in asymptote(x, eq1, str(solved[0][0]), "x"):
                             ax.plot(line, sect, color=color)
                        for line, sect in asymptote(x, eq2, str(solved[1][0]), "x"):
                             ax.plot(line, sect, color=color)
                        ax.plot(line, sect, label=label, color=color)
                    if '>' in itm or '<' in itm:
                        ax.fill_between(x, eq1, eq2, facecolor=color, alpha=.4, where=inequal)
                else:
                    if not asymp:
                        ax.plot(eq1, y, color=color)
                        ax.plot(eq2, y, color=color, label=label)
                    else:
                        for line, sect in asymptote(y, eq1, str(solved[0][0]), "y"):
                             ax.plot(sect, line, color=color)
                        for line, sect in asymptote(y, eq2, str(solved[1][0]), "y"):
                             ax.plot(sect, line, color=color)
                        ax.plot(sect, line, label=label, color=color)
                    if '>' in itm or '<' in itm:
                        ax.fill_between(y, eq1, eq2, facecolor=color, alpha=.4, where=inequal)


            ##/// X ONLY
            elif 'x' in eq:
                label, gr = await labels(ctx, x, y, eq, maximum, minimum, zeros, yinter)
                if not asymp:
                     ax.plot(x, gr, label=label, color=color)
                else:
                     for line, sect in asymptote(x, gr, eq, "x"):
                         ax.plot(line, sect, color=color)
                     ax.plot(line, sect, label=label, color=color)


            ##/// Y ONLY
            elif 'y' in eq:
                label, gr = await labels(ctx, x, y, eq, maximum, minimum, zeros, yinter)
                if not asymp:
                     ax.plot(gr, y, label=label, color=color)
                else:
                     for line, sect in asymptote(y, gr, eq, "y"):
                         ax.plot(sect, line, color=color)
                     ax.plot(sect, line, label=label, color=color)

        await msg.edit(content='```md\n#] JUST A SEC\n> SAVING IMAGE```')
        ax.legend(loc = 3)
        plotimg = io.BytesIO()
        ax.get_figure().savefig(plotimg, format = 'png', dpi = 600)
        plotimg.seek(0)
    await msg.edit(content='```md\n#] JUST A SEC\n> UPLOADING TO DISCORD```')
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
