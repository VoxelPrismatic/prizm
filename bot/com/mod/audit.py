#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing, ast, asyncio
import discord                    #python3.7 -m pip install -U discord.py
import logging, re
from util import dbman
from chk.gen import is_mod
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.pages import PageThis
from util.embedify import embedify

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

def getArgs(st:str):
    kwargs = {}
    for arg in st.splitlines():
        if '__' in arg.split('=')[1].strip():
            pass
        kwargs[arg.split('=')[0].strip()] = eval(arg.split('=')[1].strip(), {}, {'discord':discord})
    return kwargs

async def edit_target(ctx, target):
    try:
        msg2 = await ctx.bot.wait_for('message',timeout=60.0,check=chc)
    except asyncio.TimeoutError:
        return await ctx.send("```diff\n-] TIMEOUT```")
    else:
        kwargs = getArgs(msg2.content)
        await msg2.delete()
        try:
            kwargs['reason']
        except:
            kwargs['reason'] = f'REQUESTED BY ] {str(ctx.author)}'
        await target.edit(**kwargs)

@commands.command(
    aliases = [],
    help = 'mod',
    brief = 'Edits channels and things',
    usage = ';]audit',
    description = '''\
[NO INPUT FOR THIS COMMAND]
'''
)
@commands.check(enbl)
@commands.check(is_mod)
async def audit(ctx):
    msg = await ctx.send(embed=embedify(title='MANAGEMENT ;]',
                                        desc='''```md
#] AUDIT MANAGER ;]
>  Edit TextChannel -- [T]
>  Edit VoiceChannel - [V]
>  Edit Member/User -- [M]
>  Edit Guild -------- [G]
>  Edit Role --------- [R]
>  Edit Emoji -------- [E]
>  Edit Catagory ----- [C]```'''))
    for x in ['T', 'V', 'M', 'G', 'R', 'E', 'C']:
        await msg.add_reaction(eval("'\\N{REGIONAL INDICATOR SYMBOL LETTER "+x+"}'"))
    bot = ctx.bot
    def chk(rct,mbr):
        return mbr==ctx.author
    def chc(msg):
        return msg.author==ctx.author and msg.channel==ctx.channel

    try:
        rct, mbr = await bot.wait_for('reaction_add',timeout=60.0,check=chk)
    except asyncio.TimeoutError:
        return await ctx.send("```diff\n-] TIMEOUT```")
    else:

        if rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER T}':
            await msg.clear_reactions()
            await msg.edit(
                embed = embedify(
                    title = 'TEXT CHANNEL MANAGEMENT ;]',
                    desc = '```md\n#] PLEASE PING A CHANNEL TO CONTINUE```'
                )
            )
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                return await ctx.send("```diff\n-] TIMEOUT```")
            else:
                target = discord.utils.find(lambda c: c.name == msg2.content or f'<#{c.id}>' == msg2.content \
                                            or str(c.id) == msg2.content, ctx.guild.text_channels)
                await msg2.delete()
                if not target:
                    return await ctx.send(f'```diff\n-] TEXT CHANNEL NOT FOUND```')
                await msg.edit(
                    embed = embedify(
                        title = f'#{target.name} MANAGEMENT ;]',
                        desc = f'''```md
#] OPTIONS FOR TEXT CHANNEL #{target.name}
> [TEXT] name      [is currently '{target.name}']
> [TEXT] topic
> [NUM ] position  [is currently {target.position}]
> [T/F ] nsfw      [is currently {target.nsfw}]
> [T/F ] sync_permissions
> [NUM ] slowmode_delay [is currently {target.slowmode_delay}]
> [TEXT] reason    [DEFAULT: 'REQUESTED BY ] {ctx.author}']
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''
                    )
                )
                await edit_target(ctx, target)

        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER V}':
            await msg.clear_reactions()
            await msg.edit(
                embed = embedify(
                    title='VOICE CHANNEL MANAGEMENT ;]',
                    desc = '```md\n#] PLEASE TYPE THE NAME OF A VOICE CHANNEL TO CONTINUE```'
                )
            )
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                return await ctx.send("```diff\n-] TIMEOUT```")
            else:
                target = discord.utils.find(lambda c: c.name == msg2.content or str(c.id) == msg2.content, ctx.guild.voice_channels)
                await msg2.delete()
                if not target:
                    return await ctx.send(f'```diff\n-] VOICE CHANNEL NOT FOUND```')
                await msg.edit(
                    embed = embedify(
                        title = f'#{target.name} MANAGEMENT ;]',
                        desc = f'''```md
#] OPTIONS FOR VOICE CHANNEL #{target.name}
> [TEXT] name       [is currently '{target.name}']
> [NUM ] bitrate    [is currently {target.bitrate}]
> [NUM ] user_limit [is currently {target.user_limit}]
> [NUM ] position   [is currently {target.position}]
> [T/F ] sync_permissions
> [TEXT] reason     [DEFAULT: 'REQUESTED BY ] {ctx.author}']
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''
                    )
                )
                await edit_target(ctx, target)

        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER M}':
            await msg.clear_reactions()
            await msg.edit(
                embed = embedify(
                    title = 'MEMBER MANAGEMENT ;]',
                    desc = '```md\n#] PLEASE PING A MEMBER TO CONTINUE```'
                )
            )
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                return await ctx.send("```diff\n-] TIMEOUT```")
            else:
                target = discord.utils.find(
                    lambda c: c.name == msg2.content or \
                           f'<@{c.id}>' == msg2.content or \
                           str(c.id) == msg2.content or \
                           f'{c.name}#{c.discriminator}' == msg2.content or \
                           c.nick == msg2.content,
                   ctx.guild.members
                )
                await msg2.delete()
                if not target:
                    return await ctx.send(f'```diff\n-] MEMBER NOT FOUND```')
                await msg.edit(
                    embed = embedify(
                        title = f'@{target.name} MANAGEMENT ;]',
                        desc = f'''```md
#] OPTIONS FOR MEMBER @{target.name}
> [TEXT] nick      [is currently '{target.name}']
> [T/F ] mute      [is currently {target.voice.mute if target.voice else "None"}]
> [T/F ] deafen    [is currently {target.voice.deaf if target.voice else "None"}]
> [ROLE] roles     [use the ';]role' command]
> [TEXT] reason    [DEFAULT: 'REQUESTED BY ] {str(ctx.author)}']
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''
                    )
                )
                await edit_target(ctx, target)

        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER G}':
            await msg.clear_reactions()
            target = ctx.guild
            await msg.edit(
                embed = embedify(
                    title = f'GUILD MANAGEMENT ;]',
                    desc = f'''```md
#] OPTIONS FOR GUILD
> [STR ] name        [is currently '{target.name}']
> [STR ] description
> [INT ] afk_timeout [is currently {target.afk_timeout}]
> [STR ] vanity_code [is currently {target.vanity_code}]
> [STR ] reason      [DEFAULT: 'REQUESTED BY ] {str(ctx.author)}']
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''
                )
            )
            await edit_target(ctx, target)

        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER R}':
            await msg.clear_reactions()
            await msg.edit(
                embed = embedify(
                    title = 'ROLE MANAGEMENT ;]',
                    desc = '```md\n#] PLEASE PING A ROLE TO CONTINUE```'
                )
            )
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                return await ctx.send("```diff\n-] TIMEOUT```")
            else:
                target = discord.utils.find(lambda c: c.name == msg2.content or f'<@&{c.id}>' == msg2.content or str(c.id) == msg2.content or \
                                                      f'@{c.name}' == msg2.content or f'<&{c.id}>' == msg2.content, ctx.guild.roles)
                await msg2.delete()
                if not target:
                    return await ctx.send(f'```diff\n-] ROLE NOT FOUND```')
                await msg.edit(
                    embed = embedify(
                        title = f'&{target.name} MANAGEMENT ;]',
                        desc = f'''```md
#] OPTIONS FOR ROLE {target.name}
> [TEXT] name        [is currently '{target.name}']
> [TEXT] color       [is currently '{target.color}']
> [T/F ] hoist       [is currently {target.hoist}]
> [T/F ] mentionable [is currently {target.mentionable}]
> [NUM ] position    [is currently {target.position}]
> [TEXT] reason      [DEFAULT: 'REQUESTED BY ] {str(ctx.author)}']
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''
                    )
                )
                await edit_target(ctx, target)


        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER C}':
            await msg.clear_reactions()
            await msg.edit(
                embed = embedify(
                    title = 'CATEGORY MANAGEMENT ;]',
                    desc = '```md\n#] PLEASE TYPE THE NAME OF A CATEGORY TO CONTINUE```'
                )
            )
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                return await ctx.send("```diff\n-] TIMEOUT```")
            else:
                target = discord.utils.find(lambda c: c.name == msg2.content or f'<#{c.id}>' == msg2.content \
                                            or str(c.id) == msg2.content, ctx.guild.categories)
                await msg2.delete()
                if not target:
                    return await ctx.send(f'```diff\n-] CATEGORY NOT FOUND```')
                await msg.edit(
                    embed = embedify(
                        title = f'${target.name} MANAGEMENT ;]',
                        desc = f'''```md
#] OPTIONS FOR CATEGORY {target.name}
> [TEXT] name      [is currently '{target.name}']
> [NUM ] position  [is currently {target.position}]
> [T/F ] nsfw      [is currently {target.nsfw}]
> [TEXT] reason    [DEFAULT: 'REQUESTED BY ] {ctx.author}']
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''
                    )
                )
                await edit_target(ctx, target)
    await msg.delete()
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
