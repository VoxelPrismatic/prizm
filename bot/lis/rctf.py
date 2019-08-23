#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback
import asyncio, json
from util import embedify, getPre
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

bot = commands.Bot(command_prefix=getPre.getPre)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen('on_message')
async def on_msg(msg):
    ct = msg.content
    # Responds to 'F'
    if ("f" == ct or "F" == ct) and json.load(open('json/servers.json'))[str(msg.guild.id)]["rcf"]:
        fcontent = f'#] TIME TO PAY RESPECTS\n> {msg.author}'
        fmessage = await msg.channel.send(embed=embedify.embedify(desc=f'```md\n{fcontent}```'))
        await fmessage.add_reaction('<:rcf:598516101638520857>')

    # When a user speaks to the AI
    elif ct == ']help':
        await msg.channel.send('```diff\n-] ERROR\n+] To see commands list, use ";]hlep"```')

    # Responds to 'no u'
    elif ct == "no u" and json.load(open('json/servers.json'))[str(msg.guild.id)]["nou"]:
        await msg.channel.send("```md\n#] GOT \'EM\n> Get Got M8```")

    # When Pinged
    elif ct == '<@!555862187403378699>' or ct == '<@555862187403378699>':
        pre = json.load(open("json/prefixes.json"))[str(msg.guild.id)]
        await msg.channel.send(f'```md\n#] INFO\n> My prefix is "{pre}"\n> For example: "{pre}hlep"```')

@bot.listen()
async def on_reaction_add(reaction,user):
    if reaction.message.author.id == 555862187403378699 and user.id != 555862187403378699:
        if len(reaction.message.embeds[0].description) > 34:
                og = reaction.message.embeds[0].description[5:-3]
                if str(user) not in og and 'PAY RESPECTS' in og:
                    await reaction.message.edit(embed=embedify.embedify(desc=f'```md{og}\n> {user}```'))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+LIS')
    bot.add_listener(on_reaction_add)
    bot.add_listener(on_msg, "on_message")
    print('GOOD')

def teardown(bot):
    print('-LIS')
    bot.remove_listener('on_reaction_add')
    bot.add_listener("on_msg", "on_message")
    print('GOOD')