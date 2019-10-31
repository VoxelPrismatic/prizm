def iter_range(iterable, vars = 1):
    ls = []
    for x in range(0, len(iterable), vars):
        ls.append(tuple([iterable[x+y] for y in range(vars)]))
    return ls

def pinger(itm):
    if type(itm) == discord.Member:
        return f"<@{itm.id}>"
    if type(itm) == discord.Role:
        return f"<@&{itm.id}>"
    if type(itm) == discord.TextChannel:
        return f"<#{itm.id}>"
    return itm.id

def pager(ls: list, ln: int, *char: list, head = "", foot = "", attr = "", joiner = ", "):
    rtn = []
    lit = []
    if not len(char): char = [("", "ANY")]
    if attr: attr = '.'+attr
    for it in ls:
        itm = eval(it+attr)
        if len(f"{head}{joiner.join(rtn)}, X{itm}{foot}") > ln:
            lit.append(head + joiner.join(rtn))
        for ch, tp in char:
            if type(itm) == tp or tp.upper() == "ANY":
                rtn.append(f"{ch}{itm}")
                break
    if len(rtn):
        lit.append(head + ', '.join(rtn) + foot)
    return lit

def str_case(itm, fl, tr = ''):
    if itm:
        return tr if tr else str(itm)
    return fl

def ifstr(*a, **kw): return str_case(*a, **kw)

def wrap(text, max_len: int = 1500):
    ls = []
    st = ""
    for word in text.split(' '):
        if len(st+word) > max_len:
            ls.append(st)
        st += " "+word.strip()
    if st: ls.append(st)
    return ls
