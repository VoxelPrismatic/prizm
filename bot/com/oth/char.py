#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
from discord.ext import commands
from unicodedata import *
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help='oth',
                  brief = 'Shows unicode info on {char}',
                  usage = ';]char {chars}',
                  description = 'CHARS [STR] - The characters you want data on')
@commands.check(enbl)
async def char(ctx, *, txt):
    ls = []
    for t in txt:
        if t not in ls: ls.append(t)
    cata = [category(ch) for ch in ls]
    table = '```'+'\n'.join([f'{ch} - {f"u_{ord(ch):04x}" if len(f"{ord(ch):04x}") == 4 else f"U_{ord(ch):08x}"} [{category(ch)} // {name(ch)}]' for ch in ls])+'```'
    key = '```'
    code = {'Cc': 'Control',
            'Cf': 'Format',
            'Co': 'Private Use',
            'Cs': 'Surrogate',
            'Ll': 'Lowercase Letter',
            'Lm': 'Modifier Letter',
            'Lo': 'Other Letter',
            'Lt': 'Titlecase Letter',
            'Lu': 'Uppercase Letter',
            'Mc': 'Spacing Mark',
            'Me': 'Enclosing Mark',
            'Mn': 'Nonspacing Mark',
            'Nd': 'Decimal Number',
            'Nl': 'Letter Number',
            'No': 'Other Number',
            'Pc': 'Connector Punctuation',
            'Pd': 'Dash Punctuation',
            'Pe': 'Close Punctuation',
            'Pf': 'Final Punctuation',
            'Pi': 'Initial Punctuation',
            'Po': 'Other Punctuation',
            'Ps': 'Open Punctuation',
            'Sc': 'Currency Symbol',
            'Sk': 'Modifier Symbol',
            'Sm': 'Math Symbol',
            'So': 'Other Symbol',
            'Zl': 'Line Separator',
            'Zp': 'Paragraph Separator',
            'Zs': 'Space Seperator'}
    for x in list(code):
        if x in cata: key = key+f'[{x}] - {code[x].upper()}\n'
    await ctx.send(table+key+'```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(char)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('char')
    print('GOOD')
