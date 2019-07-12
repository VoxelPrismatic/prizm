#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
@commands.has_permissions(manage_roles=True)
async def role(ctx, mbr:discord.Member, typ:str, rol:discord.Role, *, reason=None):
    if typ.lower() in ['add','+','give']: await mbr.add_roles(rol,reason=''.join(reason) if reason else f'REQUESTED BY ] {ctx.author.name}')
    elif typ.lower() in ['remove','take','-']: await mbr.remove_roles(rol,reason=''.join(reason) if reason else f'REQUESTED BY ] {ctx.author.name}')
    else: return await ctx.send(f'```diff\n-] ERROR - UNKNOWN KEY\n=] \'{typ}\' IS AN UNKNOWN KEY [-, +, add, give, take, remove]')
    await ctx.message.add_reaction('\N{OK HAND SIGN}') 

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(role)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('role')
    print('GOOD')
