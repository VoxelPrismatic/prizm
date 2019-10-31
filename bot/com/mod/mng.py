#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing, asyncio
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from chk.gen import is_mod
from util.embedify import embedify
from util import dbman

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = ['manage', 'tor'],
                      help = 'mod',
                      brief = 'Brings up a management interface',
                      usage = ';]mng',
                      description = '''\
[NO INPUT FOR THIS COMMAND]
''')
@commands.check(enbl)
@commands.check(is_mod)
async def mng(ctx):
    gID = int(ctx.guild.id)
    msg = await ctx.send(embed=embedify(title='SERVER MANAGEMENT ;]', desc='''```md
#] MANAGE SERVER
>  Logging ---- [L]
>  Moderators - [M]
>  Ban Words -- [W]```'''))
    for x in ['L', 'M', 'W']:
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
        if rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER M}':
            lis = dbman.get('mod','name',id=gID, return_as_list = True)
            await msg.clear_reactions()
            await msg.edit(embed=embedify(title='SERVER MANAGEMENT ;]',
                        desc = '```md\n#] CURRENT MODS\n>  '+(
                        '\n>  '.join(lis) if len(lis) else '[NONE]') + '\n=] PING/TYPE USER\'s NAME TO ADD/REMOVE FROM LIST [SEP BY NEW LINE]```'))
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                await msg.delete()
                return await ctx.send('```diff\n-] TIMEOUT```')
            else:
                args = msg2.content.splitlines()
                await msg2.delete()
                for arg in args:
                    usr = None
                    if '<@!' in ''.join(arg) and '>' in ''.join(arg):
                        usr = ctx.guild.get_member(int(''.join(arg)[2:-1]))
                    elif '<@' in ''.join(arg) and '>' in ''.join(arg):
                        usr = ctx.guild.get_member(int(''.join(arg)[2:-1]))
                    else:
                        try:
                            usr = ctx.guild.get_member(int(arg))
                        except:
                            usr = ctx.guild.get_member_named(arg)
                    if not usr:
                        await ctx.send(f'```diff\n-] ERROR\n=] Member "{arg}" not found```')
                    if str(usr) in lis:
                        dbman.remove('mod', name=str(usr), id=ctx.guild.id)
                    else:
                        dbman.insert('mod', id=ctx.guild.id, name=str(usr))

        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER W}':
            lis = dbman.get('wrd','word',id=gID, return_as_list = True)
            if lis == None:
                lis = []
            await msg.clear_reactions()
            await msg.edit(embed=embedify(title='SERVER MANAGEMENT ;]',
                        desc='```md\n#] CURRENT BAN WORDS\n>  '+('\n>  '.join(lis) if len(lis) else '[NONE]') \
                            + '\n=] SEND WORDS TO ADD/REMOVE FROM LIST [SEP BY NEW LINE]```'))
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                await msg.delete()
                return await ctx.send('```diff\n-] TIMEOUT```')
            else:
                dbman.remove('wrd',)
                args = msg2.content.splitlines()
                await msg2.delete()
                for arg in args:
                    if arg in lis:
                        dbman.remove('wrd', id = ctx.guild.id, word = arg)
                    else:
                        dbman.insert('wrd', id = ctx.guild.id, word=arg)
        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER L}':
            logs = dbman.getCols('log')
            lis = {}
            for typ in logs:
                lis[typ] = dbman.get('log',typ,id=ctx.guild.id)
            lCH = dbman.get('oth','lCH',id=ctx.guild.id)
            await msg.clear_reactions()
            st = "```diff\n"
            rep = {'blk':'[BULK DELETE]',
                   'edt':'[EDIT MESSAGE]',
                   'typ':'[MEMBER TYPING]',
                   'del':'[DELETE MESSAGE]',
                   'mVC':'[VOICE STATUS UPDATE]',
                   'rt+':'[REACTION ADD]',
                   'rt-':'[REACTION REMOVE]',
                   'rt/':'[REACTION CLEAR]',
                   'em/':'[EMOJIS UPDATE]',
                   'gc+':'[CHANNEL CREATE]',
                   'gc-':'[CHANNEL DELETE]',
                   'gc/':'[CHANNEL UPDATE]',
                   'pin':'[PINS UPDATE]',
                   'int':'[INTEGRATION UPDATE]',
                   'web':'[WEBHOOKS UPDATE]',
                   'mb+':'[MEMBER JOIN]',
                   'mb-':'[MEMBER LEAVE]',
                   'mb/':'[MEMBER EDIT]',
                   'gl/':'[GUILD EDIT]',
                   'rl+':'[ROLE CREATE]',
                   'rl-':'[ROLE DELETE]',
                   'rl/':'[ROLE UPDATE]',
                   'bn+':'[MEMBER BANNED]',
                   'bn-':'[MEMBER UNBANNED]',
                   'bot':'[LOG BOT ACTIONS]'}
            for x in lis:
                st += f'{"+" if lis[x] else "-"}] {x} - {"Enabled" if lis[x] else "Disabled"} {rep[x]}'+'\n'
            st+=f'=] LOG CHANNEL - {str(await ctx.bot.fetch_channel(lCH)) if lCH else "[NONE]"} [PING CHANNEL TO CHANGE]\n'
            await msg.edit(embed=embedify(title='SERVER MANAGEMENT ;]',
                            desc=st+'=] TYPE CODE [ON LEFT] TO EN/DISABLE [SEP BY NEW LINE]```'))
            try:
                msg2 = await bot.wait_for('message',timeout=60.0,check=chc)
            except asyncio.TimeoutError:
                await ctx.send('```diff\n-] TIMEOUT```')
                return await msg.delete()
            else:
                args = msg2.content.splitlines()
                await msg2.delete()
                for arg in args:
                    if '<#' in arg and '>' in arg:
                        dbman.update('oth','lCH',int(arg[2:-1]),id=ctx.guild.id)
                        continue
                    try:
                        curLog = dbman.get('log',arg,id=ctx.guild.id)
                        dbman.update('log',arg,int(not curLog),id=ctx.guild.id)
                    except KeyError:
                        await ctx.send(f'```diff\n-] TOKEN "{arg}" NOT FOUND```')
        else:
            return await ctx.send('```diff\n-] INVALID REACTION, ABORTED```')

    await msg.delete()
    await ctx.send('```diff\n+] COMPLETE```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(mng)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('mng')
    print('GOOD')
