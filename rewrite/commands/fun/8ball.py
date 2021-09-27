import random

info = {
    "name": "8ball",
    "type": 1,
    "description": "The most accurate and logical way to make choices",
    "id": "8ball",
    "options": [
        {
            "name": "question",
            "description": "Question",
            "type": 3,
            "required": True
        }
    ]
}

async def command(WS, msg):
    return await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4 if "message" not in list(msg) else 7,
        "data": {
            "content": random.choice([
                'As I see it, yee',
                'Ask again later',
                'I shouldn\'t tell you',
                'Woops, I forgot what I was going to say',
                'Concentrate on your answer, and I\'ll repeat it',
                'Don\'t count on it mate',
                'Certainly',
                'Probably',
                'Most likely',
                'Maybe',
                'I say no',
                'My [1] source[s] say no',
                'Seems good',
                'Seems not so good',
                'I didn\'t care to answer this time, try again',
                'I doubt it and I\'m a downer',
                'With many or none doubts',
                'Yee fam',
                'Yeet!',
                'Boi you can believe it',
                'Bruh why are you asking a silly 8ball command'
            ]),
            "flags": 1 << 6,
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "Roll again",
                            "style": 2,
                            "custom_id": "8ball"
                        }
                    ]
                }
            ]
        }
    }))
