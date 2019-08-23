#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, json
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=['json'])
@commands.is_owner()
async def srvedit(ctx,gID:int,element,datatype,*,value):
    com = json.load(open('json/servers.json'))
    if datatype=='str':
        com[str(gID)][element]=value
    elif datatype=='float':
        com[str(gID)][element]=float(value)
    elif datatype=='int':
        com[str(gID)][element]=int(value)
    elif datatype=='bool':
        com[str(gID)][element]=False if value=='False' else True
    elif datatype=='list+':
        com[str(gID)][element].append(value)
    elif datatype=='list-':
        com[str(gID)][element].remove(value)
    elif datatype=='list':
        com[str(gID)][element]=list(value)
    else:
        return await ctx.send('```diff\n-] INVALID DATATYPE```')
    open('json/servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(srvedit)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('srvedit')
    print('GOOD')