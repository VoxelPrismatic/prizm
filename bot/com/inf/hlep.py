#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, random
import asyncio, json
from util import pages
from dyn.faces import faces
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from pprint import pprint as pp
def entry(lit,coms:list,lbl,mini) -> list:
    """
    >>> CREATES AN ENTRY IN THE HELP TABLE <<<
    LIT  [LIST] - The Pages
    COMS [LIST] - The Commands
    LBL  [STR ] - Command Label
    """
    if len(coms) > (10 if not mini else 20):
        x = 0
        for y in coms:
            if not x % (10 if not mini else 20):
                lit.append(f'#] {lbl} [{int(x/(10 if not mini else 20))+1}/{len(range(0,len(coms),10))}]\n')
            lit[-1] += y +'\n'
            x += 1
    else:
        lit.append(f'#] {lbl}\n'+'\n'.join(coms))
    return lit

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

#help = 'math',
                  #brief = '',
                  #usage = ';]',
                  #description = '[NO ARGS FOR THIS COMMAND]'

@commands.command(aliases=["help"],
                  help = 'inf',
                  brief = 'Brings up this message',
                  usage = ';]help {?com}',
                  description = 'COM [command] - OPTIONAL: Brings up a help message for that specific command')
async def hlep(ctx, com:str=''):
    mini = False
    prefix = ';]'
    try:
        prefix = json.load(open('json/prefixes.json'))[str(ctx.guild.id)]
    except:
        pass
    if '-m' in com:
        mini = True
        com = com.replace('-m','').strip()
    if com:
        try:
            com = ctx.bot.get_command(com)
        except:
            return await ctx.send(f"```diff\n-] COMMAND '{com}' NOT FOUND```")
        return await ctx.send(f'''```md
#] HELP FOR {com.name.upper()} [CATAGORY: {com.help}]
=] {com.brief}
>  USAGE - '{com.usage.replace(';]',prefix)}'
>  ALIAS - {', '.join(com.aliases)}
{com.description}
```''')
    lit = []
    coms = {}
    cats = ['INF','FUN','MATH','DIS','OTH','INT','MUSIC','AI']
    for cat in cats:
        coms[cat] = []
    for com in ctx.bot.commands:
        if not mini:
            com_desc = f'] "{str(com.usage).replace(";]", prefix)}"\n>  {com.brief} '+random.choice(faces())
        else:
            com_desc = f'> {com.name}'
        try:
            if com.help in ['mod','own']:
                continue
            coms[com.help.upper()].append(com_desc)
        except:
            pass

    replce = {'INF':'INFO',
              'FUN':'FUN',
              'MATH':'MATHS',
              'DIS':'META',
              'OTH':'OTHER',
              'INT':'INTERACTIVE',
              'MUSIC':'MUSIC',
              'AI': 'AI'}
    for cat in coms:
        lit = entry(lit,coms[cat],replce[cat],mini)
    await pages.PageThis(ctx, lit, "COMMANDS LIST", f"""```md
#] {'{?stuff}'} - Optional argument
#] To see mod commands, use "{prefix}hlepmod"
#] Some of your data is stored, use "{prefix}data" to see more```""")


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hlep)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hlep')
    print('GOOD')