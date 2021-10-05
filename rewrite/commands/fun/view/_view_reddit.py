import aiohttp
import urllib.parse
import random
import io, json
import re

async def c(WS, msg, options):
    if "persist" in options:
        message = msg["message"]
        message["components"] = [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "label": "Loading...",
                        "style": 3,
                        "custom_id": "view",
                        "disabled": True
                    }
                ]
            }
        ]
        await WS.post(WS.interaction(msg), data = WS.form({
            "type": 7,
            "data": message
        }))
        persist = options["persist"]
        match persist["t"]:
            case "subreddit":
                name = f"/r/{persist['n']}/{persist['s']}"
                sort = persist['s']
                search = persist['q']
                url = f"https://reddit.com/r/{persist['n']}/"
                if search:
                    url += f"search.json?q={urllib.parse.quote(search)}&restrict_sr=1&sort={sort}&limit=100"
                else:
                    url += f"{sort}.json?limit=100"
                listing = url.rsplit("/", 1)[0] + "/"
    else:
        await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "embeds": [{
                    "title": "LOADING ;]",
                    "description": "Just a sec...",
                    "color": 0xff8800,
                }],
                "flags": 1 << 6
            }
        }))
        subops = options["options"][0]["options"]
        persist = {"c": "reddit"}
        match options["options"][0]["name"]:
            case "subreddit":
                url = f"https://reddit.com/r/{subops[0]['value']}/"
                listing = url
                if subops[-1]['name'] == 'search':
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
                    url += f"search.json?q={urllib.parse.quote(subops[-1]['value'])}&restrict_sr=1&sort={sort}&limit=100"
                elif subops[-1]['name'] == 'sort':
                    url += f"{subops[-1]['value']}.json?limit=100"
                    sort = subops[-1]['value']
                    search = ""
                else:
                    sort = "new"
                    url += f"new.json?limit=100"
                    search = ""
                name = f"/r/{subops[0]['value']}/{sort}"
                persist['t'] = "subreddit"
                persist['n'] = subops[0]['value']
                persist['s'] = sort
                persist['q'] = search
            case "multireddit":
                pass
            case "redditor":
                pass
            case "link":
                pass

    async with aiohttp.ClientSession() as sess:
        async with sess.get(url) as resp:
            data = await resp.json()
    async with aiohttp.ClientSession() as sess:
        async with sess.get(listing + "about.json") as resp:
            obj = await resp.json()

    post = WS.classify(random.choice(data["data"]["children"])["data"])
    feed = WS.classify(obj["data"])
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
        "color": 0xff8800
    }
    if post.is_self:
        embed["fields"] = [{"name": "Content", "value": post.selftext or "[empty]"}]
        embed["footer"]["text"] = "Text"
    else:
        embed["description"] += f" | [View Link]({post.url})"
        embed["footer"]["text"] = f"Link [{post.domain}]"
        if any(post.url.lower().split("?")[0].endswith(x) for x in [".jpg", ".png", ".jpeg", ".gif"]):
            embed["image"] = {"url": post.url}
        else:
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
    resp = await WS.patch(WS.interaction(msg, 1), data = WS.form({
        "embeds": [embed],
        "flags": 1 << 6,
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "label": "New post",
                        "style": 3,
                        "custom_id": "view|" + str(persist)
                    }
                ]
            }
        ]
    }))
    print(resp)
