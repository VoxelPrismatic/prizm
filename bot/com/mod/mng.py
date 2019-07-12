#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging, json
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=['manage','tor'])
@commands.guild_only()
async def mng(ctx, what:str, typ:str, *arg):
    if ctx.author != ctx.guild.owner: return await ctx.send('```diff\n-] ERROR\n=] Only the server owner can use this command```')
    com = json.load(open('servers.json')); gID = str(ctx.guild.id)
    if what.lower() in ['mod','mods','moderator','moderators','m']:
        usr = 'NONE'
        if '<@' in ''.join(arg) and '>' in ''.join(arg): usr = ctx.guild.get_member(int(''.join(arg)[2:-1]))
        else:
            try:
                usr = ctx.guild.get_member(int(''.join(arg)))
                usr = ctx.guild.get_member_named(''.join(arg))
            except:
                if usr == 'NONE': return await ctx.send('```diff\n-] ERROR\n=] Member not found```')
        try:
            lis = com[gID]["mod"]
            if typ.lower() in ['+','add','plus']: lis.append(f'{usr.name}#{user.discriminator}')
            elif typ.lower() in ['-','remove','take']: lis.remove(f'{usr.name}#{user.discriminator}')
            else: return await ctx.send(f'```diff\n-] ERROR\n=] ALIAS \'{typ}\' NOT FOUND [-, +, add, remove]')
        except Exception as ex: return await ctx.send(f'```diff\n-] ERROR\n=] {ex}```')
    
    elif what.lower() in ['w','word','words','keyword','keywords']:
        lis = com[gID]["wrd"]
        if typ.lower() in ['+','add','plus']: lis["wrd"].extend(arg)
        elif typ.lower() in ['-','remove','take']:
            for word in arg: lis["wrd"].remove(word)
        elif typ.lower() in ['/','act','action']: lis["wrd"] = arg
        else: return await ctx.send(f'```diff\n-] ERROR\n=] ALIAS \'{typ}\' NOT FOUND [-, +, /, add, remove, act]')
    
    else: return await ctx.send(f'```diff\n-] ERROR\n=] ALIAS \'{what}\' NOT FOUND [w, m, word, mod]')
    
    open('servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    await ctx.message.add_reaction('\N{OK HAND SIGN}')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(mng)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('mng')
    print('GOOD')

