#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
bot = commands.Bot(command_prefix=";]")

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x00ffff)
async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
    return msgs

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen()
async def on_guild_join(guild): await log(guild.me, "GUILD JOIN", f"SERVER // {guild}")

@bot.listen()
async def on_guild_remove(guild): await log(guild.me, "GUILD LEFT", f"SERVER // {guild}")


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_listener(on_guild_join)
    bot.add_listener(on_guild_remove)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_listener('on_guild_join')
    bot.remove_listener('on_guild_remove')
    print('GOOD')
