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
from lis import twitter

global _inst
_inst = {}

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = ['manage', 'tor', 'config', 'conf'],
    help = 'mod',
    brief = 'Brings up a management interface for logging, twitter, starboard and more',
    usage = ';]mng',
    description = '''\
[NO INPUT FOR THIS COMMAND]
Manages:
- Logging
- Moderators
- Auto texts
- Starboard
- Twitter integration
'''
)
@commands.check(enbl)
@commands.check(is_mod)
async def mng(ctx):
    msg = await ctx.send(
        embed=embedify(
            title = 'SERVER MANAGEMENT ;]',
#>  Ban Words -- [W] [not implemented]
            desc = '''```md
#] MANAGE SERVER
>  Logging ---- [L]
>  Moderators - [M]
>  Auto Texts - [T]
>  Starboard -- [S]
>  Twitter ---- [\U0001f426]```'''))
    for x in ['L', 'M', 'T', 'S']:
        await msg.add_reaction(
            eval("'\\N{REGIONAL INDICATOR SYMBOL LETTER " + x + "}'")
        )
    for x in ["\U0001f426"]:
        await msg.add_reaction(x)
    bot = ctx.bot
    def chk(rct, mbr):
        try:
            ctx = _inst[rct.message.id]["ctx"]
            return mbr == ctx.author
        except KeyError:
            #Invalid
            return False
    def chc(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    global _inst
    _inst[msg.id] = {
        "msg": msg,
        "ctx": ctx
    }
    try:
        rct, mbr = await bot.wait_for('reaction_add', timeout = 60.0, check = chk)
    except asyncio.TimeoutError:
        await msg.delete()
        return await ctx.send("```diff\n-] TIMEOUT [60s]```")
    else:
        gID = int(_inst[rct.message.id]["ctx"].guild.id)
        msg = _inst[rct.message.id]["msg"]
        ctx = _inst[rct.message.id]["ctx"]
        if rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER M}':
            lis = dbman.get('mod', 'name', id = gID, return_as_list = True)
            await msg.clear_reactions()
            await msg.edit(
                embed = embedify(
                    title = 'SERVER MANAGEMENT ;]',
                    desc = '```md\n#] CURRENT MODS\n>  ' + (
                        '\n>  '.join(lis) if len(lis) else '[NONE]'
                    ) + '\n=] PING/TYPE USER\'s NAME TO ADD/REMOVE FROM LIST [SEP BY NEW LINE]```'
                )
            )
            try:
                msg2 = await bot.wait_for('message', timeout = 30.0, check = chc)
            except asyncio.TimeoutError:
                del _inst[msg.id]
                await msg.delete()
                return await ctx.send('```diff\n-] TIMEOUT [30s]```')
            else:
                del _inst[msg.id]
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
                        await ctx.send(f'```diff\n-] MEMBER "{arg}" NOT FOUND```')
                    if str(usr) in lis:
                        dbman.remove('mod', name = str(usr), id = ctx.guild.id)
                    else:
                        dbman.insert('mod', id = ctx.guild.id, name = str(usr))

        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER W}':
            lis = dbman.get('wrd','word',id=gID, return_as_list = True)
            if lis == None:
                lis = [""]
            await msg.clear_reactions()
            await msg.edit(
                embed = embedify(
                    title = 'SERVER MANAGEMENT ;]',
                    desc = '```md\n#] CURRENT BAN WORDS\n>  ' + (
                         '\n>  '.join(lis) if len(lis) else '[NONE]'
                    ) + '\n=] SEND WORDS TO ADD/REMOVE FROM LIST [SEP BY NEW LINE]```'
                )
            )
            try:
                msg2 = await bot.wait_for('message', timeout = 60.0, check = chc)
            except asyncio.TimeoutError:
                await msg.delete()
                del _inst[msg.id]
                return await ctx.send('```diff\n-] TIMEOUT [60s]```')
            else:
                del _inst[msg.id]
                dbman.remove('wrd',)
                args = msg2.content.splitlines()
                await msg2.delete()
                for arg in args:
                    if arg in lis:
                        dbman.remove('wrd', id = ctx.guild.id, word = arg)
                    else:
                        dbman.insert('wrd', id = ctx.guild.id, word = arg)
        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER L}':
            logs = dbman.getCols('log')
            lis = {}
            for typ in logs:
                lis[typ] = dbman.get('log', typ, id = ctx.guild.id)
            lCH = dbman.get('oth', 'lCH', id = ctx.guild.id)
            await msg.clear_reactions()
            st = "```diff\n"
            rep = {
                'blk':'[BULK DELETE]',
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
                'bot':'[LOG BOT ACTIONS]'
            }
            for x in lis:
                e = "+" if lis[x] else "-"
                t = "Enabled" if e == "+" else "Disabled"
                st += f'{e}] {x} - {t} {rep[x]}'+'\n'
            n = str(await ctx.bot.fetch_channel(lCH)) if lCH else "[NONE]"
            st += f'=] LOG CHANNEL - {n} [PING CHANNEL TO CHANGE]\n'
            await msg.edit(
                embed = embedify(
                    title = 'SERVER MANAGEMENT ;]',
                    desc = st + '=] TYPE CODE [ON LEFT] TO EN/DISABLE [SEP BY NEW LINE]```'
                )
            )
            try:
                msg2 = await bot.wait_for('message', timeout = 60.0, check = chc)
            except asyncio.TimeoutError:
                del _inst[msg.id]
                await ctx.send('```diff\n-] TIMEOUT [60s]```')
                return await msg.delete()
            else:
                del _inst[msg.id]
                args = msg2.content.splitlines()
                await msg2.delete()
                for arg in args:
                    if '<#' in arg and '>' in arg:
                        dbman.update('oth', 'lCH', int(arg[2:-1]), id = ctx.guild.id)
                        continue
                    try:
                        curLog = dbman.get('log', arg, id = ctx.guild.id)
                        dbman.update('log',arg,int(not curLog),id=ctx.guild.id)
                    except KeyError:
                        await ctx.send(f'```diff\n-] TOKEN "{arg}" NOT FOUND```')
        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER T}':
            txts = dbman.getCols('oth')
            txts.remove("lCH")
            lis = {}
            for typ in txts:
                lis[typ] = dbman.get('oth', typ, id = ctx.guild.id)
            await msg.clear_reactions()
            st = "```diff\n"
            rep = {
                'dr1':'[DRUAGA 1]',
                'rcf':'[RESPECTS]',
                'ufl':'[YOU FOOL]',
                'nou':'[NO, YOU]'
            }
            for x in lis:
                e = "+" if lis[x] else "-"
                t = "Enabled" if e == "+" else "Disabled"
                st += f'{e}] {x} - {t} {rep[x]}'+'\n'
            await msg.edit(
                embed = embedify(
                    title = 'SERVER MANAGEMENT ;]',
                    desc = st + '=] TYPE CODE [ON LEFT] TO EN/DISABLE [SEP BY NEW LINE]```'
                )
            )
            try:
                msg2 = await bot.wait_for('message', timeout = 15.0, check = chc)
            except asyncio.TimeoutError:
                del _inst[msg.id]
                await ctx.send('```diff\n-] TIMEOUT [15s]```')
                return await msg.delete()
            else:
                del _inst[msg.id]
                args = msg2.content.splitlines()
                await msg2.delete()
                for arg in args:
                    try:
                        curLog = dbman.get('oth', arg, id = ctx.guild.id)
                        dbman.update('oth', arg, int(not curLog), id = ctx.guild.id)
                    except KeyError:
                        await ctx.send(f'```diff\n-] TOKEN "{arg}" NOT FOUND```')
        elif rct.emoji == '\N{REGIONAL INDICATOR SYMBOL LETTER S}':
            await msg.clear_reactions()
            for x in ['\u0023\u20e3', '\u2b50', '\U0001f522', '\u2705', '\u2728']:
                await msg.add_reaction(x)
            while True:
                lis = dbman.get('star', *dbman.getCols("star"), id = gID, return_as_list = True)
                c = ctx.guild.get_channel(lis[3])
                e = lis[1]
                count = lis[2]
                multi = lis[3]
                await msg.edit(
                    embed = embedify(
                        title = 'SERVER MANAGEMENT ;]',
                        desc = f'''```md
#] STARBOARD SETTINGS

> CHANNEL ] #{c}
>   EMOJI ] {e}
>   COUNT ] {count if count else '[starboard disabled]'}
>   MULTI ] Multiple stars per user is {'en' if multi else 'dis'}abled
``````md
#] REACT TO EDIT STARBOARD

> CHANNEL --- \u0023\ufe0f\u20e3
> EMOJI ----- \u2b50
> COUNT ----- \U0001f522
> MULTI ----- \u2728
> DONE ------ \u2705
```'''
                    )
                )
                try:
                    r, m = await bot.wait_for('reaction_add', timeout = 15.0, check = chk)
                except asyncio.TimeoutError:
                    del _inst[msg.id]
                    return await msg.edit(content = "```diff\n-] TIMEOUT [15s]```")
                else:
                    if r.emoji == '\u2705':
                        break
                    elif r.emoji == '\u2728':
                        multi = int(not multi)
                        dbman.update('star', 'multi', multi, id = gID)
                        await ctx.send(f'```diff\n+] MULTIPLE STARS PER USER IS NOW {"en" if multi else "dis"}abled```')
                    elif r.emoji == "\u2b50":
                        m = await ctx.send("```md\n#] SEND AN EMOJI```")
                        try:
                            msg2 = await bot.wait_for('message', timeout = 20.0, check = chc)
                        except asyncio.TimeoutError:
                            del _inst[msg.id]
                            await m.delete()
                            return await msg.edit(content = '```diff\n-] TIMEOUT [20s]```')
                        await m.delete()
                        dbman.update('star', 'emoji', msg2.content, id = gID)
                        await ctx.send(f'```diff\n+] STARBOARD EMOJI SET TO `{msg2.content}\'```')
                        await msg2.delete()
                    elif r.emoji == "\U0001f522":
                        m = await ctx.send("```md\n#] SEND A NUMBER [send 0 to disable the starboard]```")
                        try:
                            msg2 = await bot.wait_for('message', timeout = 15.0, check = chc)
                        except asyncio.TimeoutError:
                            del _inst[msg.id]
                            await m.delete()
                            return await msg.edit(content = '```diff\n-] TIMEOUT [15s]```')
                        await m.delete()
                        try:
                            dbman.update('star', 'count', int(msg2.content), id = gID)
                            await ctx.send(f'```diff\n+] STARBOARD COUNT SET TO {msg2.content}```')
                            await msg2.delete()
                        except:
                            await msg2.delete()
                            del _inst[msg.id]
                            return await msg.edit(content = '```diff\n-] THAT ISN\'T A NUMBER```')
                    elif r.emoji == "\u0023\u20e3":
                        m = await ctx.send("```md\n#] PING A CHANNEL```")
                        try:
                            msg2 = await bot.wait_for('message', timeout = 20.0, check = chc)
                        except asyncio.TimeoutError:
                            del _inst[msg.id]
                            await m.delete()
                            return await msg.edit(content = '```diff\n-] TIMEOUT [20s]```')
                        await m.delete()
                        chid = msg2.content.split("<#")[-1].split(">")[0]
                        await msg2.delete()
                        try:
                            chid = int(chid)
                        except:
                            chid = 0
                        ch = ctx.guild.get_channel(chid)
                        if ch:
                            dbman.update('star', 'channel', chid, id = gID)
                            await ctx.send(f'```diff\n+] STARBOARD CHANNEL SET TO #{ch}```')
                        else:
                            del _inst[msg.id]
                            await msg.edit(content = '```diff\n-] THAT ISN\'T A CHANNEL```')
                            return
        elif rct.emoji == '\U0001f426':
            while True:
                await msg.clear_reactions()
                m2 = await ctx.send("Just a sec, fetching tweeters")
                lis = dbman.get('twitter', "user_id", "channel_id", id = gID, dont_touch = True)
                names = await twitter.get_usernames(*[l[0] for l in lis])
                ls = []
                send_to = {}
                ns = {}
                if lis:
                    for user_id, channel_id in lis:
                        ls.append(f"**{len(ls) + 1}]** [{names[user_id]}](https://twitter.com/{names[user_id]}) in <#{channel_id}>")
                        ns[len(ls)] = [user_id, channel_id]
                        try:
                            if channel_id not in send_to[user_id]:
                                send_to[user_id].append(channel_id)
                        except KeyError:
                            send_to[user_id] = [channel_id]
                else:
                    ls = ["[No tweeters]"]
                for x in ['\u2705', '\u274e']:
                    if x == '\u2705' and len(ls) == 20:
                        continue
                    await msg.add_reaction(x)
                await m2.delete()
                st = "\n".join(ls)
                await msg.edit(
                    embed = embedify(
                        title = 'SERVER MANAGEMENT ;]',
                        desc = f'''```md
#] TWITTER SETTINGS
=] Current tweeters:```
{st}

```md
#] OPTIONS
''' + ('> ADD ------ \u2705' if len(ls) < 20 else '[Only 20 tweeters allowed]') + f'''
> REMOVE --- \u274e
> SAVE ----- [wait 15s]
```'''
                    )
                )
                try:
                    r, m = await bot.wait_for('reaction_add', timeout = 15.0, check = chk)
                except asyncio.TimeoutError:
                    break
                else:
                    if r.emoji == '\u2705':
                        m2 = await ctx.send("```md\n#] SEND A NAME AND CHANNEL\n=] Format: {username} {channel}\n> VoxelPrismatic #twitter```")
                        try:
                            msg2 = await bot.wait_for('message', timeout = 60.0, check = chc)
                        except asyncio.TimeoutError:
                            del _inst[msg.id]
                            await m2.delete()
                            return await msg.edit(content = '```diff\n-] TIMEOUT [60s]```')
                        await m2.delete()
                        try:
                            channel = int(msg2.content.split("<#")[1].split(">")[0])
                        except:
                            del _inst[msg.id]
                            await msg2.delete()
                            return await msg.edit(content = '```diff\n-] INVALID OR MISSING CHANNEL```')
                        d = await twitter.get_json(f"https://api.twitter.com/2/users/by?usernames={msg2.content.split(' ')[0].strip('@')}", headers = twitter.auth)
                        try:
                            d["errors"]
                            del _inst[msg.id]
                            await msg2.delete()
                            return await msg.edit(content = '```diff\n-] INVALID TWITTER USER```')
                        except:
                            pass
                        try:
                            if channel not in send_to[d['data'][0]['id']]:
                                raise Exception
                        except:
                            dbman.insert("twitter", id = ctx.guild.id, user_id = d['data'][0]['id'], channel_id = channel)
                        await msg2.delete()

                    elif r.emoji == '\u274e':
                        m2 = await ctx.send(f"```md\n#] SEND A NUMBER FROM 1 TO {len(ls)} ```")
                        try:
                            msg2 = await bot.wait_for('message', timeout = 20.0, check = chc)
                        except asyncio.TimeoutError:
                            del _inst[msg.id]
                            await m2.delete()
                            return await msg.edit(content = '```diff\n-] TIMEOUT [20s]```')
                        await m2.delete()
                        try:
                            n = int(msg2.content)
                            if n < 1 or n > len(ls):
                                raise Exception
                            dbman.remove("twitter", id = gID, user_id = ns[n][0], channel_id = ns[n][1])
                        except:
                            await msg2.delete()
                            del _inst[msg.id]
                            return await msg.edit(content = '```diff\n-] THAT ISN\'T A VALID NUMBER```')
        else:
            await msg.delete()
            return await ctx.send('```diff\n-] INVALID REACTION, ABORTED```')
    try:
        del _inst[msg.id]
    except:
        pass
    await msg.delete()
    await ctx.send('```md\n#] COMPLETED```')

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
