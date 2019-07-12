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

@commands.command()
async def bug(ctx, *, txt):
    async with ctx.channel.typing():
        try: st = f'```md\n#] BUG REPORT IN {ctx.channel.name} - {ctx.guild.name} BY {ctx.author.name}#{ctx.author.discriminator}\n> {txt}```'
        except: st = f"```md\n#] BUG REPORT IN PRIVATE MESSAGE WITH {ctx.author.name}#{ctx.author.discriminator}\n> {txt}```"
    await ctx.bot.get_channel(597577735065436171).send(st)


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(bug)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('bug')
    print('GOOD')

