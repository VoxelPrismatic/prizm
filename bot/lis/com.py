#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

def getPre(bot,msg):
    id = msg.guild.id
    try:return json.load(open('prefixes.json'))[str(id)]
    except Exception as ex:print(ex);return ";]"

bot = commands.Bot(command_prefix=getPre)

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify.embedify(desc=f'''```md\n#] {head}!\n> {text}```'''))
    return msgs


##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen()
async def on_command_completion(ctx):
    await log(ctx.bot, 'COMMAND', f'''----
>  COM // {ctx.command}
> ARGS // {ctx.args[1:]}
> CHNL // {ctx.channel.name}
>  USR // {ctx.author}
>  GLD // {ctx.guild}''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+LIS')
    bot.add_listener(on_command_completion)
    print('GOOD')

def teardown(bot):
    print('-LIS')
    bot.remove_listener('on_command_completion')
    print('GOOD')
