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
        sub.update(globals()); out = io.StringIO(); timer = time.monotonic()
        exec("async def fn():\n"+textwrap.indent(code, '    '), sub)
        with redirect_stdout(out): rtn = await sub['fn']()
        ttl = time.monotonic() - timer
        vl = out.getvalue()
        rnT = str(type(rtn)).split("'")[1].replace('`','\u200b`')
        if type(rtn) == str: rtn = f"`{rtn}'"
        vl, rtn = str(vl).replace('`','\u200b`'), str(rtn).replace('`','\u200b`')
        interpreter = f"```md\n#] <{rnT}> {rtn.strip()} ~ [{1000*ttl:.5f}ms] py{str(sysconfig.get_python_version())}``````\n{vl.strip()} ```"
        print(interpreter)
        if len(interpreter) > 2000:
            open('txt/interpreter.txt','w+').write(f"""\
<{rnT}> {rtn.strip()} ~ [{1000*ttl:.5f}ms] py{str(sysconfig.get_python_version())}
----------
{vl}""")
            await ctx.send('```diff\n-] IT OVERFLOWED```', file=discord.File(fp=open('txt/interpreter.txt')))
        else: await ctx.send(interpreter)
    except Exception as exc:
        timer = time.monotonic()
        good = False; lineno = len(code.splitlines())
        while not good:
            try:
                exec("async def fn():\n"+textwrap.indent('\n'.join(code.splitlines()[0:lineno]), '    '), sub)
                good = True;
            except:
               lineno -= 1; good = True if lineno == -1 else False
        if lineno != -1:
            with redirect_stdout(out): rtn = await sub['fn']()
        ttl = time.monotonic() - timer
        if lineno != -1:
            vl = out.getvalue().replace('`','\u200b`')
            rnT = str(type(rtn)).split("'")[1].replace('`','\u200b`')
            if type(rtn) == str:
                rtn = f"`{rtn}'".replace('`','\u200b`')
            vl, rtn = str(vl), str(rtn)
        else:
            vl=''; rnT = "NoneType"; rtn = 'None'
        rnV = str(type(exc)).split("'")[1]
        interpreter = f"""```md
#] <{rnT}> {rtn.strip()} ~ [{1000*ttl:.5f}ms] py{str(sysconfig.get_python_version())}``````diff
-] <{rnV}> `{str(exc).strip()}'``````
{vl}
{traceback.format_exc().replace('`','` ')}```"""
        if len(interpreter) > 2000:
            open('txt/interpreter.txt','w+').write(f"""\
<{rnT}> {rtn.strip()} ~ [{1000*ttl:.5f}ms] py{str(sysconfig.get_python_version())}
<{rnV}> `{str(exc).strip()}'
----------
{vl}
----------
{traceback.format_exc()}
""")
            await ctx.send('```diff\n-] IT OVERFLOWED```',file=discord.File(fp=open('txt/interpreter.txt')))
        else: await ctx.send(interpreter)


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
