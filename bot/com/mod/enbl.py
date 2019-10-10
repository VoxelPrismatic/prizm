#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import dbman
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
    if str(ctx.author.name) not in dbman.get('mod', 'name', id=ctx.guild.id) and ctx.author != ctx.guild.owner:
        return await ctx.send('```diff\n-] SERVER MODS ONLY```')
    if not ctx.bot.get_command(nam):
        return ctx.send('```diff\n-] COMMAND DOESNT EXIST```')
    dbman.update('com', ctx.bot.get_command(nam).name, 1, id=ctx.guild.id)
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

@commands.command(aliases=['disable'],
                  help = 'mod',
                  brief = 'Disables a {command}',
                  usage = ';]dsbl {com_name}',
                  description = 'COM NAME [STR] - The name of the target command')
@commands.guild_only()
async def dsbl(ctx,nam):
    if str(ctx.author.name) not in dbman.get('mod', 'name', id=ctx.guild.id) and ctx.author != ctx.guild.owner:
        return await ctx.send('```diff\n-] SERVER MODS ONLY```')
    if not ctx.bot.get_command(nam):
        return ctx.send('```diff\n-] COMMAND DOESNT EXIST```')
    dbman.update('com', ctx.bot.get_command(nam).name, 0, id=ctx.guild.id)
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

@commands.command(aliases=['prefix'],
                  help = 'mod',
                  brief = 'Changes the prefix to {pre}',
                  usage = ';]pre {pre}',
                  description = 'PRE [STR] - The new prefix')
@commands.guild_only()
async def pre(ctx,nam):
    if str(ctx.author.name) not in dbman.get('mod', 'name', id=ctx.guild.id) and ctx.author != ctx.guild.owner:
        return await ctx.send('```diff\n-] SERVER MODS ONLY```')
    dbman.update('com', 'pre', pre, id=ctx.guild.id)
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
