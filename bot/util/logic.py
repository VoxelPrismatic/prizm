#module "logic"

def XOR(a: bool, b: bool):
    return a != b

def NOR(a: bool, b: bool):
    return not (a or b)

def XNOR(a: bool, b: bool):
    return not xor(a, b)

def NAND(a: bool, b: bool):
    return not (a and b)

def NOT(a: bool):
    return not a

def AND(a: bool, b: bool):
    return a and b

def OR(a: bool, b: bool):
    return a or b

def FLIP(a: bool):
    return not a

def mAND(*bools: bool):
    return all(bools)

def mOR(*bools: bool):
    return any(bools)

def mNAND(*bools: bool):
    return not all(bools)

def mNOR(*bools: bool):
    return not any(bools)

def mXOR(*bools: bool):
    return any(bools) != all(bools)

def mXNOR(*bools: bool):
    return not mXOR(*bools)

def mFLIP(*bools: bool):
    return [not bl for bl in bools]

def mNOT(*bools: bool):
    return [not bl for bl in bools]

def bPLUS(*bools: bool, how: int = 1):
    ls = list(f"{int(''.join(bools), 2)+how:b}")
    while len(ls) > len(bools):
        ls = ls[1:]
    return ls

def bMINUS(*bools: bool, how: int = 1):
    ls = list(f"{int(''.join(bools), 2)-how:b}")
    while len(ls) > len(bools):
        ls = ls[1:]
    return ls
