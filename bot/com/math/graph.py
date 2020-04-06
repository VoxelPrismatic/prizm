#!/usr/bin/env python3
# -*- coding: utf-8 -*
#/// DEPENDENCIES
import io, re
import discord
from PIL import Image
import logging, random
import sympy as sp
import typing, math, cmath
from typing import Optional as Opt
import numpy as np
import numexpr as ne
import matplotlib.pyplot as pyplt
import matplotlib as mpl
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.parse_eq import parse_eq, unparse_eq as fmt
from numpy import nanargmax as NAmax, nanargmin as NAmin, argmax as Amax, \
                  argmin as Amin, nanmax as Nmax, nanmin as Nmin

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

calculators = {
    ##/// OTHERS
    r"---zoom": [500, 'prizm'],
    r"---smol": [100, 'prizm'],
    r"---step=\d+": [0, 'prizm'],
    ##/// TI
    r"---ti8[43][p+]?cs?e": [132, 'ti84ce'],
    r"---ti8[4321][p+s]?(se)?": [47, 'ti82'],
    r"---ti73[p+]?e?(se)?": [47, 'ti73'],
    r"---ti8[56](se)?": [64, 'ti85'],
    r"---ti89t?": [80, 'ti89t'],
    r"---ti80": [32, 'ti80'],
    r"---nspirecx(ii|2)?(-t)?(cas)?": [160, 'nspirecx'],
    r"---nspire(cas)?": [160, 'nspire'],
    r"---ti92(ii|[p+]|2)?": [120, 'ti92'],
    ##/// CASIO
    r"---fx7000ga?": [96, 'fx7000g'],
    r"---fx2p": [128, 'fx2p'],
    r"---cfx9850gbp": [128, 'fx2p'],
    r"---fx9950cg": [128, 'cfx9950gc'],
    r"---fx9750g(ii|2)?": [128, 'fx9750g'],
    r"---fxcg500": [320, 'fxcg500'],
    r"---fxcg50": [384, 'fxcg50'],
    ##/// HP
    r"---hp28[cs]": [137, 'hp28c'],
    r"---hp48(g|gii|gp|gx|s|sx)": [131, 'hp48'],
    r"---hp49gp?": [131, 'hp48'],
    r"---hp50g?p?": [131, 'hp48'],
    r"---(hp)?prime": [320, 'hpprime'],
    r"---hp3[98]g(ii|s|p)?": [131, 'hp48'],
    r"---hp40gs?": [131, 'hp48'],
    r"---hp9g": [35, 'hp9g'],
    r"---hp42s": [131, 'hp42s'],

    ##/// OTHERS
    r"---numworks?": [10000, 'numworks'],
}

def arc(st: str):
    return re.sub(r"a((sin|cos|tan)h?)", r"arc\1", st)
def nrc(st: str):
    return re.sub(r"arc((sin|cos|tan)h?)", r"a\1", st)
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
def plotter(ax, x, y, label = None, color = None, polar = False):
    if polar:
        if type(x) == list:
            x = np.array(x)
        if type(y) == list:
            y = np.array(y)
        for z in np.argwhere(y < 0):
            y[z] = abs(y[z])
            x[z] += np.pi
    try:
        ax.plot(x, y, label = label, color = color)
    except ValueError:
        try:
            len(y)
            x = [x] * len(y)
        except TypeError:
            y = [y] * len(x)
        ax.plot(x, y, label = label, color = color)
    return ax
def filler(ax, z, eq1, eq2, color, inequal):
    ax.fill_between(z, eq1, eq2, facecolor = color, alpha = .2, where = inequal)
    return ax
def option(nam, eq, val = 0):
    if nam in eq:
        return eq.replace(nam, ""), 1
    return eq, val
def grab_window(eq, x, y, step, ymax, polar):
    m = re.search("\{(.*)\}", eq)
    if m:
        window = m[1]
        res = [
            r"x *(=?[<>]=?) *(-?\d+(\.\d+)?)",
            r"(\-?\d+(\.\d+)?) *(=?[<>]=?) *x",
            r"y *(=?[<>]=?) *(-?\d+(\.\d+)?)",
            r"(-?\d+(\.\d+)?) *(=?[<>]=?) *y"
        ]
        for sect in window.split(","):
            sect = sect.strip()
            for r in res:
                m = re.search(r, sect)
                if m:
                    if "x" in r:
                        z = x
                    else:
                        z = y
                    if m[1] == "<":
                        z = np.where(z < float(m[2]), z, np.nan)
                    elif m[1] == ">":
                        z = np.where(z > float(m[2]), z, np.nan)
                    elif m[1] in [">=", "=>", "=>="]:
                        z = np.where(z >= float(m[2]), z, np.nan)
                    elif m[1] in ["<=", "=<", "=<="]:
                        z = np.where(z <= float(m[2]), z, np.nan)
                    if "x" in r:
                        x = z
                    else:
                        y = z
    return re.sub(r"\{.*\}", "", eq), x, y

def multilabels(x, y, eq0, eq1, eq2, solved, maximum, minimum, zeros, yinter):
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
    cur = [[ [], [] ]] #Groups of functions
    for i in range(1, len(ls)-1):
        j, k = float(ls[i]), float(ls[i+1])
        cur[-1][0].append(ln[i])
        cur[-1][1].append(ls[i])
        if ((j > 1 and k < -1) or (j < -1 and k > -1)) and (j != np.nan and k != np.nan):
            z = np.arange(ln[i], ln[i+1], 0.00001)
            fn = ne.evaluate(arc(eq.replace(lt, "z")))
            if NAmin(fn) == NAmax(fn) - 1:
                cur[-1][1][-1] = Nmin(fn)
                cur.append([ [ln[i]], [Nmax(fn)] ])
            elif NAmin(fn) == NAmax(fn) + 1:
                cur[-1][1][-1] = Nmax(fn)
                cur.append([ [ln[i]], [Nmin(fn)] ])
    if lt == "y":
        for i in range(len(cur)):
            cur[i] = cur[i][::-1]
    return cur

def labels(x, y, eq, maximum, minimum, zeros, yinter):
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


@commands.command(
    aliases = ["plot"],
    help = 'math',
    brief = 'Your personal graphing calculator',
    usage = ';]graph {?window} {eq1} {?ops} | {eq2} {?ops} | {...} {?ops}',
    description = '''\
WINDOW [NUMBERS] - Set XMIN, XMAX, YMIN, YMAX in that order
EQx    [TEXT   ] - The equation to graph
OPS    [TEXT   ] - Other arguments
> The style list too is long, use ';]graph help' for more
* Use '>=' and '<=' for 'at least' and 'at most' graphs [respectively]
* XY equations like `x^2+y^2` MUST have an equal sign
* Still use x and y for polar equations, where 'r' is y and 'x' is theta
'''
)
@commands.check(enbl)
async def graph(ctx, xmin: Opt[float] = None, xmax: Opt[float] = None,
                ymin: Opt[float] = None, ymax: Opt[float] = None, *, eqs = ""):
    if eqs.lower() == "help":
        return await ctx.send("""```md
#] GRAPH OPTIONS
]  --max
>  Find the maximum coordinates
]  --min
>  Find the minimum coordinates
]  --zero
>  Find the coordinates of where y=0
]  --yint
>  Find the coordinates of where x=0
]  --det  --detect  --asym  --asymptote
>  Find asymptotes and remove the vertical line there
** These are specific per equation, eg
   ;]graph tan(x) --asym | tan(x^2) --zero
           ^asym only      ^zero only``````md
#] PRIZM STYLES ---
]  ---zoom
>  Allows for smaller windows
]  ---smol
>  Allows for even smaller windows
]  ---step={digit}
>  Custom steps, 10000 max and 5 min, there is a check
>  Usage: ---step=69  ---step=420
#] TI STYLES ---
]  ---ti84cse ---ti84ce ---ti83ce ---ti83pce
]  ---ti84  ---ti83  ---ti82  ---ti81
]  ---ti73  ---ti73e
]  ---ti85  ---ti86  ---ti85se  ---ti86se
]  ---ti89  ---ti89t
]  ---ti80
]  ---tinspire ---tinspireii  ---nspirecas
]  ---tinspirecx  ---tinspirecxii  ---nspirecxcas
]  ---ti92  ---ti92p  ---ti92ii
#] CASIO STYLES ---
]  ---fx7000g  ---fx7000ga
]  ---fx2p  ---cfx9850gbp
]  ---fx9950cg
]  ---fx9750g  ---fx9750gii
]  ---fxcg50
]  ---fxcg500
#] HP STYLES ---
]  ---hp28c  ---hp28s
]  ---hp48g  ---hp48gii  ---hp48gp  ---hp48gx
]    ---hp48s  ---hp48sx  ---hp49g  ---hp49gp
]    ---hp50  ---hp50g  ---hp50p  ---hp50gp
]    ---hp39g  ---hp39gii  ---hp39gs  ---hp39gp
]    ---hp38g  ---hp38gii  ---hp38gs  ---hp39gp
]    ---hp40g  ---hp40gs
]  ---hpprime  ---prime
]  ---hp9p
]  ---hp42s
#] OTHER STYLES
]  ---numworks  ---numwork
]  ---pol  ---polar
** This changes how the graph looks entirely, ex
   ;]graph x | y | x^2 | y^2 ---style_name
```""")
    msg = await ctx.send('```md\n#] JUST A SEC\n> INITIALIZING```')


    ##/// INITIALIZE THINGS
    if xmin is not None and eqs == "":
        eqs = str(xmin)
        xmin = -10
    if xmin is None:
        xmin = -10
    if xmax is None:
        xmax = 10
    if ymin is None:
        ymin = xmin
    if ymax is None:
        ymax = xmax
    xmin, xmax = min(xmin, xmax), max(xmax, xmin)
    ymin, ymax = min(ymin, ymax), max(ymax, ymin)
    xr = abs(xmin) + abs(xmax)
    polar = False
    if re.search(r"---pol(ar)?", eqs):
        polar = True
        eqs = re.sub(r"---pol(ar)?", "", eqs)
        ymax = abs(xmin)
        ymin = 0
        ymin = 2 * 3.1415926535
        xmin = 0
    try:
        cstep = int(eqs.split('---step=')[1].split(' ')[0])
    except IndexError:
        cstep = 5
    cstep = min(10000, max(5, cstep)) #Limit the steps from 0 to 10000 inclusive
    for calc in calculators:
        if re.search(calc, eqs):
            if calc == r"---step=\d+":
                step = cstep
            else:
                step = xr / calculators[calc][0]
            eqs = re.sub(calc, "", eqs)
            styler = calculators[calc][1]
            break
    else:
        step = (abs(max(xmax, ymax)) + abs(min(xmin, ymin))) / 10000
        styler = 'prizm'
    eqA = []
    eqs = eqs.split(' | ')
    await msg.edit(content='```md\n#] JUST A SEC\n> PARSING EQUATIONS```')
    mini, maxi = min(xmin, ymin), max(xmax, ymax)
    array = np.array(np.arange(mini, maxi, step))
    for eq in eqs:
        mx, mn, zr, yi, dt, ae = 0, 0, 0, 0, 0, ""
        eq, mx = option("--max", eq)
        eq, mn = option("--min", eq)
        eq, zr = option("--zero", eq)
        eq, yi = option("--yint", eq)
        if eq.startswith("x=") and eq[2] not in "<>":
            eq = eq[2:]
            ae = "y"
        elif eq.startswith("y=") and eq[2] not in "<>":
            eq = eq[2:]
            ae = "x"
        for nam in ["det", "asym", "detect", "asymptote"]:
            eq, dt = option("--"+nam, eq, dt)
        eq = parse_eq(eq)
        if "x" in eq and "y" in eq or ">" in eq or "<" in eq:
            ae = "xy"
        if "x" in eq:
            ae = "x"
        elif "y" in eq:
            ae = "y"
        if "x" in eq and "y" in eq and not any(t in eq for t in "=><"):
            eq += "=0"
        eq, x, y = grab_window(eq, array, array, step, ymax, polar)
        eqA.append([nrc(eq), mx, mn, zr, yi, dt, x, y, ae])


    ##/// STYLIZE
    async with ctx.channel.typing():
        await msg.edit(content='```md\n#] JUST A SEC\n> STYLIZING```')
        pyplt.style.use(styler)
        a, kw = [], {}
        if polar:
            kw["projection"] = "polar"
            a = [111]
        ax = pyplt.subplot(*a, **kw)
        x, y = array, array
        if not polar:
            z = ne.evaluate('y-y' if max(xmax, ymax) == ymax else 'x-x')
            ax.set_ylim(top = ymax, bottom = ymin)
            ax.set_xlim(left = xmin, right = xmax)
            ax.plot(x, z, 'w', z, y, 'w', linewidth = 1) #Axis Lines
        else:
            ax.set_rmax(xmax / 2)
            ax.set_rticks([xmax / 2, xmax, 3 * xmax / 2, 2 * xmax])
        colors = eval(str(mpl.rcParams["axes.prop_cycle"])[16:-1])
        await msg.edit(content='```md\n#] JUST A SEC\n> GRAPHING```')
        func = f"{abs(xmax) + abs(xmin)} ** 2 - 4 * (x + {xmin} - {xmax})"
        circle1 = evl(f"-0.5 * sqrt({func}) + {ymax} - {ymin}", x, y)
        circle2 = evl(f"0.5 * sqrt({func}) + {ymax} - {ymin}", x, y)

        for eq, mx, mn, zeros, yinter, asymp, x, y, axis in eqA:
            color = random.choice(colors)
            params = [mx, mn, zeros, yinter]

            ##/// X and Y EQUATIONS
            if axis == "xy":
                x, y = sp.symbols('x y')
                itm = [z for z in ['>=','<=','=>', '=<', '>','<','='] if z in eq][0]
                half = eq.split(itm)
                try:
                    solved = sp.solvers.solve(f"({half[0]})-({half[1]})", x, y)
                except:
                    solved = [[f"({half[0]})-({half[1]})", "x"]] * 2
                x, y = array, array
                eq1 = evl(str(solved[0][0]), x, y).round(8)
                eq2 = evl(str(solved[1][0]), x, y).round(8)
                label = multilabels(x, y, eq, eq1, eq2, solved, *params)
                if str(solved[0][1]) == 'x':
                    st, a11, a12, a21, a22, z = "x", x, x, eq1, eq2, x
                else:
                    st, a11, a12, a21, a22, z = "y", eq1, eq2, y, y, y
                if not asymp:
                    ax = plotter(ax, a11, a21, color = color, polar = polar)
                    ax = plotter(ax, a12, a22, label, color, polar = polar)
                else:
                    for side in solved:
                        for line, sect in asymptote(z, eq1, str(side[0]), st):
                            ax = plotter(ax, line, sect, color = color, polar = polar)
                    ax = plotter(ax, line, sect, label, color, polar = polar)
                inequals = {
                    ">=": (lambda eq1, eq2: eq1 >= eq2),
                    "=>": (lambda eq1, eq2: eq1 >= eq2),
                    "<=": (lambda eq1, eq2: eq1 <= eq2),
                    "=<": (lambda eq1, eq2: eq1 <= eq2),
                    "<": (lambda eq1, eq2: eq1 > eq2),
                    ">": (lambda eq1, eq2: eq1 < eq2)
                }
                if '>' in itm or '<' in itm:
                    inequal = inequals[itm](eq1, eq2)
                    eqs = [eq1, eq2]
                    if not len(np.argwhere(inequal)):
                        eqs = [circle1, circle2]
                        if ">" in itm:
                            inequal = inequals[itm](eq1, circle1)
                        else:
                            inequal = inequals[itm](circle1, eq2)
                    ax = filler(ax, z, eqs[0], eqs[1], color, inequal)

            else:
                label, gr = labels(x, y, eq, *params)
                if axis == "x":
                    a1, a2, st = x, gr, "x"
                else:
                    a1, a2, st = gr, y, "y"
                if not asymp:
                     ax = plotter(ax, a1, a2, label, color, polar = polar)
                else:
                     for line, sect in asymptote(a1, a2, eq, st):
                         ax = plotter(ax, line, sect, color = color, polar = polar)
                     ax = plotter(ax, line, sect, label, color, polar = polar)

        await msg.edit(content='```md\n#] JUST A SEC\n> SAVING IMAGE```')
        ax.legend(loc = 3)
        plotimg = io.BytesIO()
        dpi = 600
        ax.get_figure().savefig(plotimg, format = 'png', dpi = dpi, pad_inches = 0.2)
        plotimg.seek(0)
        while len(plotimg.getvalue()) > 1024 ** 2 * 2: #No images greater than 2mb
            dpi -= 50
            plotimg = io.BytesIO()
            ax.get_figure().savefig(plotimg, format = 'png', dpi = dpi)
            plotimg.seek(0)
    await msg.edit(content='```md\n#] JUST A SEC\n> UPLOADING TO DISCORD```')
    await ctx.send("```md\n#] HERE IS YOUR GRAPH!```",
                   file = discord.File(plotimg, 'PRIZM_graph.png'))
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
