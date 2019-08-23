#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing, ast
import discord                    #python3.7 -m pip install -U discord.py
import logging, json, re
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
        kwargs[arg.split('=')[0].strip()] = ast.literal_eval(arg.split('=')[1].strip())
    return kwargs

@commands.command(help = 'mod',
                  brief = 'Edits channels and things',
                  usage = ';]audit',
                  description = '[NO ARGS FOR THIS COMMAND]')
@commands.check(enbl)
@commands.guild_only()
async def audit2(ctx):

    if ctx.author.name+'#'+str(ctx.author.discriminator) not in json.load(open('json/servers.json'))[str(ctx.guild.id)]['mod'] and ctx.author!=ctx.guild.owner:
        return await ctx.send('```diff\n-] SERVER MODS ONLY```')

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
            await msg.edit(embed=embedify(title='TEXT CHANNEL MANAGEMENT ;]',
                                          desc = '```md\n#] PLEASE PING A CHANNEL TO CONTINUE```'))
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                return await ctx.send("```diff\n-] TIMEOUT```")
            else:
                target = discord.utils.find(lambda c: c.name == msg2.content or f'<#{c.id}>' == msg2.content or str(c.id) == msg2.content, ctx.guild.text_channels)
                await msg2.delete()
                if not target:
                    return await ctx.send(f'```diff\n-] TEXT CHANNEL NOT FOUND```')
                await msg.edit(embed=embedify(title=f'#{target.name} MANAGEMENT ;]',
                                              desc = f'''```md
#] OPTIONS FOR TEXT CHANNEL #{target.name}
> [STR ] name      [is currently '{target.name}']
> [STR ] topic
> [INT ] position  [is currently {target.position}]
> [BOOL] nsfw      [is currently {target.nsfw}]
> [BOOL] sync_permissions
> [INT ] slowmode_delay [is currently {target.slowmode_delay}]
> [STR ] reason    [DEFAULT: 'REQUESTED BY ] {str(ctx.author)}]
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''))
                try:
                    msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
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

        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER V}':
            await msg.clear_reactions()
            await msg.edit(embed=embedify(title='VOICE CHANNEL MANAGEMENT ;]',
                                          desc = '```md\n#] PLEASE TYPE THE NAME OF A VOICE CHANNEL TO CONTINUE```'))
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                return await ctx.send("```diff\n-] TIMEOUT```")
            else:
                target = discord.utils.find(lambda c: c.name == msg2.content or str(c.id) == msg2.content, ctx.guild.voice_channels)
                await msg2.delete()
                if not target:
                    return await ctx.send(f'```diff\n-] VOICE CHANNEL NOT FOUND```')
                await msg.edit(embed=embedify(title=f'#{target.name} MANAGEMENT ;]',
                                              desc = f'''```md
#] OPTIONS FOR VOICE CHANNEL #{target.name}
> [STR ] name       [is currently '{target.name}']
> [INT ] bitrate    [is currently {target.bitrate}]
> [INT ] user_limit [is currently {target.user_limit}]
> [INT ] position   [is currently {target.position}]
> [BOOL] sync_permissions
> [STR ] reason     [DEFAULT: 'REQUESTED BY ] {str(ctx.author)}]
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''))
                try:
                    msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
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

        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER M}':
            await msg.clear_reactions()
            await msg.edit(embed=embedify(title='MEMBER MANAGEMENT ;]',
                                          desc = '```md\n#] PLEASE PING A MEMBER TO CONTINUE```'))
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                return await ctx.send("```diff\n-] TIMEOUT```")
            else:
                target = discord.utils.find(lambda c: c.name == msg2.content or f'<@{c.id}>' == msg2.content or str(c.id) == msg2.content or \
                                                      f'{c.name}#{c.discriminator}' == msg2.content or c.nick == msg2.content, ctx.guild.members)
                await msg2.delete()
                if not target:
                    return await ctx.send(f'```diff\n-] MEMBER NOT FOUND```')
                await msg.edit(embed=embedify(title=f'@{target.name} MANAGEMENT ;]',
                                              desc = f'''```md
#] OPTIONS FOR MEMBER @{target.name}
> [STR ] nick      [is currently '{target.name}']
> [BOOL] mute      [is currently {target.voice.mute if target.voice else "None"}]
> [BOOL] deafen    [is currently {target.voice.deaf if target.voice else "None"}]
> [ROLE] roles     [use the ';]role' command]
> [STR ] reason    [DEFAULT: 'REQUESTED BY ] {str(ctx.author)}]
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''))
                try:
                    msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
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

        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER G}':
            await msg.clear_reactions()
            target = ctx.guild
            await msg.edit(embed=embedify(title=f'GUILD MANAGEMENT ;]',
                                            desc = f'''```md
#] OPTIONS FOR GUILD
> [STR ] name        [is currently '{target.name}']
> [STR ] description
> [INT ] afk_timeout [is currently {target.afk_timeout}]
> [STR ] vanity_code [is currently {target.vanity_code}]
> [STR ] reason      [DEFAULT: 'REQUESTED BY ] {str(ctx.author)}]
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''))
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
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

        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER R}':
            await msg.clear_reactions()
            await msg.edit(embed=embedify(title='ROLE MANAGEMENT ;]',
                                          desc = '```md\n#] PLEASE PING A ROLE TO CONTINUE```'))
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                return await ctx.send("```diff\n-] TIMEOUT```")
            else:
                target = discord.utils.find(lambda c: c.name == msg2.content or f'<@&{c.id}>' == msg2.content or str(c.id) == msg2.content or \
                                                      f'@{c.name}' == msg2.content, ctx.guild.members)
                await msg2.delete()
                if not target:
                    return await ctx.send(f'```diff\n-] ROLE NOT FOUND```')
                await msg.edit(embed=embedify(title=f'@{target.name} MANAGEMENT ;]',
                                              desc = f'''```md
#] OPTIONS FOR ROLE @{target.name}
> [STR ] name        [is currently '{target.name}']
> [COL ] color       [is currently {target.color}]
> [BOOL] hoist       [is currently {target.hoist}]
> [BOOL] mentionable [is currently {target.mentionable}]
> [INT ] position    [is currently {target.position}]
> [STR ] reason      [DEFAULT: 'REQUESTED BY ] {str(ctx.author)}]
#] SYNTAX: 'arg=bool', 'arg="String"', 'arg=int', sep args by new line```'''))
                try:
                    msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
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

    #elif typ.lower() in ['emoji','emj','emji']:
        #await emj.edit(**kwargs)

    #elif typ.lower() in ['catagory','cat']:
        #await ctx.guild.get_channel(iID).edit(**kwargs)

    await ctx.message.add_reaction('<:wrk:608810652756344851>')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(audit2)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('audit2')
    print('GOOD')
