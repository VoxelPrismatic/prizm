#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, random, typing
import praw, re, time, prawcore as craw
from util.priz_err import *
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.praw_util import *
from util.praw_util import reddit as rd
from util.embedify import embedify

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

def grab_nsfw(sbd):
    try:
        ls = list(sbd.new(limit=1))
    except craw.exceptions.Redirect:
        raise PrizmRedditError()
    if isinstance(sbd, praw.models.Subreddit): return sbd.over18
    if isinstance(sbd, praw.models.Multieddit): return sbd.over_18
    return False

async def get(thing, msg):
    ls, x = [], 0
    for sbn in thing:
        x += 1
        ls.append(sbn)
        if not x%50:
            async with msg.channel.typing():
                await msg.edit(content=msg.content[:-3]+" /```")
    return ls

@commands.command(
    aliases = ['rd', 'redd', 'rdt', 'red'],
    help = 'fun',
    brief = 'Gives you a random post from a given {subreddit}',
    usage = ';]reddit {?subreddit} {?search}',
    description = '''\
SUBREDDIT [TEXT] - The name of the subredditm /r/ is optional
> /u/ is required to redditor feeds
> also can be a link to a submission
> /m/<multireddit>#<redditor> is needed for multireddits
> > eg /m/CoolMultireddit#Redditor1010
SEARCH    [TEXT] - What to search for
'''
)
@commands.check(enbl)
async def reddit(ctx, subreddit:str, *, search = ''):
    msg = await ctx.send('```md\n#] LOGGING IN```')
    async with ctx.channel.typing():
        red = rd()
        is_user, is_multi, is_nsfw = False, False, False
    allow_nsfw = ctx.channel.is_nsfw()
    await msg.edit(content='```md\n#] FINDING SUBREDDIT```')
    if re.search(r"^https?\://", subreddit):
        board = "post"
        await msg.edit(content='```md\n#] GRABBING LINK```')
        sbn = post(red, subreddit)
        if sbn.over_18 and not allow_nsfw:
            raise PrizmNsfwError()
    else:
        sbd = None
        if 'm/' in subreddit:
            if '#' not in subreddit:
                raise PrizmSyntaxError("/m/<multireddit>#<redditor>")
            sbd = multi(red, subreddit.split('#')[-1],
                        subreddit.split('#')[0].split('m/')[-1])
            is_nsfw = grab_nsfw(sbd)
            isMulti = True
            await msg.edit(content='```md\n#] GRABBING MULTIREDDIT```')
        elif 'u/' in subreddit:
            sbd = user(red, subreddit.split('u/')[-1])
            isRedditor = True
            await msg.edit(content='```md\n#] GRABBING REDDITOR```')
        elif 'r/' in subreddit:
            sbd = sub(red, subreddit.split('r/')[-1])
            is_nsfw = grab_nsfw(sbd)
            await msg.edit(content='```md\n#] GRABBING SUBREDDIT```')
        else:
            sbd = sub(red, subreddit)
            is_nsfw = grab_nsfw(sbd)
            await msg.edit(content='```md\n#] GRABBING SUBREDDIT```')
        if is_nsfw and not ctx.channel.is_nsfw():
            raise PrizmNsfwError()
        async with ctx.channel.typing(): pass
        if search and not is_user:
            board = "search"
            sbq = await get(sbd.search(search, limit=200), msg)
        else:
            sort = random.choice(['n', 'h', 't', 'c'] + (['r'] if not is_user else []))
            thing = {
                "n": [(lambda sb, ms: get(sb.new(limit = 200), ms)), "new"],
                "h": [(lambda sb, ms: get(sb.hot(limit = 200), ms)), "hot"],
                "t": [(lambda sb, ms: get(sb.top(limit = 200), ms)), "top"],
                "c": [(lambda sb, ms: get(sb.controversial(limit = 200), ms)), "controversial"],
                "r": [(lambda sb, ms: get(sb.rising(limit = 200), ms)), "rising"]
            }
            sbh, board = thing[sort]
            sbq = await sbh(sbd, msg)
        if type(sbq) != list: return
        sbn = random.choice(sbq)
        attempts = 0
        await msg.edit(content='```md\n#] PARSING POST```')
        while ((sbn.over_18 and not allow_nsfw) or not sbn) and attempts < 200:
            sbn = random.choice(sbq)
            attempts += 1
        if attempts >= 200 and sbn.over_18 and not allow_nsfw:
            return await msg.edit(content='```diff\n-] ONLY NSFW POSTS FOUND```')
    if type(sbn) == praw.models.Submission:
        txt = sbn.selftext.replace('>!','||').replace('!<','||')
        lnk = sbn.permalink
        src = sbn.url.split('//')[1].split('/')[0].split('www.')[-1]
        if src == 'reddit.com':
            src = "self."+sbn.subreddit.display_name
        prm = sbn.shortlink
        lnk = sbn.url
    attrib = ''
    warn = ''
    if sbn.locked or time.time() - sbn.created_utc > 15552000: 
        attrib += '[-] '
    if sbn.stickied: 
        attrib += '[>- '
    if sbn.edited: 
        attrib += '=> '
    if sbn.is_self: 
        attrib += 'TXT '
    else: 
        attrib += 'O-O '
    if sbn.over_18: 
        attrib += '<!> '
    if sbn.spoiler: 
        attrib += '[||] '
    if not any(lnk.endswith(f'.{fmt}') for fmt in ['gif', 'jpg', 'jpeg', 'png']):
        warn = '```diff\n-] Try clicking "[IMAGE]"```'
    await ctx.send(
        embed = embedify(
            title = f'REDDIT ;] - {src}',
            desc=f"""```md
#] {sbn.title}
]] FLAIR ] [{sbn.link_flair_text}]
]] SCORE ] {sbn.score}
>  OTHER ] {attrib if attrib else '[NONE]'}```
[[POST]]({prm}) [[IMAGE]]({lnk})
{warn}""",
            img = lnk if not txt else None,
            fields = [
                ['CONTENT', txt if len(txt) <= 1024 else txt[:1021]+'...', False]
            ] if sbn.is_self else [],
            foot = f"/r/{sbn.subreddit.display_name}/{board} // "
                   f"/u/{sbn.author.name if sbn.author else '[DELETED]'} "
                   f"{'// /m/' + sbd.display_name if is_multi else ''}"
        )
    )
    await msg.delete()

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(reddit)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('reddit')
    print('GOOD')
