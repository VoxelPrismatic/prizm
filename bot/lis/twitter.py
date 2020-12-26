import discord
import asyncio
import requests
import html
import aiohttp
import json
from util import dbman
from datetime import datetime
from discord.ext import commands
import threading

boteth = None

auth = {
    'Authorization': 'Bearer <twitter token>'
}

tweet_exts = {
    "expansions": [
        "attachments.poll_ids",
        "attachments.media_keys",
        "author_id",
        "entities.mentions.username",
        "in_reply_to_user_id",
        "referenced_tweets.id",
        "referenced_tweets.id.author_id"
    ],
    "media.fields": [
        "duration_ms",
        "height",
        "media_key",
        "preview_image_url",
        "type",
        "url",
        "width",
        "public_metrics",
    ],
    "poll.fields": [
        "end_datetime",
        "id",
        "options",
        "voting_status"
    ],
    "tweet.fields": [
        "attachments",
        "author_id",
        "context_annotations",
        "conversation_id",
        "created_at",
        "entities",
        "id",
        "in_reply_to_user_id",
        "public_metrics",
        "possibly_sensitive",
        "referenced_tweets",
        "reply_settings",
        "source",
        "text",
        "withheld"
    ],
    "user.fields": [
        "profile_image_url",
        "name",
        "username"
    ]
}

tweet_ext = ""
for thing in tweet_exts:
    tweet_ext += ("&" if tweet_ext else "?") + thing + "=" + ",".join(tweet_exts[thing])


old_tweets = []

def parse_text(tweet):
    text = tweet["text"]
    txt = html.unescape(text)
    parsed = []
    try:
        for mention in tweet["entities"]["mentions"][::-1]:
            if mention in parsed:
                continue
            parsed.append(mention)
            if not text[mention["start"]:mention["end"]].startswith("@"):
                if "#" in text[mention["start"]:]:
                    while not text[mention["start"]:mention["end"]].startswith("@"):
                        mention["start"] += 1
                        mention["end"] += 1
                else:
                    while not text[mention["start"]:mention["end"]].startswith("@"):
                        mention["start"] -= 1
                        mention["end"] -= 1
            txt = txt.replace(text[mention["start"]:mention["end"]], f"[@{mention['username']}](https://twitter.com/{mention['username']})", 1)
    except Exception as ex:
        #input(ex)
        pass #No mentions
    try:
        for hashtag in tweet["entities"]["hashtags"][::-1]:
            if hashtag in parsed:
                continue
            parsed.append(hashtag)
            if not text[hashtag["start"]:hashtag["end"]].startswith("#"):
                if "#" in text[hashtag["start"]:]:
                    while not text[hashtag["start"]:hashtag["end"]].startswith("#"):
                        hashtag["start"] += 1
                        hashtag["end"] += 1
                else:
                    while not text[hashtag["start"]:hashtag["end"]].startswith("#"):
                        hashtag["start"] -= 1
                        hashtag["end"] -= 1
            txt = txt.replace(text[hashtag["start"]:hashtag["end"]], f"[#{hashtag['tag']}](https://twitter.com/hashtag/{hashtag['tag']})", 1)
    except Exception as ex:
        #input(ex)
        pass #No hashtags
    try:
        last_photo == 0
        for url in tweet["entities"]["urls"][::-1]:
            if url in parsed:
                continue
            parsed.append(url)
            if not text[url["start"]:url["end"]].startswith("https://t.co/"):
                if "https://t.co/" in text[url["start"]:]:
                    while not text[url["start"]:url["end"]].startswith("https://t.co/"):
                        url["start"] += 1
                        url["end"] += 1
                else:
                    while not text[url["start"]:url["end"]].startswith("https://t.co/"):
                        url["start"] -= 1
                        url["end"] -= 1
            name = url["display_url"]
            if url["expanded_url"].endswith("/photo/1"):
                last_photo += 1
                name = f"[photo {last_photo}]"
            elif url["expanded_url"].endswith("/photo/2"):
                name = "[photo 2]"
            elif url["expanded_url"].endswith("/photo/3"):
                name = "[photo 3]"
            elif url["expanded_url"].endswith("/photo/4"):
                name = "[photo 4]"
            print()
            txt = txt.replace(text[url["start"]:url["end"]], f"[{name}]({url['url']})", 1)
    except Exception as ex:
        #input(ex)
        pass #No hashtags
    return txt

is_done = True
passed = 0

async def get_json(*a, **kw):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(*a, **kw) as resp:
            return await resp.json()

async def get_usernames(*ids):
    names = {}
    for i in ids:
        try:
            names[i]
        except:
            names[i] = (await get_json(
                f"https://api.twitter.com/2/users/{i}",
                headers = auth
            ))["data"]["username"]
    return names

async def on_tweet(boteth):
    #global is_done
    #if not is_done:
        #return

    #is_done = False

    global old_tweets, passed
    send_to = {}
    for user_id, channel_id in dbman.get("twitter", "user_id", "channel_id", dont_touch = 1):
        try:
            if channel_id not in send_to[user_id]:
                send_to[user_id].append(channel_id)
        except KeyError:
            send_to[user_id] = [channel_id]

    #print("Listening for tweets")
    for tweeter in send_to:
        try:
            data = await get_json(
                f"https://api.twitter.com/1.1/statuses/user_timeline.json?user_id={tweeter}&count=1",
                headers = auth
            )
            #print(old_tweets)
            #print(json.dumps(data, indent = 4))
            tID = data[0]["id"]
            #print(tID)
            while tID not in old_tweets and passed:
                data = await get_json(
                    f"https://api.twitter.com/2/tweets/{tID}" + tweet_ext,
                    headers = auth
                )
                dan = data["includes"]["users"][0]
                embed = discord.Embed()
                print(json.dumps(data, indent = 4))
                embed.timestamp = datetime.fromisoformat(data["data"]["created_at"].split(".")[0])
                embed.color = discord.Color(0x00ffff)
                embed.set_author(
                    name = f"{dan['name']} [@{dan['username']}]",
                    icon_url = f"{dan['profile_image_url']}",
                    url = f"https://twitter.com/{dan['username']}"
                )
                try:
                    references = data["data"]["referenced_tweets"]
                    if references:
                        not_dan = data["includes"]["users"]
                        not_dan = not_dan[min(len(not_dan) - 1, 1)]
                        if references[0]["type"] == "replied_to":
                            embed.add_field(
                                name = f"__{not_dan['name']}__ [@{not_dan['username']}] sent:",
                                value = parse_text(data["includes"]["tweets"][0]) + \
                                    f"\n\n[Link to tweet](https://twitter.com/{not_dan['username']}/status/{references[0]['id']})",
                                inline = False
                            )
                            try:
                                embed.set_thumbnail(
                                    url = data["includes"]["tweets"][0]["urls"][0]["images"][0]["url"]
                                )
                            except:
                                pass
                            embed.add_field(
                                name = f"__{dan['name']}__ [@{dan['username']}] replied:",
                                value = parse_text(data["data"]) + \
                                    f"\n\n[Link to tweet](https://twitter.com/{dan['username']}/status/{data['data']['id']})",
                                inline = False
                            )
                            try:
                                embed.set_image(
                                    url = data["includes"]["media"][0]["url"]
                                )
                            except:
                                pass
                        elif references[0]["type"] == "retweeted":
                            embed.add_field(
                                name = f"__{dan['name']}__ [@{dan['username']}] retweeted from __{not_dan['name']}__ [@{not_dan['username']}]:",
                                value = parse_text(data["includes"]["tweets"][0]) + \
                                    f"\n\n[Link to tweet](https://twitter.com/{not_dan['username']}/status/{data['data']['id']})",
                                inline = False
                            )
                            try:
                                embed.set_image(
                                    url = data["includes"]["tweets"][0]["urls"][0]["images"][0]["url"]
                                )
                            except:
                                pass
                        elif references[0]["type"] == "retweeted":
                            embed.add_field(
                                name = f"__{dan['name']}__ [@{dan['username']}] quoted:",
                                value = parse_text(data["data"]) + \
                                    f"\n\n[Link to tweet](https://twitter.com/{dan['username']}/status/{data['data']['id']})",
                                inline = False
                            )
                            embed.add_field(
                                name = f"__{not_dan['name']}__ [@{not_dan['username']}] quoted:",
                                value = parse_text(data["includes"]["tweets"][0]) + \
                                    f"\n\n[Link to tweet](https://twitter.com/{not_dan['username']}/status/{references[0]['id']})",
                                inline = False
                            )
                        else:
                            input(references)
                    else:
                        raise Exception
                except Exception as ex:
                    #print(ex)
                    embed.add_field(
                        name = f"__{dan['name']}__ [@{dan['username']}] sent:",
                        value = parse_text(data["data"]) + \
                            f"\n\n[Link to tweet](https://twitter.com/{dan['username']}/status/{data['data']['id']})",
                        inline = False
                    )
                    try:
                        embed.set_image(
                            url = data["includes"]["media"][0]["url"]
                        )
                    except:
                        pass
                #embed.description = text

                #print(json.dumps(embed.to_dict(), indent = 4))

                for channel in send_to[tweeter]:
                    try:
                        await boteth.get_channel(channel).send(embed = embed)
                    except Exception as ex:
                        print(ex)
                    pass
                #exit()
                old_tweets.append(tID)
                data = await get_json(
                    f"https://api.twitter.com/1.1/statuses/user_timeline.json?user_id={tweeter}&count=1&max_id={tID}",
                    headers = auth
                )
                tID = data[0]["id"]
            old_tweets.append(tID)
        except Exception as ex:
            raise ex
    passed = 1



##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
#def setup(bot):
    #global boteth
    #boteth = bot
    #print('+LIS')
    ##bot.add_listener(on_tweet, "on_message")
    #timer = threading.Timer(1, (lambda: asyncio.run(on_tweet())))
    #timer.start()
    #print('GOOD')

#def teardown(bot):
    #print('-LIS')
    #global boteth
    #boteth = bot
    ##bot.remove_listener("on_tweet", "on_message")
    #is_done = True
    #print('GOOD')
