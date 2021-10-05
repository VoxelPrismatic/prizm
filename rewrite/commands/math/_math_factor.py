async def c(WS, msg, options):
    n = options["options"][0]["value"]
    m = n
    all_factors = []
    prime_factors = []

    for i in range(1, n + 1):
        if n % i == 0:
            all_factors.append(str(i))

    while n > 1:
        for i in range(1, n + 1):
            if n % i:
                prime_factors.append(str(i))
                n //= i

    await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "embeds": [{
                "title": f"{m}'s factors",
                "fields": [
                    {
                        "name": "All factors",
                        "value": ", ".join(all_factors),
                        "inline": False
                    },
                    {
                        "name": "Prime factors",
                        "value": ", ".join(prime_factors),
                        "inline": False
                    }
                ],
                "color": 0x00ff00
            }],
            "flags": 1 << 6
        }
    }))

