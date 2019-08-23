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

@commands.command(help = 'inf',
                  brief = 'Creates a bug report',
                  usage = ';]bug {txt}',
                  description = 'TXT [STR] - The bug, preferably with the error and command')
async def bug(ctx, *, txt):
    async with ctx.channel.typing():
        try:
            st = f'```md\n#] BUG REPORT IN {ctx.channel.name} - {ctx.guild.name} BY {ctx.author.name}#{ctx.author.discriminator}\n> {txt}```'
        except:
            st = f"```md\n#] BUG REPORT IN PRIVATE MESSAGE WITH {ctx.author.name}#{ctx.author.discriminator}\n> {txt}```"
    await ctx.bot.get_channel(597577735065436171).send(st)
    await ctx.message.add_reaction('<:wrk:608810652756344851>')


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

