import aiohttp
import urllib.parse
import random
import io, json
import re
import datetime
import time

CHOICES_SORT = [
    {
        "name": "new",
        "value": "new"
    },
    {
        "name": "hot",
        "value": "hot"
    },
    {
        "name": "top-hour",
        "value": "top-hour"
    },
    {
        "name": "top-day",
        "value": "top-day"
    },
    {
        "name": "top-week",
        "value": "top-week"
    },
    {
        "name": "top-month",
        "value": "top-month"
    },
    {
        "name": "top-year",
        "value": "top-year"
    },
    {
        "name": "top-all",
        "value": "top-all"
    },
    {
        "name": "rising",
        "value": "rising"
    },
    {
        "name": "controversial",
        "value": "controversial"
    }
]

info = {
    "name": "reddit",
    "description": "View a reddit post, or make a live feed",
    "type": 1,
    "id": "reddit",
    "options": [
        {
            "name": "sub",
            "type": 1,
            "description": "View a random post from a subreddit",
            "options": [
                {
                    "name": "name",
                    "description": "Subreddit name",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "sort",
                    "description": "How to sort your listing",
                    "type": 3,
                    "required": False,
                    "choices": CHOICES_SORT
                },
                {
                    "name": "search",
                    "description": "Optional search",
                    "type": 3,
                    "required": False
                }
            ]
        },
        {
            "name": "multi",
            "type": 1,
            "description": "View a random post from a multireddit",
            "options": [
                {
                    "name": "name",
                    "description": "Multireddit name",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "redditor",
                    "description": "Redditor who made this multireddit",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "sort",
                    "description": "How to sort your listing",
                    "type": 3,
                    "required": False,
                    "choices": CHOICES_SORT
                },
                {
                    "name": "search",
                    "description": "Optional search",
                    "type": 3,
                    "required": False
                }
            ]
        },
        {
            "name": "user",
            "type": 1,
            "description": "View a random post from a redditor",
            "options": [
                {
                    "name": "name",
                    "description": "Redditor name",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "sort",
                    "description": "How to sort your listing",
                    "type": 3,
                    "required": False,
                    "choices": CHOICES_SORT
                },
                {
                    "name": "search",
                    "description": "Optional search",
                    "type": 3,
                    "required": False
                }
            ]
        },
        {
            "name": "link",
            "type": 1,
            "description": "Post the link in the PRIZM style ;]",
            "options": [
                {
                    "name": "url",
                    "description": "link to the post",
                    "type": 3,
                    "required": True
                }
            ]
        },
    ]
}

async def command(WS, msg):
    if "message" in msg:
        options = {"persist": eval(msg['message']['components'][0]['components'][0]['custom_id'].split('|',1)[-1].strip("|"))}
        direction = msg['data']['custom_id'].split("|")[1][0]
        if direction in "<>":
            message = msg["message"]
            persist = options["persist"]
            old_components = message["components"]
            message["components"] = [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "Loading...",
                            "style": 3,
                            "custom_id": "reddit|" + json.dumps(persist)
                        }
                    ]
                }
            ]
            await WS.post(WS.interaction(msg), data = WS.form({
                "type": 7,
                "data": message
            }))
            print(f"https://reddit.com/by_id/t3_{msg['data']['custom_id'].split('/')[-1]}/.json")
            data = await WS.get(f"https://reddit.com/by_id/t3_{msg['data']['custom_id'].split('/')[-1]}/.json")
            post = WS.classify(data["data"]["children"][0]["data"])
            img = post.gallery_data.items
            i = persist["i"]
            if direction == "<":
                i -= 1
                if i == -1: i = len(img) - 1
            else:
                i += 1
                if i == len(img): i = 0
            print(i)
            persist["i"] = i
            embed = message["embeds"][0]
            old_components[0]["components"][0]["custom_id"] = "reddit|" + json.dumps(persist)
            embed["footer"]["text"] = f"Gallery [{i+1}/{len(post.gallery_data.items)}]"
            embed["image"] = {"url": post.media_metadata[img[i].media_id].o[0].u.split("?")[0].replace("/preview.", "/i.")}
            embed["footer"]["text"] += f" | {'+' if post.score > 0 else '-'}{post.score}"
            if post.edited:
                embed["footer"]["text"] += " | Edited"
            if post.over_18:
                embed["footer"]["text"] += " | NSFW"
            if post.spoiler:
                embed["footer"]["text"] += " | Spoiler"
            if post.locked:
                embed["footer"]["text"] += " | Locked"
            #embed["timestamp"] =
            embed["footer"]["text"] += f" | [{post.link_flair_text or 'No Flair'}]"
            print(embed)
            resp = await WS.patch(WS.interaction(msg, 1), data = WS.form({
                "embeds": [embed],
                "components": old_components
            }))
            return

    else:
        options = msg["data"]["options"][0]
    skipit = False
    url = ""
    name = ""
    listing = ""
    data = []

    if "persist" in options:
        persist = options["persist"]
        message = msg["message"]
        message["components"] = [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "label": "Loading...",
                        "style": 3,
                        "custom_id": "reddit|" + json.dumps(persist)
                    }
                ]
            }
        ]
        await WS.post(WS.interaction(msg), data = WS.form({
            "type": 7,
            "data": message
        }))
        match persist["t"]:
            case "s":
                name = f"/r/{persist['n']}/{persist['s']}"
                url = f"https://reddit.com/r/{persist['n']}/"
                listing = url
            case "m":
                name = f"/u/{persist['u']}/m/{persist['n']}/{persist['s']}"
                url = f"https://reddit.com/user/{persist['u']}/m/{persist['n']}/"
                listing = url
            case "u":
                name = f"/user/{persist['n']}/{persist['s']}"
                url = f"https://reddit.com/user/{persist['n']}/submitted/"
                listing = f"https://reddit.com/user/{persist['n']}/"
            case "l":
                name = f"/r/{persist['n']}/{persist['l']}"
                url = f"https://reddit.com/by_id/t3_{persist['l']}/.json"
                listing = f"https://reddit.com/r/{persist['n']}/"
                skipit = True
        if skipit:
            search = sort = ""
        elif persist['q']:
            search, sort = persist['q'], persist['s']
            url += f"search.json?q={urllib.parse.quote(search)}&restrict_sr=1&sort={sort.split('-')[-1]}&limit=100&include_over_18=on"
        else:
            search, sort = persist['q'], persist['s']
            url += f"{sort.split('-')[0]}.json?limit=100"
            if "-" in sort:
                url += "&sort=" + sort.split("-")[1]
    else:
        await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "embeds": [{
                    "title": "LOADING ;]",
                    "description": "Just a sec...",
                    "color": 0xff8800,
                }]
            }
        }))
        subops = options["options"]
        persist = {"t": options["name"][0]}
        if options["name"] == "link":
            pass
        elif subops[-1]['name'] == 'search':
            if subops[1]['name'] == 'sort':
                match subops[1]['value']:
                    case "new" | "hot":
                        sort = subops[1]["value"]
                    case "top-hour" | "top-day" | "top-week" | "top-month" | "top-year" | "top-all":
                        sort = "top"
                    case "rising":
                        sort = "comments"
                    case _:
                        sort = "relevance"
            else:
                sort = "relevance"
            search = subops[-1]["value"]
            persist["s"] = sort
            persist["q"] = search
        elif subops[-1]['name'] == 'sort':
            sort = subops[-1]['value']
            url += f"{sort.split('-')[0]}.json?limit=100"
            if "-" in sort:
                url += "&sort=" + sort.split("-")[1]
            search = ""
            persist["s"] = sort
            persist["q"] = search
        else:
            sort = "new"
            search = ""
            persist["s"] = sort
            persist["q"] = search

        match options["name"]:
            case "sub":
                url = f"https://reddit.com/r/{subops[0]['value']}/"
                listing = url
                name = f"/r/{subops[0]['value']}/{sort}"
                persist["n"] = subops[0]['value']
            case "multi":
                url = f"https://reddit.com/user/{subops[1]['value']}/m/{subops[0]['value']}/"
                listing = url
                name = f"/u/{subops[1]['value']}/m/{subops[0]['value']}/{sort}"
                persist["n"] = subops[0]['value']
                persist["u"] = subops[1]['value']
            case "user":
                url = f"https://reddit.com/user/{subops[0]['value']}/submitted/"
                listing = f"https://reddit.com/user/{subops[0]['value']}/"
                name = f"/u/{subops[0]['value']}/{sort}"
                persist["n"] = subops[0]['value']
            case "link":
                t3 = subops[0]['value'].split("/comments/")[-1].split("redd.it/")[-1].split("/gallery/")[-1].split("/")[0]
                url = f"https://reddit.com/by_id/t3_{t3}/.json"
                data = (await WS.get(url))["data"]["children"][0]["data"]
                listing = f"https://reddit.com/r/{data['subreddit']}/"
                skipit = True
                name = f"/r/{data['subreddit']}/{t3}"
                persist["n"] = data["subreddit"]
                persist["l"] = t3
                search = ""
                sort = "link"
            case _:
                print(options)
        if skipit:
            pass
        elif persist['q']:
            url += f"search.json?q={urllib.parse.quote(subops[-1]['value'])}&restrict_sr=1&sort={sort}&limit=100&include_over_18=on"
        else:
            url += f"new.json?limit=100"


    if name not in WS.cache.persist:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                data = await resp.json()
            async with sess.get(listing + "about.json") as resp:
                obj = await resp.json()
                if "data" not in obj:
                    obj["data"] = {
                        "over18": False,
                        "icon_img": "https://www.redditstatic.com/custom_feeds/custom_feed_default_7.png",
                    }
        WS.cache.persist[name] = {
            "time": time.time(),
            "data": data["data"]["children"],
            "obj": WS.classify(obj["data"]),
            "after": data["data"]["after"]
        }
    elif len(WS.cache.persist[name]["data"]) < 500 and WS.cache.persist[name]["after"]:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url + "&after=" + WS.cache.persist[name]["after"]) as resp:
                data = await resp.json()
        WS.cache.persist[name]["after"] = data["data"]["after"]
        WS.cache.persist[name]["data"] += data["data"]["children"]

    WS.cache.persist[name]["time"] = time.time()
    data = WS.cache.persist[name]["data"]
    feed = WS.cache.persist[name]["obj"]

    if "guild_id" not in msg or not WS.cache.guilds[msg['guild_id']]("channels", id = msg["channel_id"]).nsfw:
        if feed.over18 or all(p["data"]["over_18"] for p in data):
            return await WS.patch(WS.interaction(msg, 1), data = WS.form({
                "embeds": [{
                    "title": "NOPE ;[",
                    "description": "This is an NSFW subreddit, which is not allowed here.",
                    "footer": {"text": f"If you wish to view {name}, make sure you are in an NSFW channel."},
                    "color": 0xff0000
                }]
            }))

        n = random.randint(0, len(data))
        while data[n]["data"]["over_18"]:
            del data[n]
            n = random.randint(0, len(data))
        post = WS.classify(data[n]["data"])
    else:
        post = WS.classify(random.choice(data)["data"])

    embed = {
        "author": {
            "name": f"{name} " + (f"'{search}' " if search else ''),
            "icon_url": feed.icon_img or feed.community_icon or "https://styles.redditmedia.com/t5_6/styles/communityIcon_a8uzjit9bwr21.png",
            "url": listing
        },
        "title": post.title[:256],
        "description": f"[Open Post](https://redd.it/{post.name[3:]})",
        "footer": {
            "text": f"",
            "icon_url": "https://cdn.discordapp.com/avatars/845317680722739220/e05cb529ac4af465ac0e528e13c600a9.png?size=256"
        },
        "color": 0xff8800,
        "timestamp": datetime.datetime.utcfromtimestamp(post.created_utc).isoformat()
    }

    components = [
        {
            "type": 2,
            "label": "New post" if persist['t'] != 'l' else "Refresh",
            "style": 3,
            "custom_id": "reddit|" + json.dumps(persist)
        }
    ]

    if post.is_self:
        embed["fields"] = [{"name": "Content", "value": post.selftext[:1024] or "[empty]"}]
        embed["footer"]["text"] = "Text"
    else:
        embed["description"] += f" | [View Link]({post.url})"
        embed["footer"]["text"] = f"Link [{post.domain}]"
        if any(post.url.lower().split("?")[0].endswith(x) for x in [".jpg", ".png", ".jpeg", ".gif"]):
            embed["image"] = {"url": post.url}
            embed["footer"]["text"] = f"Image [{post.domain}]"
        elif "gallery_data" in post:
            persist['i'] = 0
            print("\x1b[91;1m", post, "\x1b[0m")
            img = post.gallery_data.items[0]
            img = img.media_id
            embed["footer"]["text"] = f"Gallery [1/{len(post.gallery_data.items)}]"
            embed["image"] = {"url": post.media_metadata[img].o[0].u.split("?")[0].replace("/preview.", "/i.")}
            custom = post.name[3:] + f"/{post.name[3:]}"
            components[0]["custom_id"] = "reddit|" + json.dumps(persist)
            components += [
                {
                    "type": 2,
                    "label": "<",
                    "style": 3,
                    "custom_id": "reddit|<" + custom
                },
                {
                    "type": 2,
                    "label": ">",
                    "style": 3,
                    "custom_id": "reddit|>" + custom
                }
            ]
        elif post.thumbnail:
            embed["image"] = {"url": post.thumbnail}
    embed["footer"]["text"] += f" | {'+' if post.score > 0 else '-'}{post.score}"
    if post.edited:
        embed["footer"]["text"] += " | Edited"
    if post.over_18:
        embed["footer"]["text"] += " | NSFW"
    if post.spoiler:
        embed["footer"]["text"] += " | Spoiler"
    if post.locked:
        embed["footer"]["text"] += " | Locked"
    #embed["timestamp"] =
    embed["footer"]["text"] += f" | [{post.link_flair_text or 'No Flair'}]"
    print(embed)
    resp = await WS.patch(WS.interaction(msg, 1), data = WS.form({
        "embeds": [embed],
        "flags": 1 << 6,
        "components": [
            {
                "type": 1,
                "components": components
            }
        ]
    }))
    print(resp)
