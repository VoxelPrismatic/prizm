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
import asyncio
import shlex
import io

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

def get_output(lim = False):
    out = open("out.txt").read()
    err = open("err.txt").read()
    if lim:
        out = out[-600:]
        err = err[-600:]
    return f'''```md
#] stdOUT
{out}___``````diff
-] stdERR
{err}___```'''

@commands.command(
    help = 'own',
    brief = 'Executes a shell command',
    usage = ';]shell {code}',
    description = '''\
CODE [TEXT] - The shell code to execute
'''
)
@commands.is_owner()
async def shell(ctx, *, code:str):
    st1 = time.monotonic()
    msgs = await ctx.send('```md\n#] JUST A MOMENT\n> Running for 0s```')
    msg_ = await ctx.send('\*output goes here\*')
    try:
        proc = subprocess.Popen(
            shlex.split(code.replace('---shell','')),
            stdout = open("/home/priz/Desktop/PRIZM/out.txt", "wb+"),
            stderr = open("/home/priz/Desktop/PRIZM/err.txt", "wb+")
        )
        t = 0
        while proc.poll() is None:
            await asyncio.sleep(0.25)
            t += 0.25
            if t == int(t):
                await msgs.edit(content = f'```md\n#] JUST A MOMENT\n> Running for {t}s```')
                await msg_.edit(content = get_output(True))
        interpreter_lim = get_output(True)
        interpreter = get_output()
        print(interpreter)
        await ctx.send(
            interpreter_lim,
            file = discord.File(io.BytesIO(interpreter.encode()), "bash.txt")
        )
    except Exception as exc:
        tb = traceback.format_exc().replace('`','\u200b`')
        await ctx.send(f'''```diff
-] ERROR
-] TYPE // {type(exc).__name__}
> {str(exc)}
{tb}```''')
    await msgs.delete()
    await msg_.delete()


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
