#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, json
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from dyn.refresh import refresh
from util import jsonSave
def getPre(bot,msg):
    try:return json.load(open('prefixes.json'))[str(msg.guild.id)]
    except Exception as ex:print(ex);return ";]"

bot = commands.Bot(command_prefix=getPre)

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

#@bot.listen()
async def on_guild_join(g): 
    allext, lodtxt = refresh()
    bot.remove_command('help')
    try:pre = json.load(open('prefixes.json'))
    except: 
        open('prefixes.json','w').write('{"hi":"bye"}')
        pre = json.load(open('prefixes.json'))
    com = json.load(open('servers.json'))
    pre[str(g.id)] = ';]'
    com[str(g.id)]={}
    com[str(g.id)]["com"]={}
    com[str(g.id)]["tag"]={}
    com[str(g.id)]["nam"]=g.name
    com[str(g.id)]["rcf"] = True
    com[str(g.id)]["dr1"] = True
    com[str(g.id)]["nou"] = True
    open('servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    for ext in range(len(allext)-1):
        for nam in allext[ext]: 
            bot.load_extension(f'{lodtxt[ext]}{nam}')
            c = bot.get_command(nam)
            com[str(g.id)]["com"][c.name] = True
    open('servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    open('prefixes.json','w').write(json.dumps(pre,sort_keys=True,indent=4)) 

#@bot.listen()
async def on_guild_remove(guild):
    pre, com = json.load(open('prefixes.json')), json.load(open('servers.json'))
    del pre[str(guild.id)]; del com[str(guild.id)]
    open('prefixes.json','w').write(json.dumps(pre,sort_keys=True,indent=4))
    open('servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))


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
