#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import io
import time
import discord                    #python3.7 -m pip install -U discord.py
import logging
import textwrap
import sysconfig
import traceback
import contextlib
from discord.ext import commands
from contextlib import redirect_stdout
from util.pages import PageThis
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def exe(ctx, *, code: str):
    if 'while' in code or 'input(' in code:
        ms = await ctx.send('```diff\n-] THIS CODE CONTAINS "WHILE" OR "INPUT("\n] Continue?```')
        await ms.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER Y}')
        await ms.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER N}')
        def ch(v,n): return n == ctx.author
        try: v,n = await ctx.bot.wait_for('reaction_add',check=ch,timeout=30)
        except: return await ms.delete()
        if str(v.emoji) != '\N{REGIONAL INDICATOR SYMBOL LETTER Y}': return await ms.delete()
    st1 = time.monotonic()
    try:
        code = code.strip('\n')
        sub = {
            'ctx': ctx,
            'me': ctx.me,
            'bot': ctx.bot,
            'cog': ctx.cog,
            'args': ctx.args,
            'guild': ctx.guild,
            'kwargs': ctx.kwargs,
            'author': ctx.author,
            'channel': ctx.channel,
            'message': ctx.message,
        }
        sub.update(globals())
        out = io.StringIO()
        rs = exec("async def fn():\n"+textwrap.indent(code, '    '), sub)
        fn = sub['fn']
        st2 = time.monotonic()
        with redirect_stdout(out): rtn = str(await fn())
        ttl = time.monotonic() - st2
        vl = str(out.getvalue())
        if rtn == None: rtn = 'None'
        head = f'''```md
#] *.EXE 0.0
] PYTHON V // {str(sysconfig.get_python_version())}
> EXE TIME // {str(1000*ttl)[:10]}ms
> TTL TIME // {str(1000*(time.monotonic()-st1))[:10]}ms
'''
        foot = f'''] ======== // ========
> RETURNED // {rtn}
>  PRINTED // {"None" if vl == "" else f"{vl[:-1]}"}
```'''
        print(head+foot)
        if len(vl)+len(rtn) > 1000:
            r = rtn.split('\n'); v = vl.split('\n')
            rr = []; vv = []; st = ""; lit = [head[6:]]
            for x in r: rr.extend([x[i:i+1000] for i in range(0, len(x), 1000)])
            for x in v: vv.extend([x[i:i+1000] for i in range(0, len(x), 1000)])
            for x in rr:
                if len(st) >= 500:lit.append('PRINTED // '+st);st=""
                else: st=f"{st}{x}\n"
            if st != "": lit.append('RETURNED // '+st)
            for x in vv:
                if len(st) >= 500:lit.append('PRINTED // '+st);st=""
                else: st=f"{st}{x}\n"
            if st != "": lit.append('RETURNED // '+st)
            return await PageThis(ctx,lit,'it overflowed UwU')
        else: await ctx.send(head+foot)
    except Exception as exc:
        await ctx.send(f'''```diff
-] ERROR
-] TYPE // {type(exc).__name__}
> {str(exc)}
{traceback.format_exc().replace('`','` ')}```''')


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(exe)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('exe')
    print('GOOD')