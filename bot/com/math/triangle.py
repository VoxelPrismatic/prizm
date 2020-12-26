#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from util import embedify, pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
import math
import re
from numexpr import evaluate as calc

global _inst
_inst = {}

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

async def request(ctx, num, m, chk):
    try:
        ms = await ctx.bot.wait_for("message", timeout = 15.0, check = chk)
    except asyncio.TimeoutError:
        await m.delete()
        await ctx.send("```diff\n-] TIMEOUT [15s]```", delete_after = 5.0)
    else:
        await m.delete()
        eq = ms.content
        try:
            await ms.delete()
        except:
            pass
        eq = eq.replace('^','**').lower().strip()
        oth = {
            r"(\d)\(": r"\1*(",
            r"\)(\d)": r")*\1",
            r"(\d+)i": r"\1j",
            r"([\*\+\-\^\/ ])i ?": r"\1 1j",
            r"\)i": r")*1j",
            r"i\(": r"1j*(",
            r"pi(\d)": r"3.141592653*\1",
            r"(\d)pi": r"\1*3.141592653",
            r"([\*\+\-\^\/ ])pi": r"\1 3.1415926535",
            r"pi([\*\+\-\^\/ ])": r"3.1415926535 \1",
            r"\)pi": r")*3.1415926535",
            r"pi\(": r"3.1415926535*(",
            r"e(\d)": r"2.718281828*\1",
            r"(\d)e": r"\1*2.718281828",
            r"([\*\+\-\^\/ ])e": r"\1 2.718281828",
            r"e([\*\+\-\^\/ ])": r"2.718281828 \1",
            r"\)e": r")*2.718281828",
            r"e\(": r"2.718281828*(",
        }
        fns = {
            r"(\d+)root\((.*)\)": r"(\2)^(1/\1)",
            r"logbase(\d+)\((.*)\)": r"log(\2, \1)",
            r"((tan|cos|sin|cot|csc|sec)h?)\*\*-1\((.*)\)": "a\1(\2)",
            r"cot\((.*)\)": r"(1/tan(\1))",
            r"csc\((.*)\)": r"(1/sin(\1))",
            r"sec\((.*)\)": r"(1/cos(\1))",
            r"coth\((.*)\)": r"(1/tanh(\1))",
            r"csch\((.*)\)": r"(1/sinh(\1))",
            r"sech\((.*)\)": r"(1/cosh(\1))",
            r"acot\((.*)\)": r"atan(1/(\1))",
            r"acsc\((.*)\)": r"asin(1/(\1))",
            r"asec\((.*)\)": r"acos(1/(\1))",
            r"acoth\((.*)\)": r"atanh(1/(\1))",
            r"acsch\((.*)\)": r"asinh(1/(\1))",
            r"asech\((.*)\)": r"acosh(1/(\1))"
        }
        for r in fns:
            eq = re.sub(r, fns[r], eq)
        for r in oth:
            eq = re.sub(r, oth[r], eq)
        try:
            num = calc(eq)
        except ValueError:
            await ctx.send("```diff\n-] BAD VALUE [numbers only]```", delete_after = 5.0)
        except SyntaxError:
            await ctx.send("```diff\n-] UNREADABLE [numbers only]```", delete_after = 5.0)
    return num
def tri(a, b, c, X, Y, Z):
    return f"""\
  A          A = {a}
  |\         B = {b}
Y |  \ Z     C = {c}
  |    \     X = {X:.3f}
  C-----B    Y = {Y:.3f}
     X       Z = {Z:.3f}"""
def angle_sin(s, a1, a2):
    return s * (math.sin(a1) / math.sin(a2))
def side_cos(s1, a, s2):
    return (s1**2 + s2**2 -2*s1*s2*math.cos(a))**0.5
def angle_cos(s1, s2, s3):
    return math.acos(abs(s3**2-s2**2-s1**2)/(2*s1*s2))
def angles_sin(s1, a, s2):
    ans = math.asin((math.sin(a)/s2)*s1)
    return (ans, ans-a), (180-ans-a, 180-ans+a)
def ssa_sin(s1, a, s2, hao2, n0, n1, n2, n3, n4, u):
    a1, a2 = angles_sin(s1, a, s2)
    hao2 += f"{n0} = arcsin(sin({n2})/{n3})*{n4})\n"
    hao2 += f"{n1} = {u} - {n1} - {n2}\n"
    hao2 += f"{n0}2 = {n0} - {n2}\n"
    hao2 += f"{n1}2 = {u} - {n0}\n"
    if a1[0] <= 0 or a2[0] <= 0:
        a1, a2, = a1[1], a2[1]
    elif a1[1] <= 0 or a2[1] <= 0:
        a1, a2, = a1[0], a2[0]
    else:
        if u == "2pi":
            a1 = f"{a1[0]/pi*12:.2f}/12 pi or {a1[1]/pi*12:.2f}/12 pi"
            a2 = f"{a2[0]/pi*12:.2f}/12 pi or {a2[1]/pi*12:.2f}/12 pi"
        else:
            a = f"{a1[0]*180/pi:.2f} or {a1[1]*180/pi:.2f}"
            c = f"{a2[0]*180/pi:.2f} or {a2[1]*180/pi:.2f}"
    return a1, a2, hao2

@commands.command(
    aliases = ["tri"],
    help = 'math',
    brief = 'Solves triangles',
    usage = ';]triangle',
    description = '[NO INPUT FOR THIS COMMAND]'
)
@commands.check(enbl)
async def triangle(ctx):
    a = 0
    b = 0
    c = 0
    X = 0
    Y = 0
    Z = 0
    rad = True
    hao2 = ""
    msg = await ctx.send(
        embed = embedify.emb(
            title = "TRIANGLES ;]",
            desc = f"""```md
#] TRIANGLES

{tri(a, b, c, X, Y, Z)}

#] CLICK \u2705 AFTER ENTERING 3 VALUES
>  One value must be a side
#] ANY '0' VALUE IS CONSIDERED EMPTY
]] RADIANS - CLICK \U0001f501 TO CHANGE
```""",
            foot = "PRIZM ;] // REACT TO EDIT"
        )
    )
    _inst[msg.id] = {"var": [a, b, c, X, Y, Z], "msg": msg, "rad": rad, "ctx": ctx}
    for r in "ABCXYZ":
        await msg.add_reaction(eval('"\\N{REGIONAL INDICATOR SYMBOL LETTER '+r+'}"'))
    await msg.add_reaction("\u2705")
    await msg.add_reaction(f"\U0001f501")
    def check(rct, usr):
        return usr == ctx.author and rct.emoji in [
            "\U0001f1e6", "\U0001f1e7", "\U0001f1e8",
            "\U0001f1fd", "\U0001f1fe", "\U0001f1ff",
            "\U0001f501", "\u2705"
        ]
    def chk(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    while True:
        try:
            rct, usr = await ctx.bot.wait_for("reaction_add", timeout = 60.0, check = check)
        except asyncio.TimeoutError:
            del _inst[msg.id]
            delet = []
            for tmsg in list(_inst)[:]:
                imsg=_inst[tmsg]["msg"]
                if imsg.edited_at is None:
                    tm = imsg.created_at.timestamp()
                else:
                    tm = imsg.edited_at.timestamp()
                if float(datetime.datetime.utcnow().timestamp()-tm) > 59:
                    delet.append(tmsg)
                    await msg.edit(embed=embedify.emb(title = "TRIANGLES ;]", desc = f"""```md
#] TRIANGLES

{tri(a, b, c, X, Y, Z)}
```""", foot = "PRIZM ;] // TIMEOUT"))
                    await imsg.clear_reactions()
            for m in delet:
                del _inst[m]
        else:
            e = rct.emoji
            ctx = _inst[rct.message.id]["ctx"]
            a, b, c, X, Y, Z = _inst[rct.message.id]["var"]
            rad = _inst[rct.message.id]["rad"]
            msg = _inst[rct.message.id]["msg"]
            if e == "\U0001f1e6":
                m = await ctx.send("```md\n#] ENTER VALUE FOR A [ANGLE]```")
                a = await request(ctx, a, m, chk)
            elif e == "\U0001f1e7":
                m = await ctx.send("```md\n#] ENTER VALUE FOR B [ANGLE]```")
                b = await request(ctx, b, m, chk)
            elif e == "\U0001f1e8":
                m = await ctx.send("```md\n#] ENTER VALUE FOR C [ANGLE]```")
                c = await request(ctx, c, m, chk)
            elif e == "\U0001f1fd":
                m = await ctx.send("```md\n#] ENTER VALUE FOR X [SIDE]```")
                X = await request(ctx, X, m, chk)
            elif e == "\U0001f1fe":
                m = await ctx.send("```md\n#] ENTER VALUE FOR Y [SIDE]```")
                Y = await request(ctx, Y, m, chk)
            elif e == "\U0001f1ff":
                m = await ctx.send("```md\n#] ENTER VALUE FOR Z [SIDE]```")
                Z = await request(ctx, Z, m, chk)
            elif e == "\U0001f501":
                rad = not rad
            elif e == "\u2705":
                try:
                    await msg.clear_reactions()
                except:
                    pass
                pi = 3.1415926535
                u = "2pi"
                if not rad:
                    a = a/180*pi
                    b = b/180*pi
                    c = c/180*pi
                    u = "180"
                while a > 2*pi or a < 0:
                    a += (-1 if a > 2*pi else 1) * 2*pi
                while b > 2*pi or b < 0:
                    b += (-1 if b > 2*pi else 1) * 2*pi
                while c > 2*pi or c < 0:
                    c += (-1 if c > 2*pi else 1) * 2*pi
                if a + b + c > pi:
                    del _inst[msg.id]
                    return await ctx.send("```-] INVALID ANGLES```")
                elif a < 0 or b < 0 or c < 0 or X < 0 or Y < 0 or Z < 0:
                    del _inst[msg.id]
                    return await ctx.send("```-] NEGATIVE VALUES NOT ALLOWED```")
                elif not(X or Y or Z):
                    await ctx.send("```-] NO SIDES GIVEN, SIDE X = 1```")
                    X = 1
                elif X and Y and Z and (a or b or c):
                    del _inst[msg.id]
                    return await ctx.send("```-] TOO MANY VALUES GIVEN```")


                if a and b and c:
                    pass #Dont continue on
                elif a and b and not c:
                    c = pi - a - b
                    hao2 += f"C = {u} - A - B\n"
                elif a and c and not b:
                    b = pi - a - c
                    hao2 += f"B = {u} - A - C\n"
                elif b and c and not a:
                    a = pi - b - c
                    hao2 += f"A = {u} - B - C\n"
                #Law of cosines

                if X and Y and c and not Z:
                    Z = side_cos(X, c, Y)
                    hao2 += "Z = \u221a(X\xb2 + Y\xb2 - 2 * X * Y * cos(C))\n"
                if Z and Y and a and not X:
                    X = side_cos(Z, a, Y)
                    hao2 += "X = \u221a(Z\xb2 + Y\xb2 - 2 * Z * Y * cos(A))\n"
                if X and Z and b and not Y:
                    Y = side_cos(X, b, Z)
                    hao2 += "Y = \u221a(X\xb2 + Z\xb2 - 2 * X * Z * cos(B))\n"
                if X and Y and Z:
                    if a and b and c:
                        pass #Dont continue on
                    elif a and b and not c:
                        c = pi - a - b
                        hao2 += f"C = {u} - A - B\n"
                    elif a and c and not b:
                        b = pi - a - c
                        hao2 += f"B = {u} - A - C\n"
                    elif b and c and not a:
                        a = pi - b - c
                        hao2 += f"A = {u} - B - C\n"
                    else:
                        if not c:
                            c = math.acos((X**2 + Y**2 - Z**2)/(2 * X * Y))
                            hao2 += "C = arccos((X\xb2 + Y\xb2 - Z\xb2)/(2 * X * Y))\n"
                        if not a:
                            a = math.acos((Y**2 + Z**2 - X**2)/(2 * Z * Y))
                            hao2 += "A = arccos((Y\xb2 + Z\xb2 - X\xb2)/(2 * Y * Z))\n"
                        if not b:
                            b = math.acos((Z**2 + X**2 - Y**2)/(2 * X * Z))
                            hao2 += "B = arccos((Z\xb2 + X\xb2 - Y\xb2)/(2 * X * Z))\n"

                #Law of sines - Angle
                if not(X and Y and Z):
                    if a and b and Y and not X:
                        X = angle_sin(Y, a, b)
                        hao2 += "X = Y*(sin(A)/sin(B))\n"
                    if b and a and X and not Y:
                        Y = angle_sin(X, b, a)
                        hao2 += "Y = X*(sin(B)/sin(A))\n"
                    if c and b and Y and not Z:
                        Z = angle_sin(Y, c, b)
                        hao2 += "Z = Y*(sin(C)/sin(B))\n"
                    if a and c and Z and not X:
                        X = angle_sin(Z, a, c)
                        hao2 += "X = Z*(sin(A)/sin(C))\n"
                    if b and c and Z and not Y:
                        Y = angle_sin(Z, b, c)
                        hao2 += "Y = Z*(sin(B)/sin(C))\n"
                    if c and a and X and not Z:
                        Z = angle_sin(X, c, a)
                        hao2 += "Z = X*(sin(C)/sin(A))\n"

                    if a and b and c:
                        pass #Dont continue on
                    elif a and b and not c:
                        c = pi - a - b
                        hao2 += f"C = {u} - A - B\n"
                    elif a and c and not b:
                        b = pi - a - c
                        hao2 += f"B = {u} - A - C\n"
                    elif b and c and not a:
                        a = pi - b - c
                        hao2 += f"A = {u} - B - C\n"
                    else:
                        if Y and b and Z and not a and not c:
                            a, c, hao2 = ssa_sin(Y, b, Z, hao2, "A", "C", "B", "Y", "Z", u)
                        if Y and b and X and not a and not c:
                            a, c, hao2 = ssa_sin(Y, b, X, hao2, "A", "C", "B", "Y", "X", u)
                        if X and a and Z and not b and not c:
                            b, c, hao2 = ssa_sin(X, a, Z, hao2, "B", "C", "A", "X", "Z", u)
                        if X and a and Y and not b and not c:
                            b, c, hao2 = ssa_sin(X, a, Y, hao2, "B", "C", "A", "X", "Y", u)
                        if Z and c and X and not a and not b:
                            a, b, hao2 = ssa_sin(Z, c, X, hao2, "A", "B", "C", "Z", "X", u)
                        if Z and c and Y and not a and not b:
                            a, b, hao2 = ssa_sin(Z, c, X, hao2, "A", "B", "C", "Z", "Y", u)
                if not rad:
                    try:
                        a = round(a*180/pi, 2)
                    except:
                        pass
                    try:
                        b = round(b*180/pi, 2)
                    except:
                        pass
                    try:
                        c = round(c*180/pi, 2)
                    except:
                       pass
                else:
                    try:
                        a = f"{a/pi*12:.2f}/12 pi"
                    except:
                        pass
                    try:
                        b = f"{b/pi*12:.2f}/12 pi"
                    except:
                        pass
                    try:
                        c = f"{c/pi*12:.2f}/12 pi"
                    except:
                       pass
                try:
                    await msg.clear_reactions()
                except:
                    pass
                del _inst[msg.id]
                return await msg.edit(embed=embedify.emb(title = "TRIANGLES ;]", desc = f"""```md
#] TRIANGLES

{tri(a, b, c, X, Y, Z)}

]] {"RADIANS" if rad else "DEGREES"}

#] HOW TO SOLVE
>  For this specific triangle
{hao2}
```""", foot = "PRIZM ;] // COMPLETED"))
            try:
                await msg.remove_reaction(rct, usr)
                foot = "REACT TO EDIT"
            except:
                foot = "RE-REACT TO EDIT"
            _inst[msg.id] = {"var": [a, b, c, X, Y, Z], "msg": msg, "rad": rad, "ctx": ctx}
            await msg.edit(embed=embedify.emb(title = "TRIANGLES ;]", desc = f"""```md
#] TRIANGLES

{tri(a, b, c, X, Y, Z)}

#] CLICK \u2705 AFTER ENTERING 3 VALUES
>  One value must be a side
#] ANY '0' VALUE IS CONSIDERED EMPTY
]] {"RADIANS" if rad else "DEGREES"} - CLICK \U0001f501 TO CHANGE
```""", foot = "PRIZM ;] // "+foot))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(triangle)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('triangle')
    print('GOOD')
