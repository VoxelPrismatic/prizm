import math
from sympy.simplify.simplify import nsimplify
from numexpr import evaluate

async def c(WS, msg, options):
    A = float(options["options"][0]["value"])
    B = float(options["options"][1]["value"])
    C = float(options["options"][2]["value"])

    # Get other shit
    root = str(nsimplify(f'sqrt({B**2}-4*{A}*{C})'))
    imaginary, K, D = False, 1, 1

    # Get imaginary
    if '*I' in root:
        root, imaginary = root.replace('*I', ''), True

    # Other formatting
    if '*' not in root and 'sqrt(' not in root:
        K, D = float(eval(root)), 1
    elif '*' not in root and 'sqrt(' in root:
        K, D = 1, float(eval(root))
    else:
        K, D = int(root.split('*')[0]), float(eval(root))
    if imaginary:
        K = K*1j

    sol1 = round(float(evaluate(f"({-B}+{K}*sqrt({D}))/(2*{A})")), 8)
    sol2 = round(float(evaluate(f"({-B}-{K}*sqrt({D}))/(2*{A})")), 8)
    K = round(K, 8)
    A = round(A, 8)
    B = round(B, 8)
    C / round(C, 8)
    D = round(D, 8)

    resp = await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "flags": 1 << 6,
            "embeds": [{
                "fields": [{
                    "name": "FORMULA",
                    "value": f"__{-B} ± {K}√{D}__\n{2*A}",
                    "inline": False
                }, {
                    "name": "SOLUTION 1",
                    "value": f"{sol1}",
                    "inline": True
                }, {
                    "name": "SOLUTION 2",
                    "value": f"{sol2}",
                    "inline": True
                }],
                "color": 0x00ff00
            }]
        }
    }))
    print(resp)

