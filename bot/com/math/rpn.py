#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import math, cmath, numpy, decimal
from decimal import Decimal as dec
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from decimal import *

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

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
async def rpn(ctx, *, expression):
    msg = await ctx.send('`CALCULATING`')
    async with ctx.channel.typing():
        ops = {
        "+": (lambda a, b: a + b),
        "-": (lambda a, b: a - b),
        "*": (lambda a, b: a * b),
        "/": (lambda a, b: a / b),
        "^": (lambda a, b: a ** b),
        '**': (lambda a, b: a ** b),
        '%': (lambda a, b: a % b),
        '&': (lambda a, b: a & b),
        '<<': (lambda a, b: int(a) << int(b)),
        '>>': (lambda a, b: int(a) >> int(b)),
        '<': (lambda a, b: int(bool(a < b))),
        '>': (lambda a, b: int(bool(a > b))),
        '<=': (lambda a, b: int(bool(a <= b))),
        '>=': (lambda a, b: int(bool(a >= b))),
        '!=': (lambda a, b: int(bool(a != b))),
        '==': (lambda a, b: int(bool(a == b))),
        '<>': (lambda a, b: int(bool(a != b))),
        '&&': (lambda a, b: int(bool(a and b))),
        '||': (lambda a, b: int(bool(a or b))),
        'and': (lambda a, b: int(bool(a and b))),
        'or': (lambda a, b: int(bool(a or b))),
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
        'G': dec('6.67408e-11'),    # GRAV CONSTANT
        'h': dec('1.05457148e-34'), # PLANCK CONSTANT
        'mPl': dec('1.2209e22'),    # PLANCK MASS ENERGY
        'B': dec('1836.15')**-1,  # RATIO ELECTRON TO PROTON MASS
        'me': dec('0.51'),    # MASS OF ELECTRON
        'mp': dec('983.3'),   # MASS OF PROTON
        'mn': dec('939.6'),   # MASS OF NEUTRON
        'mu': dec('2.4'),     # MASS OF UP QUARK
        'md': dec('4.8'),     # MASS OF DOWN QUARK
        'ms': dec('104'),     # MASS OF STRANGE QUARK
        'aG': dec('5.9e-39'), # GRAV COUPLING CONSTANT
        'a1': 1/dec('98.4'),           # HYPER COUPLING CONSTANT
        'a2': 1/dec('29.6'),           # WEAK COUPLING CONSTANT
        'a3': dec('0.1187'),           # STRONG COUPLING CONSTANT
        'as': dec('0.1187'),
        }
        
        mat = {
        'sin': (lambda a: math.sin(math.radians(a))),
        'cos': (lambda a: math.cos(math.radians(a))),
        'tan': (lambda a: math.tan(math.radians(a))),
        'rsin': (lambda a: math.sin(a)),
        'rcos': (lambda a: math.cos(a)),
        'rtan': (lambda a: math.tan(a)),
        'exp': (lambda a: math.exp(a)),
        'floor': (lambda a: math.floor(a)),
        'ceil': (lambda a: math.ceil(a)),
        'abs': (lambda a: abs(a)),
        '!': (lambda a: math.factorial(a)),
        '?': (lambda a: sum([x for x in range(1,int(a)+1)])),
        'fact': (lambda a: math.factorial(a)),
        'deg': (lambda a: math.degrees(a)),
        'rad': (lambda a: math.radians(a)),
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
                if token in spc: stack.append(spc[token])
                elif token in mat: stack.append(mat[token](stack.pop()))
                elif token in ops:
                    arg2 = stack.pop(); arg1 = stack.pop()
                    try: stack.append(ops[token](arg1, arg2))
                    except ZeroDivisionError: stack.append(math.nan)
                else: stack.append(dec(token))
                if stack[-1] > 20**100: return await ctx.send('```diff\n-] TOO LARGE [20^100 MAX]```')
        except IndexError: return await ctx.send('```diff\n-] ERROR - POP FROM EMPTY STACK\n=] TOO MANY OPERATORS?```')
        except KeyError: return await ctx.send(f'```diff\n-] ERROR - TOKEN UNRECOGNIZED\n=] TOKEN {token} IS UNRECOGNIZED```')
        except decimal.ConversionSyntax: return await ctx.send(f'```diff\n-] ERROR - TOKEN UNRECOGNIZED\n=] TOKEN {token} IS UNRECOGNIZED```')
        else:
            if len(stack) != 1: return await ctx.send('```diff\n-] ERROR - TOO MANY VALUES\n=] TOO LITTLE OPERATORS?```')
    await ctx.send(content='`'+str(stack.pop())+'`')
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
