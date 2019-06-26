#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import time
import discord                    #python3.7 -m pip install -U discord.py
import logging
import subprocess
import traceback, sysconfig
from discord.ext import commands
from contextlib import redirect_stdout
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from util.pages import PageThis

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def shell(ctx, *, code:str):
    st1 = time.monotonic()
    msgs = await ctx.send('```md\n#]JUST A MOMENT```')
    aray = code.split(' ',1)
    try:
        st2 = time.monotonic()
        out = subprocess.run(aray, capture_output=True, timeout=180).stdout.decode()
        ttl = time.monotonic() - st2
        print(f'''```md
#] *.EXE 0.0
> EXE TIME // {str(1000*ttl)[:10]}ms
> TTL TIME // {str(1000*(time.monotonic()-st1))[:10]}ms
] ======== // ========
{out}
```''')
        if len(out) < 1000: await ctx.send(f'''```md
#] *.EXE 0.0
> EXE TIME // {str(1000*ttl)[:10]}ms
> TTL TIME // {str(1000*(time.monotonic()-st1))[:10]}ms
] ======== // ========
{out}
```''')
        else: 
            lit = [f'''
#] *.EXE 0.0
> EXE TIME // {str(1000*ttl)[:10]}ms
> TTL TIME // {str(1000*(time.monotonic()-st1))[:10]}ms
] ======== // ========''']; s = ""
            for x in out.splitlines():
                if len(s+'\n'+x)>1990:  lit.append(s);s=x
                else: s+='\n'+x
            return await PageThis(ctx,lit,'it overflowed UwU')
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
    bot.add_command(shell)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('shell')
    print('GOOD')