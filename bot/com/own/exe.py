#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import io
import time
import discord                    #python3.7 -m pip install -U discord.py
import logging
import textwrap
import sysconfig
import contextlib
from discord.ext import commands
from contextlib import redirect_stdout
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def exe(ctx, *, code: str):
    st1 = time.monotonic()
    try:
        code = code.strip('\n').replace('py','').replace('`','')
        print(textwrap.indent(code, '    '))
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
            'message': ctx.message
        }
        sub.update(globals())
        out = io.StringIO()
        rs = exec("async def fn():\n"+textwrap.indent(code, '    '), sub)
        fn = sub['fn']
        st2 = time.monotonic()
        with redirect_stdout(out): rtn = await fn()
        ttl = time.monotonic() - st2
        vl = out.getvalue()
        await ctx.send(f'''```md
#] *.EXE 0.0
> RETURNED // {rtn}
> EXE TIME // {str(1000*ttl)[:10]}ms
> TTL TIME // {str(1000*(time.monotonic()-st1))[:10]}ms
> OUTPUTED // {"NONE" if vl == "" else f"{vl[:-1]}"}
> PYTHON V // {str(sysconfig.get_python_version())}```''')
    except Exception as exc:
        await ctx.send(f'''```diff
-] ERROR
-] TYPE // {type(exc).__name__}
{str(exc)}```''')


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
