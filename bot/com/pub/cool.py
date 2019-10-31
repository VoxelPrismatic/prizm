#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                 help = 'fun',
                  brief = 'Gives someone a sneaky surprise',
                  usage = ';]cool {member}',
                  description = '''\
MEMBER [MEMBER] - The member you want to surprise, ping or name or ID
''')
@commands.check(enbl)
async def cool(ctx, member:discord.Member):
    await ctx.message.delete()
    await ctx.send(f'''
Never gonna give <@{member.id}> up!
Never gonna let <@{member.id}> down!
Never gonna run around, and, desert you!
Never gonna make <@{member.id}> cry!
Never gonna say goodbye!
Never gonna run around, and, desert you!
''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(cool)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('cool')
    print('GOOD')

