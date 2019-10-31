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

@commands.command(aliases = [],
                  help = 'oth',
                  brief = 'Shows unicode info on {char}',
                  usage = ';]char {chars}',
                  description = '''\
CHARS [TEXT] - The characters you want data on
> If you want info on one character, you can see how to write it in various programming languages
''')
@commands.check(enbl)
async def char(ctx, *, txt):
    ls = []
    for t in txt:
        if t not in ls: ls.append(t)
    cata = [category(ch) for ch in ls]
    extra = ""
    table = '```'+'\n'.join([f'{ch} - U+{ord(ch):04x} [{category(ch)} // {name(ch)}]' for ch in ls])+'```'
    if len(ls) == 1:
        ch = ls[0]
        py = f"u{ord(ch):04x}" if len(f"{ord(ch):04x}") == 4 else f"U{ord(ch):08x}"
        tmp = f"{ord(ch):02x}"
        if len(tmp) != 2: tmp = str(ch.encode('utf-8'))[2:-1].replace('\\x','')
        if len(tmp)%2: tmp = "0"+tmp #Always an even length
        htm = "%".join(tmp[x]+tmp[x+1] for x in range(0,len(tmp),2))
        js = "\\u{"+f"{ord(ch):x}"+"}"
        jv = f"(char){ord(ch)}"
        extra = f'''```
   PY ] \\{py if len(tmp) != 2 else "x"+tmp}
  URL ] %{htm}
 HTML ] &#x{ord(ch):x};
 JAVA ] {jv}
   JS ] {js}
SWIFT ] {js}
 RUBY ] {js}
   C# ] {jv}
  C++ ] \\{py}
    C ] \\{py}```'''
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
    await ctx.send(table+key+'```'+extra)

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
