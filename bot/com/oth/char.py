#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
from discord.ext import commands
import unicodedata as unidata
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from html.entities import html5
import re
import io

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
    html5chars = {html5[key]: key for key in html5}
    html5codes = {key.upper(): html5[key] for key in html5}
    try:
        if re.search(r"^\\u[0-9A-Fa-f]{4}$", txt):
            txt = chr(int(txt[2:], 16))
        elif re.search(r"^\\u\{[0-9A-Fa-f]+\}$", txt):
            txt = chr(int(txt[3:-1], 16))
        elif re.search(r"^\&\#x[0-9A-Fa-f]{4}\;$", txt):
            txt = chr(int(txt[3:-1], 16))
        elif re.search(r"^\\U[0-9A-Fa-f]{8}$", txt):
            txt = chr(int(txt[2:], 16))
        elif re.search(r"^\\x[0-9A-Fa-f]{2}$", txt):
            txt = chr(int(txt[2:], 16))
        elif re.search(r"^(\%[0-9A-Fa-f]{2})+$", txt):
            txt = chr(int(txt.replace("%", ""), 16))
        elif re.search(r"^\\[nN]\{[\w\d ]+\}$", txt):
            txt = unidata.lookup(txt[3:-1].upper())
        elif re.search(r"^\&[\w\d]+;$", txt):
            txt = html5codes[txt[1:-1].upper()]
    except Exception as ex:
        return await ctx.send(f"```diff\n-] INVALID CHAR\n=] {str(ex)}```")
       
    ls = []
    for t in txt:
        if t not in ls: ls.append(t)
    cata = []
    extra = ""
    table = "```"
    more = ""
    for ch in ls:
        code = ord(ch)
        table += "\n" + f"{ch} - U+{code:04x} [{unidata.name(ch)} - {unidata.category(ch)}]"
        cata.append(unidata.category(ch))
        py = f"u{code:04x}"
        if len(f"{code:04x}") > 4:
            py = f"U{code:08x}"
        byte = f"x{code:02x}"
        if len(byte) > 3:
            byte = py
        hx = f"{code:x}"
        if len(hx) % 2:
            hx = "0" + hx
        url = ""
        for n in range(0, len(hx), 2):
            url += "%" + hx[n] + hx[n + 1]
        try:
            html = f"or &{html5chars[ch].strip(';')};"
        except KeyError:
            html = ""
        js = "\\u{"+f"{code:x}"+"}"
        jv = f"(char){code}"
        reg = f'or /\\{py}/'
        more += f'''[ {ch} ] -----
U+{code:04x} [{unidata.name(ch)} - {unidata.category(ch)}]
    PY ] \\{byte} or \\N{'{'+unidata.name(ch)+'}'}
   URL ] {url}
  HTML ] &#x{code:x}; {html}
  JAVA ] {jv}
    JS ] {js}
 SWIFT ] {js}
  RUBY ] {js}
    C# ] {jv}
   C++ ] \\{py}
     C ] \\{py}
 REGEX ] /\\{js}/u {reg if py[0] == "u" else ''}
KOTLIN ] \\{py if py[0] == "u" else "NOPE."}
'''
    table += "```"
    key = '```'
    code = {
        'Cc': 'Control',
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
        'Zs': 'Space Seperator'
    }
    extra = ""
    if len(txt) == 1:
        extra = '```' + more + '```'
    for x in list(code):
        if x in cata: 
            key += f'[{x}] - {code[x].upper()}\n'
    await ctx.send(
        table + key + '```' + extra, 
        file = discord.File(io.BytesIO(more.encode()), "chars.txt")
    )
        

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
