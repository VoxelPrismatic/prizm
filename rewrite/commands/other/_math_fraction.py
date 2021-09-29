import math

async def c(WS, msg, options):
    a, b = options["options"][0]["value"], options["options"][1]["value"]
    try:
        a = int(a)
    except:
        return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "flags": 1 << 6,
                "embeds": [{
                    "title": "ERROR ;[",
                    "description": "`{a}` is not a whole number",
                    "color": 0xff0000
                }]
            }
        }))
    try:
        b = int(b)
    except:
        return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "flags": 1 << 6,
                "embeds": [{
                    "title": "ERROR ;[",
                    "description": "`{b}` is not a whole number",
                    "color": 0xff0000
                }]
            }
        }))
    c = math.gcd(a, b)
    return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "flags": 1 << 6,
                "embeds": [{
                    "title": "FRACTIONS ;]",
                    "description": "**{a/c:.0f}** / **{b/c:.0f}**",
                    "color": 0x00ff00
                }]
            }
        }))
