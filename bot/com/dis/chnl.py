#!/chnl/bin/env python3
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

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def chnl(ctx, _chnl:discord.TextChannel):
    result = 0
    def check(reaction, user): return user == ctx.author
    lit = [f"""
      ID // {_chnl.id}
     POS // {_chnl.position}
    NAME // {_chnl.name}
   GROUP // {_chnl.category.name}
 CREATED // {_chnl.created_at}"""]
    ovrrds = []
    for thing in _chnl.overwrites:
        ovr = _chnl.overwrites_for(thing)
        perms = []
        if ovr.create_instant_invite: perms.append("create_instant_invite")
        if ovr.kick_members: perms.append("kick_members")
        if ovr.ban_members: perms.append("ban_members")
        if ovr.administrator: perms.append("administrator")
        if ovr.manage_channels: perms.append("manage_channels")
        if ovr.manage_guild: perms.append("manage_guild")
        if ovr.view_audit_log: perms.append("view_audit_log")
        if ovr.priority_speaker: perms.append("priority_speaker")
        if ovr.read_messages: perms.append("read_messages")
        if ovr.send_messages: perms.append("send_messages")
        if ovr.send_tts_messages: perms.append("send_tts_messages")
        if ovr.manage_messages: perms.append("manage_messages")
        if ovr.embed_links: perms.append("embed_links")
        if ovr.attach_files: perms.append("attach_files")
        if ovr.read_message_history: perms.append("read_message_history")
        if ovr.mention_everyone: perms.append("mention_everyone")
        if ovr.external_emojis: perms.append("external_emojis")
        if ovr.connect: perms.append("connect")
        if ovr.speak: perms.append("speak")
        if ovr.mute_members: perms.append("mute_members")
        if ovr.deafen_members: perms.append("deafen_members")
        if ovr.move_members: perms.append("move_members")
        if ovr.use_voice_activation: perms.append("use_voice_activation")
        if ovr.change_nickname: perms.append("change_nickname")
        if ovr.manage_nicknames: perms.append("manage_nicknames")
        if ovr.manage_roles: perms.append("manage_roles")
        if ovr.manage_webhooks: perms.append("manage_webhooks")
        if ovr.manage_emojis: perms.append("manage_emojis")
        lit.append(f"OVERRIDE [{thing}] // {', '.join(perms)}")
    msgchnl = await ctx.send(embed=embedify(f'''```md
#] CHANNEL INFO``````
{lit[result]}
```'''))
    await msgchnl.add_reaction('⏪')
    await msgchnl.add_reaction('◀')
    await msgchnl.add_reaction('⏹')
    await msgchnl.add_reaction('▶')
    await msgchnl.add_reaction('⏩')
    while True:
        try: reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError: return await msgchnl.clear_reactions()
        else:
            if str(reaction.emoji) == '⏪':
                result = 0
                await msgchnl.remove_reaction('⏪', ctx.author)
            elif str(reaction.emoji) == '◀':
                await msgchnl.remove_reaction('◀', ctx.author)
                result = result - 1
                if result < 0: result = len(lit) - 1
            elif str(reaction.emoji) == '⏹':
                return await msgchnl.clear_reactions()
            elif str(reaction.emoji) == '▶':
                await msgchnl.remove_reaction('▶', ctx.author)
                result = result+1
                if result > (len(lit) - 1): result = 0
            elif str(reaction.emoji) == '⏩':
                result = len(lit) - 1
                await msgchnl.remove_reaction('⏩', ctx.author)
            await msgchnl.edit(embed=embedify(f'''```md
#] CHANNEL INFO``````
{lit[result]}
```'''))


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(chnl)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('chnl')
    print('GOOD')

