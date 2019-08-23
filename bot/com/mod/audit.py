#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging, json, re
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.pages import PageThis

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'mod',
                  brief = 'Edits channels and things - Will change to an interface rather than a command',
                  usage = ';]audit {typ} {iID} {*args}',
                  description = 'TYP [OBJECT] - What to edit\niID [INT   ] - The ID of that object, must be the ID\n*ARGS - Type ";]audit help" to see them')
@commands.check(enbl)
@commands.guild_only()
async def audit(ctx, typ, iID:int=None, *args):
    kwargs = {}
    for arg in args: kwargs[arg.split('=')[0]]=eval(arg.split('=')[1])

    try:
        rsn = kwargs['reason']
    except:
        rsn = f'REQUESTED BY ] {ctx.author.name}#{ctx.author.discriminator}'
    kwargs['reason'] = rsn

    if ctx.author.name+'#'+str(ctx.author.discriminator) not in json.load(open('json/servers.json'))[str(ctx.guild.id)]['mod'] and ctx.author!=ctx.guild.owner:
        return await ctx.send('```diff\n-] SERVER MODS ONLY```')

    elif typ.lower() in ['channel','txt','ch','chnl','text','textchannel']:
        await ctx.guild.get_channel(iID).edit(**kwargs)

    elif typ.lower() in ['vc','voice','voicechannel']:
        await ctx.guild.get_channel(iID).edit(*kwargs)

    elif typ.lower() in ['mbr','user','usr','member','plr','player']:
        await ctx.guild.get_member(iID).edit(**kwargs)

    elif typ.lower() in ['gld','guild','srv','server','srvr']:
        await ctx.guild.edit(**kwargs)

    elif typ.lower() in ['role','rol']:
        await ctx.guild.get_role(iID).edit(**kwargs)

    elif typ.lower() in ['emoji','emj','emji']:
        await emj.edit(**kwargs)

    elif typ.lower() in ['catagory','cat']:
        await ctx.guild.get_channel(iID).edit(**kwargs)

    elif typ.lower() == 'help':
        await PageThis(ctx,[
'''#] GUILD
> name [str]
> description [str]
> icon [bytes]
> banner [bytes]
> splash [bytes]
> region [VoiceRegion]
> afk_channel [VoiceChannel]
> afk_timeout [int]
> owner [Member]
> verification_level [VerificationLevel]
> default_notifications [NotificationLevel]
> explicit_content_filter [ContentFilter]
> vanity_code [str]
> system_channel [TextChannel]
> system_channel_flags [SystemChannelFlags]''',
'''#] TEXT CHANNEL
> name [str]
> topic [str]
> position [int]
> nsfw [bool]
> sync_permissions [bool]
> catagory [CatagoryChannel]
> slowmode_delay [int]
-
#] CATAGORY
> name [str]
> position [int]
> nsfw [bool]''',
'''#] VC
> name [str]
> bitrate [int]
> user_limit [int]
> position [int]
> sync_permissions [bool]
> catagory [CatagoryChannel]
-
#] MEMBER
> nick [str]
> mute [bool]
> deafen [bool]
> roles [LIST: Role]
> voice_channel [VoiceChannel]''',
'''#] ROLE
> name [str]
> permissions [Permissions]
> color [Color]
> hoist [bool]
> mentionable [bool]
> position [int]
-
#] EMOJI
> name [str]
> roles [LIST: Role]'''], low='```md\n> reason [str]\n#] SYNTAX\n> <kwarg>=<value>\n#] HAVING TROUBLE WITH STRINGS? USE `\\u0020` INSTEAD!```',
    name='AUDIT HELP')

    else:
        return await ctx.send(f'```diff\n-] ALIAS \'{typ}\' NOT FOUND [chnl, vc, gld, mbr, emoji, catagory, role]```')

    await ctx.message.add_reaction('<:wrk:608810652756344851>')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(audit)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('audit')
    print('GOOD')
