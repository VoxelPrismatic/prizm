from . import _view_reddit

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
    "name": "view",
    "description": "Views a reddit or twitter post",
    "type": 1,
    "id": "view",
    "options": [
        {
            "name": "reddit",
            "description": "View a reddit post",
            "type": 2,
            "options": [
                {
                    "name": "subreddit",
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
                    "name": "multireddit",
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
                    "name": "redditor",
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
        },
        {
            "name": "twitter",
            "description": "View a twitter thread",
            "type": 1,
            "options": [
                {
                    "name": "account",
                    "description": "View the most recent post from an account",
                    "type": 3,
                    "required": False
                },
                {
                    "name": "link",
                    "description": "View a twitter thread, because Discord doesn't embed nicely",
                    "type": 3,
                    "required": False
                },
                {
                    "name": "list",
                    "description": "View the most recent post from a list",
                    "type": 3,
                    "required": False
                }
            ]
        }
    ]
}

extras = [
    _view_reddit
]

async def command(WS, msg):
    if "message" in msg:
        options = {"persist": eval(msg['data']['custom_id'].split('|',1)[-1])}
        options["name"] = options["persist"]["c"]
    else:
        options = msg["data"]["options"][0]

    match options["name"]:
        case "reddit":
            await _view_reddit.c(WS, msg, options)
        case "twitter":
            await _view_twitter.c(WS, msg, options)
