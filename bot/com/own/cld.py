#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
from dyn import refresh
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify.embedify(desc=f'''```md\n#] {head}!\n> {text}```'''))
    return msgs

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

def lext(name, bot): bot.load_extension(name); print(f'>Lext {name}')
def rext(name, bot): bot.reload_extension(name); print(f'>Rext {name}')
def uext(name, bot): bot.unload_extension(name); print(f'>Uext {name}')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def rld(ctx, *name):
    allext, lodtxt = refresh.refresh()
    await log(ctx.bot, 'EXT', 'Reloading EXT[s]')
    async with ctx.channel.typing():
        if not len(name):
            for ext in range(len(allext)):
                for com in allext[ext]: rext(f"{lodtxt[ext]}{com}", ctx.bot)
        else: rext(name[0], ctx.bot)
    await log(ctx.bot, 'EXT', 'EXT[s] successfully reloaded')
    await ctx.message.add_reaction('<:wrk:608810652756344851>')
    
@commands.command()
@commands.is_owner()
async def uld(ctx, *name):
    allext, lodtxt = refresh.refresh()
    await log(ctx.bot, 'EXT', 'Unloading EXT[s]')
    async with ctx.channel.typing():
        if not len(name):
            for ext in range(len(allext)):
                for com in allext[ext]: uext(f"{lodtxt[ext]}{com}", ctx.bot)
        else: uext(name[0], ctx.bot)
    await log(ctx.bot, 'EXT', 'EXT[s] successfully unloaded')
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

@commands.command()
@commands.is_owner()
async def fld(ctx, typ):
    allext, lodtxt = refresh.refresh()
    for ext in range(len(allext)):
        for com in allext[ext]:
            try:
                if typ == "l": lext(f"{lodtxt[ext]}{com}", ctx.bot)
                if typ == "r": rext(f"{lodtxt[ext]}{com}", ctx.bot)
                if typ == "u": uext(f"{lodtxt[ext]}{com}", ctx.bot)
            except: pass
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

@commands.command()
@commands.is_owner()
async def ld(ctx, *name):
    allext, lodtxt = refresh.refresh()
    await log(ctx.bot, 'EXT', 'Loading EXT[s]')
    async with ctx.channel.typing():
        if not len(name):
            for ext in range(len(allext)):
                for com in allext[ext]: lext(f"{lodtxt[ext]}{com}", ctx.bot)
        else: lext(name[0], ctx.bot)
    await log(ctx.bot, 'EXT', 'EXTS[s] successfully loaded')
    await ctx.message.add_reaction('<:wrk:608810652756344851>')
    
##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rld)
    bot.add_command(uld)
    bot.add_command(fld)
    bot.add_command(ld)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rld')
    bot.remove_command('uld')
    bot.remove_command('fld')
    bot.remove_command('ld')
    print('GOOD')

