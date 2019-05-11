#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
bot = commands.Bot(command_prefix=";]")

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x00ffff)
async def log(bot, head, text): #use "ctx.bot" for the bot
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
    return msgs


##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen('on_message')
async def on_msg(msg):
    ct = msg.content
    if "f" == ct or "F" == ct:
        fcontent = f'#] TIME TO PAY RESPECTS\n> {msg.author} PAID RESPECTS'
        fmessage = await msg.channel.send(embed=embedify(f'```md\n{fcontent}```'))
        await fmessage.add_reaction('🇫')
        try: reaction, user = await bot.wait_for('reaction_add', timeout=600.0)
        except asyncio.TimeoutError: return await fmessage.clear_reactions()
        else:
            fcontent = fcontent+f'\n> {user} PAID RESPECTS'
            if str(reaction.emoji) == '🇫': await fmessage.edit(embed=embedify(f'```md\n{fcontent}```'))
    elif ct == ']help': await msg.channel.send('```diff\n-] ERROR\n+] To see commands list, use ";]hlep"```')
    elif ct == "no u": await msg.channel.send("```md\n#] GOT \'EM\n> Get Got M8```")
    elif ct == "druaga1sec":
        await msg.delete()
        await msg.channel.send('```md\n#] just, just, just a sec ;]\n> I\'m installing a GT420 into an XServe 0.0```')

#@bot.listen()
#async def on_reaction_add(reaction,user):
    #try:
        #if str(user) not in reaction.message.content:
            #if reaction.message.author.id == 555862187403378699 and user.id != 555862187403378699:
                #if 'PAID RESPECTS' in reaction.message.content:
                    #await reaction.message.edit(embed = embedify(f'```md{reaction.message.embeds[0].description[5:-3]}\n> {user} PAID RESPECTS```'))
    #except discord.HTTPException: await exc(ctx, 1)
    #except discord.Forbidden: await exc(ctx, 2)
    #except discord.NotFound: await exc(ctx, 3)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+LIS')
    #bot.add_listener(on_reaction_add)
    bot.add_listener(on_msg, "on_message")
    print('GOOD')

def teardown(bot):
    print('-LIS')
    #bot.remove_listener('on_reaction_add')
    bot.add_listener("on_msg", "on_message")
    print('GOOD')
