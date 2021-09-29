from math import *
from cmath import *
from numpy import *
from numexpr import *
import sympy as sp
from util.parse_math import parse_eq

async def c(WS, msg, options):
    eq = parse_eq(eq)
    try:
        num = round(float(evaluate(eq)), 16)
        if str(num).endswith(".0"):
            num = int(num)
    except ValueError:
        return await WS.post({
            "type": 4,
            "data": {
                "flags": 1 << 6,
                "embeds": [{
                    "title": "ERROR ;[",
                    "description": "Bad value [unknown error]",
                    "color": 0xff0000
                }]
            }
        })
    except SyntaxError as ex:
        return await WS.post({
            "type": 4,
            "data": {
                "flags": 1 << 6,
                "embeds": [{
                    "title": "ERROR ;[",
                    "description": f"Syntax Error: `{ex}`",
                    "color": 0xff0000
                }]
            }
        })
    except ZeroDivisionError:
        return await WS.post({
            "type": 4,
            "data": {
                "flags": 1 << 6,
                "embeds": [{
                    "title": "ERROR ;[",
                    "description": f"You can't divide by 0",
                    "color": 0xff0000
                }]
            }
        })
    except NameError:
        return await WS.post({
            "type": 4,
            "data": {
                "flags": 1 << 6,
                "embeds": [{
                    "title": "ERROR ;[",
                    "description": f"Undefined name error: `{ex}`",
                    "color": 0xff0000
                }]
            }
        })
    else:
        return await WS.post({
            "type": 4,
            "data": {
                "flags": 1 << 6,
                "embeds": [{
                    "title": "CALC ;]",
                    "description": f"{num}",
                    "color": 0x00ff00
                }]
            }
        })
