#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import json
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
def getPre(bot,msg):
    try:return json.load(open('prefixes.json'))[str(msg.guild.id)]
    except Exception as ex:print(ex);return ";]"

bot = commands.Bot(command_prefix=getPre)

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
    return msgs


##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen()
async def when_mentioned(msg):
    print('hi')
    pre = json.load(open("prefixes.json"))[str(msg.guild.id)]
    await msg.channel.send(f'```md\n#]INFO\n> My prefix is `{pre}`\n> For example: "{pre}hlep"```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_listener(when_mentioned)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_listener('when_mentioned')
    print('GOOD')
