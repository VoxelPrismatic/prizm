#!/rol/bin/env python3
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
async def rol(ctx, *, _rol:discord.Role):
    try:
        perms = []
        if _rol.permissions.create_instant_invite: perms.append("create_instant_invite")
        if _rol.permissions.kick_members: perms.append("kick_members")
        if _rol.permissions.ban_members: perms.append("ban_members")
        if _rol.permissions.administrator: perms.append("administrator")
        if _rol.permissions.manage_channels: perms.append("manage_channels")
        if _rol.permissions.manage_guild: perms.append("manage_guild")
        if _rol.permissions.view_audit_log: perms.append("view_audit_log")
        if _rol.permissions.priority_speaker: perms.append("priority_speaker")
        if _rol.permissions.read_messages: perms.append("read_messages")
        if _rol.permissions.send_messages: perms.append("send_messages")
        if _rol.permissions.send_tts_messages: perms.append("send_tts_messages")
        if _rol.permissions.manage_messages: perms.append("manage_messages")
        if _rol.permissions.embed_links: perms.append("embed_links")
        if _rol.permissions.attach_files: perms.append("attach_files")
        if _rol.permissions.read_message_history: perms.append("read_message_history")
        if _rol.permissions.mention_everyone: perms.append("mention_everyone")
        if _rol.permissions.external_emojis: perms.append("external_emojis")
        if _rol.permissions.connect: perms.append("connect")
        if _rol.permissions.speak: perms.append("speak")
        if _rol.permissions.mute_members: perms.append("mute_members")
        if _rol.permissions.deafen_members: perms.append("deafen_members")
        if _rol.permissions.move_members: perms.append("move_members")
        if _rol.permissions.use_voice_activation: perms.append("use_voice_activation")
        if _rol.permissions.change_nickname: perms.append("change_nickname")
        if _rol.permissions.manage_nicknames: perms.append("manage_nicknames")
        if _rol.permissions.manage_roles: perms.append("manage_roles")
        if _rol.permissions.manage_webhooks: perms.append("manage_webhooks")
        if _rol.permissions.manage_emojis: perms.append("manage_emojis")
        await ctx.send(embed=embedify(f'''```
      ID // {_rol.id}
     POS // {_rol.position}
    NAME // {_rol.name}
   COLOR // {_rol.color}
   HOIST // {_rol.hoist}
   PERMS // {', '.join(perms)}
 CREATED // {_rol.created_at}
 MANAGED // {_rol.managed}
 MENTION // {_rol.mentionable}
PERM VAL // {_rol.permissions.value}
```'''))
    except discord.HTTPException: await exc(ctx, 1)
    except discord.Forbidden: await exc(ctx, 2)
    except discord.NotFound: await exc(ctx, 3)


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rol)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rol')
    print('GOOD')
