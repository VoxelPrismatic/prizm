import datetime

info = {
    "name": "snowflake",
    "type": 1,
    "description": "Gives you the time information from a given ID",
    "id": "snowflake",
    "options": [
        {
            "name": "id",
            "description": "ID from a channel, message, role, etc",
            "type": 3,
            "required": True
        }
    ]
}

async def command(WS, msg):
    options = msg["data"]["options"][0]["value"]
    try:
        snow = int(options)
        if len(options) < 17 or len(options) > 19:
            raise Exception
    except:
        return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "ERROR ;[",
                        "description": f"The provided snowflake, `{options}`, is not a valid snowflake",
                        "color": 0xff0000,
                        "timestamp": WS.NOW
                    }
                ],
                "flags": 1 << 6
            }
        }))
    t = int(((snow >> 22) + 1420070400000)/1000)
    snow_time = datetime.datetime.utcfromtimestamp(t)
    now_time = datetime.datetime.utcnow()

    seconds = int((now_time - snow_time).total_seconds())
    minutes = int(seconds / 60)
    seconds %= 60
    hours = int(minutes / 60)
    minutes %= 60
    days = int(hours / 24)
    hours %= 24
    months = int(days / 30)
    days %= 30
    years = int(months / 12)
    months %= 12

    diff = []
    if years:
        diff.append(f"{years} year{'s' if years != 1 else ''}")
    if months:
        diff.append(f"{months} month{'s' if months != 1 else ''}")
    if days:
        diff.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:
        diff.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        diff.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds:
        diff.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    diff = ", ".join(diff)
    utc = snow_time.strftime('%Y-%m-%dT%H:%M:%S UTC')

    return await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "content": "",
            "embeds": [
                {
                    "title": "SNOWFLAKE ;]",
                    "fields": [
                        {
                            "name": "AGE",
                            "value": f"<t:{t}:R>\n{diff} old",
                            "inline": False
                        },
                        {
                            "name": "DATE",
                            "value": f"<t:{t}:F>\n`{utc}`",
                            "inline": False
                        }
                    ]
                }
            ],
            "flags": 1 << 6
        }
    }))


