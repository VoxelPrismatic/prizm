#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
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

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x00ffff)
async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
    return msgs

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen()
async def on_guild_join(guild): 
    await log(bot, "GUILD JOIN", f"SERVER // {guild}")
    pre = json.load(open('prefixes.json'))
    pre[guild.id]=';]'
    open('prefixes.json','w').write(json.dumps(pre,sort_keys=True,indent=4))
    com = json.load(open('servers.json'))
    for g in bot.guilds:
        try: x = com[str(g.id)]
        except:
            com[str(g.id)]={}
            com[str(g.id)]["com"]={}
            com[str(g.id)]["tag"]={}
        for c in bot.commands:
            try: x = com[str(g.id)]["com"][c]
            except: com[str(g.id)]["com"][c] = True
    open('servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))

@bot.listen()
async def on_guild_remove(guild): await log(bot, "GUILD LEFT", f"SERVER // {guild}")


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
