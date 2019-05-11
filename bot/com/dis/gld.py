#!/gld/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text, thumb): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d).set_thumbnail(url=thumb)
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def gld(ctx):
    _gld = ctx.guild
    result = 0
    chnls = []; rols = []; emjs = []
    def check(reaction, user): return user == ctx.author
    lit = [f"""
      ID // {_gld.id}
     AFK // {_gld.afk_timeout} - {_gld.afk_channel}
    NAME // {_gld.name}
    DESC // {_gld.description}
  BANNER // {_gld.banner_url}
  REGION // {_gld.region}
  NOTIFS // {_gld.default_notifications}
 CREATED // {_gld.created_at}""",
            f""" MFA LVL // {_gld.mfa_level}
   OWNER // {_gld.owner}
   LARGE // {_gld.large}
FEATURES // {_gld.features}
VRFY LVL // {_gld.verification_level}
NUM MBRS // {_gld.member_count}"""]
    for channel in _gld.channels:
        if len(f"{', '.join(chnls)},{channel.name}") > 2000:
            lit.append(f"CHANNELS // {', '.join(chnls)}")
            chnls = [];chnls.append(f"{channel.name}")
        else: chnls.append(f"{channel.name}")
    if len(chnls) > 0: lit.append(f"CHANNELS // {', '.join(chnls)}")
    for role in _gld.roles:
        if len(f"{', '.join(rols)},{role.name}") > 2000:
            lit.append(f"ROLES // {', '.join(rols)}")
            rols = [];rols.append(f"{role.name}")
        else: rols.append(f"{role.name}")
    if len(rols) > 0: lit.append(f"ROLES // {', '.join(rols)}")
    for emot in _gld.emojis:
        if len(f"{', '.join(emjs)},{emot.name}") > 2000:
            lit.append(f"EMOJI // {', '.join(emjs)}")
            emjs = [];emjs.append(f"{emot.name}")
        else: emjs.append(f"{emot.name}")
    if len(emjs) > 0: lit.append(f"EMOJI // {', '.join(emjs)}")
    msggld = await ctx.send(embed=embedify(f'''```md
#] GUILD INFO``````
{lit[result]}
```''', _gld.icon_url))
    await msggld.add_reaction('⏪')
    await msggld.add_reaction('◀')
    await msggld.add_reaction('⏹')
    await msggld.add_reaction('▶')
    await msggld.add_reaction('⏩')
    while True:
        try: reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError: return await msggld.clear_reactions()
        else:
            if str(reaction.emoji) == '⏪':
                result = 0
                await msggld.remove_reaction('⏪', ctx.author)
            elif str(reaction.emoji) == '◀':
                await msggld.remove_reaction('◀', ctx.author)
                result = result - 1
                if result < 0: result = len(lit) - 1
            elif str(reaction.emoji) == '⏹':
                return await msggld.clear_reactions()
            elif str(reaction.emoji) == '▶':
                await msggld.remove_reaction('▶', ctx.author)
                result = result+1
                if result > (len(lit) - 1): result = 0
            elif str(reaction.emoji) == '⏩':
                result = len(lit) - 1
                await msggld.remove_reaction('⏩', ctx.author)
            await msggld.edit(embed=embedify(f'''```md
#] GUILD INFO``````
{lit[result]}
```''', _gld.icon_url))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(gld)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('gld')
    print('GOOD')

