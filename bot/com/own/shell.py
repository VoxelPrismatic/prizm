#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import time
import discord                    #python3.7 -m pip install -U discord.py
import logging
import subprocess
import traceback
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from util.pages import PageThis

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'own',
                  brief = '',
                  usage = ';]',
                  description = '[NO ARGS FOR THIS COMMAND]')
@commands.is_owner()
async def shell(ctx, *, code:str):
    st1 = time.monotonic()
    msgs = await ctx.send('```md\n#] JUST A MOMENT```')
    try:
        st2 = time.monotonic()
        proc = subprocess.run(code.replace('---shell','').split(), capture_output=True,shell=('---shell' in code), timeout = 120.0)
        out = proc.stdout.decode().replace('`','\u200b`')
        err = proc.stderr.decode().replace('`','\u200b`')
        ttl = time.monotonic() - st2
        interpreter = f'''```md
{out}{err}
] ==================
> EXE TIME // {str(1000*ttl)[:10]}ms
```'''
        print(interpreter)
        if len(interpreter) > 2000:
            open('txt/interpreter.txt','w+').write(f"""\
> EXE TIME // {str(1000*ttl)[:10]}ms
----------
{out}{err}
""")
            await ctx.send('```diff\n-] IT OVERFLOWED```',file=discord.File(fp=open('txt/interpreter.txt')))
        else: await ctx.send(interpreter)

    except Exception as exc:
        tb = traceback.format_exc().replace('`','\u200b`')
        await ctx.send(f'''```diff
-] ERROR
-] TYPE // {type(exc).__name__}
> {str(exc)}
{tb}```''')


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
