import json

def refresh():
    """
    >>> PROVIDES EASY EXTENSION LOADING <<<
    RETURNS - 2 LISTS
    """

    coms = json.loads(open("dyn/refresh.json").read())

    cat = [
        "own",
        "mod",
        "inf",
        "pub",
        "dis",
        "math",
        "int",
        "oth",
        "music",
        "listen"
    ]

    allext = []
    lodtxt = []
    for x in cat:
        allext.append(coms[x])
        if x != "listen":
            lodtxt.append(f"com.{x}.")
        else:
            lodtxt.append("lis.")

    return allext, lodtxt
