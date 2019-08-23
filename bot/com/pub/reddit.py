#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, random, typing
import praw
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.prawUser import usr
from util.embedify import embedify

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = ["rd"],
                  help='fun',
                  brief='Gives you a random post from a given {subreddit}',
                  usage=';]reddit {?subreddit} {?search}',
                  description='''SUBREDDIT [STR] - The name of the subreddit, /r/ not needed
                - /u/ is required to redditor feeds
                - also can be a link to a submission
SEARCH    [STR] - What to search for''')
@commands.check(enbl)
async def reddit(ctx, subreddit:str, *, search = ''):
    async with ctx.channel.typing():
        red = usr()
    if 'http' in subreddit:
        sbn = red.submission(id=red.submission.id_from_url(subreddit))
    else:
        sbd = None
        for pre in ['/r/','r/','/u/','u/']:
            async with ctx.channel.typing():
                pass
            if sbd:
                continue
            if 'r/' in pre: 
                sbd = red.subreddit(subreddit.replace(pre,''))
                isRedditor = False
            elif 'u/' in pre:
                sbd = red.redditor(subreddit.replace(pre,''))
                isRedditor = True
            try: 
                ls = list(sbd.new(limit=1))
                break
            except:
                sbd = None
                isRedditor = False
        if not sbd:
            sbd = red.subreddit(subreddit)
            isRedditor = False
        else:
            isRedditor = True
        if not isRedditor and sbd.over18 and not ctx.channel.is_nsfw():
            return await ctx.send('```diff\n-] NSFW SUBREDDITS ARE NOT ALLOWED IN NON NSFW CHANNELS```')
        async with ctx.channel.typing():
            pass
        if search and not isRedditor:
            sbd = list(sbd.search(search, limit=500))
        else:
            sort = random.choice(['new','hot','top','controversial'] + (['rising'] if isRedditor else []))
            sbd = list(eval('sbd.'+sort+'(limit=500)'))
        sbn = random.choice(sbd)
        while (sbn.over_18 and not ctx.channel.is_nsfw()) or sbn == None:
            sbn = random.choice(sbd)
    txt = sbn.selftext.replace('>!','||').replace('!<','||')
    await ctx.send(embed=embedify(title='REDDIT ;]',
                      desc=f'''```md
#] /r/{sbn.subreddit.display_name} - /u/{sbn.author.name}
{sbn.title}
>  Flair: [{sbn.link_flair_text}]
>  {sbn.score} upvote{'s' if sbn.score != 1 else ''} - {sbn.upvote_ratio*100:.2f}%
>  Is {'' if sbn.locked else 'not '}archived
>  Is {'' if sbn.stickied else 'not '}pinned
>  Has {'' if sbn.edited else 'not '}been edited
>  Is {'not ' if sbn.is_self else ''}a link/video/image post
>  Is {'' if sbn.spoiler else 'not '}a spoiler
>  SOURCE: {sbn.url[sbn.url.find('//')+2: sbn.url.find('/', sbn.url.find('//')+2)]} ```
[[PERMALINK]]({sbn.shortlink}) [[LINK]]({sbn.url})''',
img = sbn.url if not sbn.is_self else None,
fields = [['CONTENT', txt if len(txt) < 1022 else txt[:1022]+'...', False]] if sbn.is_self else []))

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