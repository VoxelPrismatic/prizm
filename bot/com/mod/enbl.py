#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, json
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl as en

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=['enable'])
@commands.guild_only()
async def enbl(ctx,nam):
    g=ctx.guild
    if f'{ctx.author.name}#{ctx.author.discriminator}' not in json.load(open('servers.json'))[str(ctx.guild.id)]["mod"] and ctx.author!=ctx.guild.owner:
        return await ctx.send('```diff\n-] ERROR\n=] Only the server mods can use this command```')
    if nam not in [c.name for c in ctx.bot.commands]: return ctx.send('```diff\n-] ERROR\n=] That command doesn\'t exist```')
    com = json.load(open('servers.json'))
    com[str(g.id)]["com"][nam]=True
    open('servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    await ctx.message.add_reaction('\N{OK HAND SIGN}')

@commands.command(aliases=['disable'])
@commands.guild_only()
async def dsbl(ctx,nam):
    g=ctx.guild
    if f'{ctx.author.name}#{ctx.author.discriminator}' not in json.load(open('servers.json'))[str(ctx.guild.id)]["mod"] and ctx.author!=ctx.guild.owner:
        return await ctx.send('```diff\n-] ERROR\n=] Only the server mods can use this command```')
    if nam not in [c.name for c in ctx.bot.commands]: return ctx.send('```diff\n-] ERROR\n=] That command doesn\'t exist```')
    com = json.load(open('servers.json'))
    com[str(g.id)]["com"][nam]=False
    open('servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    await ctx.message.add_reaction('\N{OK HAND SIGN}')
    
@commands.command(aliases=['prefix'])
@commands.guild_only()
async def pre(ctx,nam):
    g=ctx.guild
    if f'{ctx.author.name}#{ctx.author.discriminator}' not in json.load(open('servers.json'))[str(ctx.guild.id)]["mod"] and ctx.author!=ctx.guild.owner:
        return await ctx.send('```diff\n-] ERROR\n=] Only the server mods can use this command```')
    pr = json.load(open('prefixes.json'))
    pr[str(g.id)]=nam
    open('prefixes.json','w').write(json.dumps(pr,sort_keys=True,indent=4))
    await ctx.message.add_reaction('\N{OK HAND SIGN}')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(enbl)
    bot.add_command(dsbl)
    bot.add_command(pre)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('enbl')
    bot.remove_command('dsbl')
    bot.remove_command('pre')
    print('GOOD')