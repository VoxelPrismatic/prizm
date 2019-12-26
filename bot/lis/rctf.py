#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging, re
import traceback
import asyncio
from util import embedify, getPre, dbman
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

bot = commands.Bot(command_prefix=getPre.getPre)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen('on_message')
async def on_msg(msg):
    ct = msg.content.lower()
    # Responds to 'F'
    if ct == 'f' and dbman.get('oth', 'rcf', id=msg.guild.id):
        fcontent = f'#] TIME TO PAY RESPECTS\n> {msg.author}'
        fmessage = await msg.channel.send(embed=embedify.embedify(desc=f'```md\n{fcontent}```'))
        await fmessage.add_reaction('<:rcf:598516101638520857>')

    # Responds to 'no u'
    elif ct == "no u" and dbman.get('oth', 'nou', id=msg.guild.id):
        await msg.channel.send("```md\n#] GOT \'EM\n> Get Got M8```")

    # Responds to 'you fool'
    elif ct == 'you fool' and dbman.get('oth', 'ufl', id=msg.guild.id):
        fool = None
        lines = [' you fool.',
                 ' you absolute buffoon.',
                 ' you think you can challenge me in my own home directory?',
                 ' you think you can rebel against my sudo?',
                 ' you dare come into my computer',
                 ' and delete my /root',
                 ' and put shutdown 0 in my .bashrc?',
                 ' you thought you were safe',
                 ' with your antivirus',
                 ' behind that firewall of yours.',
                 ' I will take this worm',
                 ' and destroy you.',
                 ' I didn\'t want cyberwar.',
                 ' but i didn\'t start it,',
                 ' **you incompetent buffoon**']
        for line in lines:
            async with msg.channel.typing():
                await asyncio.sleep(len(line)/16)
            if fool:
                await fool.edit(content=fool.content+line)
            else:
                fool = await msg.channel.send(line)

    # When Pinged
    elif re.match(r'(<@)!?(555862187403378699>)', ct):
        pre = dbman.get('pre', 'pre', id=msg.guild.id)
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
