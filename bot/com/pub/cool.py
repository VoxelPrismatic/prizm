#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def cool(ctx, user:int):
    strtemp = '////////'
    await ctx.channel.purge(limit = 1)
    coolthing = await ctx.send(strtemp)
    varslol = True
    rickroll = f'''
Never gonna give <@{user}> up!
Never gonna let <@{user}> down!
Never gonna run around, and, desert you!
Never gonna make <@{user}> cry!
Never gonna say goodbye!
Never gonna run around, and, desert you!
'''
    while varslol == True:
        try:
            for x in range(125):
                strtemp = f'{strtemp}////////'
                await coolthing.edit(content = f'{strtemp}')
            varslol = False
            await ctx.send(rickroll)
        except:
            if not varslol: await coolthing.edit(rickroll)
            else:
                await ctx.send('YOU WILL NOT END THIS!')
                strtemp = '////////'
                coolthing = await ctx.send(strtemp)


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

