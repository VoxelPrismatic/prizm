import sympy
from util import parse_math

def casing(match):
    return f"{parse_math.to_super(match.group(2))}√({int(match.group(0))**int(match.group(1))})"

async def c(WS, msg, options):
    solved = sympy.nsimplify(f"root({options['options'][1]['value']}, {options['options'][0]['value']})")
    solved = re.sub(r"sqrt\((.+?)\)", r"\1**(1/2)", solved)
    solved = re.sub(r"(.+?)**\((.+?)/(.+?)\)", casing, solved)
    await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "content": solved.replace("**", "^"),
            "flags": 1 << 6
        }
    }))
