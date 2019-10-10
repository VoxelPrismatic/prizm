#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import math, cmath, numpy
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help='math',
                  brief = 'Reverse Polish Notation [1 1 +]',
                  usage = ';]rpn {eq}',
                  description = 'EQ [STR] - The RPN equation')
@commands.check(enbl)
async def rpn(ctx, *, expression):
    msg = await ctx.send('```md\n#] CALCULATING```')
    async with ctx.channel.typing():
        ops = {
        "+": (lambda a, b: a + b), 
        "-": (lambda a, b: a - b),
        "*": (lambda a, b: a * b), 
        "/": (lambda a, b: a / b),
        "^": (lambda a, b: a ** b), 
        "**": (lambda a, b: a ** b),
        '%': (lambda a, b: a % b), 
        '&': (lambda a, b: a & b),
        '<<': (lambda a, b: int(a) << int(b)), 
        '<': (lambda a, b: a < b),
        '>>': (lambda a, b: int(a) >> int(b)), 
        '>': (lambda a, b: int(a > b)),
        '<=': (lambda a, b: int(a <= b)), 
        '>=': (lambda a, b: int(a >= b)),
        '=<': (lambda a, b: int(a <= b)), 
        '=>': (lambda a, b: int(a >= b)),
        '!=': (lambda a, b: int(a != b)),
        '=!': (lambda a, b: int(a != b)),
        '==': (lambda a, b: int(a == b)),
        '<>': (lambda a, b: int(a != b)),
        '&&': (lambda a, b: int(a and b)),
        '||': (lambda a, b: int(a or b)),
        'and': (lambda a, b: int(a and b)),
        'or': (lambda a, b: int(a or b)),
        'gcd': (lambda a, b: math.gcd(a,b)),
        'lcm': (lambda a, b: math.lcm(a,b)),
        'root': (lambda a, b: a ** (b**-1)),
        'log': (lambda a, b: math.log(a,b)),
        'rect': (lambda a, b: cmath.rect(a,b))
        }

        spc = {
        "pi": numpy.pi,
        "e": math.e,
        "tau": math.tau,
        'inf': math.inf,
        'nan': math.nan,
        'infj': cmath.infj,
        'nanj': cmath.nanj,
        'c': 299792458,               # SPEED OF LIGHT
        'G': 6.67408e-11,    # GRAV CONSTANT
        'h': 1.05457148e-34, # PLANCK CONSTANT
        'mPl': 1.2209e22,    # PLANCK MASS ENERGY
        'B': 1836.15**-1,  # RATIO ELECTRON TO PROTON MASS
        'me': 0.51,    # MASS OF ELECTRON
        'mp': 983.3,   # MASS OF PROTON
        'mn': 939.6,   # MASS OF NEUTRON
        'mu': 2.4,     # MASS OF UP QUARK
        'md': 4.8,     # MASS OF DOWN QUARK
        'ms': 104,     # MASS OF STRANGE QUARK
        'aG': 5.9e-39, # GRAV COUPLING CONSTANT
        'a1': 1/98.4,           # HYPER COUPLING CONSTANT
        'a2': 1/29.6,           # WEAK COUPLING CONSTANT
        'a3': 0.1187,           # STRONG COUPLING CONSTANT
        'as': 0.1187,
        }

        mat = {
        'sin': (lambda a: math.sin(a)),
        'cos': (lambda a: math.cos(a)),
        'tan': (lambda a: math.tan(a)),
        'exp': (lambda a: math.exp(a)),
        'floor': (lambda a: math.floor(a)),
        'ceil': (lambda a: math.ceil(a)),
        'abs': (lambda a: abs(a)),
        '!': (lambda a: math.factorial(a)),
        '?': (lambda a: sum([x for x in range(1,int(a)+1)])),
        'fact': (lambda a: math.factorial(a)),
        'deg': (lambda a: math.degrees(a)),
        'rad': (lambda a: math.radians(a)),
        '°': (lambda a: math.radians(a)),
        'd': (lambda a: math.radians(a)),
        'acosh': (lambda a: math.acosh(a)),
        'asinh': (lambda a: math.asinh(a)),
        'atanh': (lambda a: math.atanh(a)),
        'cosh': (lambda a: math.cosh(a)),
        'sinh': (lambda a: math.sinh(a)),
        'tanh': (lambda a: math.tanh(a)),
        'arccos': (lambda a: numpy.arccos(a)),
        'arcsin': (lambda a: numpy.arcsin(a)),
        'arctan': (lambda a: numpy.arctan(a)),
        'arccosh': (lambda a: numpy.arccosh(a)),
        'arcsinh': (lambda a: numpy.arcsinh(a)),
        'arctanh': (lambda a: numpy.arctanh(a)),
        'phase': (lambda a: cmath.phase(a)),
        'acos': (lambda a: math.acos(a)),
        'asin': (lambda a: math.asin(a)),
        'atan': (lambda a: math.atan(a)),
        'real': (lambda a: a.real),
        'imag': (lambda a: a.imag*1j),
        'sqrt': (lambda a: a**.5),
        'log10': lambda a: math.log10(a),
        'fpart': (lambda a: int(str(a).split('.')[1])),
        'ipart': (lambda a: int(str(a).split('.')[0]))
        }

        tokens = expression.split()
        stack = []
        try:
            for token in tokens:
                if token in spc:
                    stack.append(spc[token])
                elif token in mat:
                    stack.append(mat[token](stack.pop()))
                elif token in ops:
                    arg2 = stack.pop()
                    arg1 = stack.pop()
                    try: stack.append(ops[token](arg1, arg2))
                    except ZeroDivisionError:
                        stack.append(math.nan)
                else: stack.append(float(token))
                if stack[-1] > 20**100:
                    return await ctx.send('```diff\n-] TOO LARGE [20^100 MAX]```')
        except IndexError:
            return await ctx.send('```diff\n-] ERROR - POP FROM EMPTY STACK\n=] TOO MANY OPERATORS?```')
        except KeyError:
            return await ctx.send(f'```diff\n-] ERROR - TOKEN UNRECOGNIZED\n=] TOKEN {token} IS UNRECOGNIZED```')
        else:
            if len(stack) != 1:
                return await ctx.send('```diff\n-] ERROR - TOO MANY VALUES\n=] TOO LITTLE OPERATORS?```')
    await ctx.send(content=f'```md\n#] {round(stack.pop(),8)}```')
    await msg.delete()

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rpn)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rpn')
    print('GOOD')
