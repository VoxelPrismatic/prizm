#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, json
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl as en

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=['enable'],
                  help = 'mod',
                  brief = 'Enables a {command}',
                  usage = ';]enbl {com_name}',
                  description = 'COM NAME [STR] - The name of the target command')
@commands.guild_only()
async def enbl(ctx,nam):
    g=ctx.guild
    if f'{ctx.author.name}#{ctx.author.discriminator}' not in json.load(open('json/servers.json'))[str(ctx.guild.id)]["mod"] and ctx.author!=ctx.guild.owner:
        return await ctx.send('```diff\n-] ERROR\n=] Only the server mods can use this command```')
    if nam not in [c.name for c in ctx.bot.commands]:
        return ctx.send('```diff\n-] ERROR\n=] That command doesn\'t exist```')
    com = json.load(open('json/servers.json'))
    com[str(g.id)]["com"][nam]=True
    open('json/servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

@commands.command(aliases=['disable'],
                  help = 'mod',
                  brief = 'Disables a {command}',
                  usage = ';]dsbl {com_name}',
                  description = 'COM NAME [STR] - The name of the target command')
@commands.guild_only()
async def dsbl(ctx,nam):
    g=ctx.guild
    if f'{ctx.author.name}#{ctx.author.discriminator}' not in json.load(open('json/servers.json'))[str(ctx.guild.id)]["mod"] and ctx.author!=ctx.guild.owner:
        return await ctx.send('```diff\n-] ERROR\n=] Only the server mods can use this command```')
    if nam not in [c.name for c in ctx.bot.commands]:
        return ctx.send('```diff\n-] ERROR\n=] That command doesn\'t exist```')
    com = json.load(open('json/servers.json'))
    com[str(g.id)]["com"][nam]=False
    open('json/servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

@commands.command(aliases=['prefix'],
                  help = 'mod',
                  brief = 'Changes the prefix to {pre}',
                  usage = ';]pre {pre}',
                  description = 'PRE [STR] - The new prefix')
@commands.guild_only()
async def pre(ctx,nam):
    g=ctx.guild
    if f'{ctx.author.name}#{ctx.author.discriminator}' not in json.load(open('json/servers.json'))[str(ctx.guild.id)]["mod"] and ctx.author!=ctx.guild.owner:
        return await ctx.send('```diff\n-] ERROR\n=] Only the server mods can use this command```')
    pr = json.load(open('json/prefixes.json'))
    pr[str(g.id)]=nam
    open('json/prefixes.json','w').write(json.dumps(pr,sort_keys=True,indent=4))
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

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
