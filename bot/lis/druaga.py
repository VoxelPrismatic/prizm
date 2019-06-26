#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback
from util import embedify, pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
def getPre(bot,msg):
    id = msg.guild.id
    try:return json.load(open('prefixes.json'))[str(id)]
    except Exception as ex:print(ex);return ";]"

bot = commands.Bot(command_prefix=getPre)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen()
async def druaga(dru):
    ct = dru.content
    if "druaga1" in ct:
        print('DRUAGA1!')
        druagas = {
            'druaga1sec':['just, just, just a sec ;]',
                        'I\'m installing a GT420 into an XServe 0.0'],
            'druaga1ram':['WHERE THE RAM GONE? 0.0',
                        'i wanna install windows 2 :C'],
            'druaga1button': ['here button button button 0.0',
                            'where are you? ;-;'],
            'druaga1btn': ['here button button button 0.0',
                            'where are you? ;-;'],
            'druaga1screen': ['and this screen is reflective enough that you can see stuff... :C',
                              'and thats really annoying while im trying to film stuff'],
            'druaga1pb': ['*finger touches powerbook 170* 9.6',
                          'OH SHIT! FUCK! IVE NEVER BLED SO MUCH IN MY LIFE XC']
            }
        if ct in druagas:
            await dru.delete()
            await dru.channel.send(f'```md\n#] {druagas[ct][0]}\n> {druagas[ct][1]}```')
        else:
            await dru.add_reaction("<:druaga1:579442502092849192>")

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+LIS')
    bot.add_listener(druaga, "on_message")
    print('GOOD')

def teardown(bot):
    print('-LIS')
    bot.remove_listener('druaga', 'on_message')
    print('GOOD')
