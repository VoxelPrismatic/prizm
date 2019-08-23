#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'fun',
                  brief = 'In rememberance of DJ Quzingler [BOT]',
                  usage = ';]djq',
                  description = '[NO ARGS FOR THIS COMMAND]')
@commands.check(enbl)
async def djq(ctx):
    send = ""
    s = True
    data = "aeiou"
    cons = "bcdfghjklmnpqrstvwxyz"
    y = random.randint(1,10)
    for x in range(y):
        send = send+(cons[rand(0,len(cons)-1)])
        if x==y:
            if random.randint(0,1):
                send = send+(data[rand(0,len(data)-1)])
        else:
            send = send+(data[rand(0,len(data)-1)])
    await ctx.send(f'here you go friend, you can name it to anything you like, what about {send} ?')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(djq)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('djq')
    print('GOOD')
