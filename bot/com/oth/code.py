#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing, base64
import discord                    #python3.7 -m pip install -U discord.py
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = ['exec'],
                      help = 'oth',
                      brief = 'A public exec command to test your code!',
                      usage = ';]code {lang} {code}',
                      description = '''\
LANG [STR] - The language to use
> 'js' for JavaScript
> 'py' for Python
> 'tr' for Boolean Logic
CODE [STR] - The code to execute
''')
@commands.check(enbl)
async def code(ctx, lang, *, code):
    code = code.replace('\n','\\n')
    url = f"https://voxelprismatic.github.io/code_online/?.code={code}?.lang={lang}"
    prizlink = "https://voxelprismatic.github.io/prizlink/?url=" + base64.b64encode(url.encode()).decode()
    await ctx.send(embed=embedify.embedify(title="CODE ONLINE ;]", desc=f"```md\n#] CLICK LINK TO VIEW RESULTS!!!```\n[LINK ;]]({prizlink})"))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(code)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('code')
    print('GOOD')
