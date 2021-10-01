import re

def to_super(thing):
    thing = thing.replace("1", "\N{SUPERSCRIPT ONE}")
    thing = thing.replace("2", "\N{SUPERSCRIPT TWO}")
    thing = thing.replace("3", "\N{SUPERSCRIPT THREE}")
    thing = thing.replace("4", "\N{SUPERSCRIPT FOUR}")
    thing = thing.replace("5", "\N{SUPERSCRIPT FIVE}")
    thing = thing.replace("6", "\N{SUPERSCRIPT SIX}")
    thing = thing.replace("7", "\N{SUPERSCRIPT SEVEN}")
    thing = thing.replace("8", "\N{SUPERSCRIPT EIGHT}")
    thing = thing.replace("9", "\N{SUPERSCRIPT NINE}")
    thing = thing.replace("0", "\N{SUPERSCRIPT ZERO}")
    return thing

def to_sub(thing):
    thing = thing.replace("1", "\N{SUBSCRIPT ONE}")
    thing = thing.replace("2", "\N{SUBSCRIPT TWO}")
    thing = thing.replace("3", "\N{SUBSCRIPT THREE}")
    thing = thing.replace("4", "\N{SUBSCRIPT FOUR}")
    thing = thing.replace("5", "\N{SUBSCRIPT FIVE}")
    thing = thing.replace("6", "\N{SUBSCRIPT SIX}")
    thing = thing.replace("7", "\N{SUBSCRIPT SEVEN}")
    thing = thing.replace("8", "\N{SUBSCRIPT EIGHT}")
    thing = thing.replace("9", "\N{SUBSCRIPT NINE}")
    thing = thing.replace("0", "\N{SUBSCRIPT ZERO}")
    return thing

parser = {
    r"a((sin|cos|tan|sec|csc|cot)h?)": r"arc\1",
    r"(\d+)root\((.+?)\)": r"(\2)^(1/\1)",
    r"logbase(\d+)\((.+?)\)": r"log(\2, \1)",
    r"((tan|cos|sin|cot|csc|sec)h?)(\*\*)?-1\((.+?)\)": r"arc\1(\4)",
    r"cot\((.+?)\)": r"(1/tan(\1))",
    r"csc\((.+?)\)": r"(1/sin(\1))",
    r"sec\((.+?)\)": r"(1/cos(\1))",
    r"coth\((.+?)\)": r"(1/tanh(\1))",
    r"csch\((.+?)\)": r"(1/sinh(\1))",
    r"sech\((.+?)\)": r"(1/cosh(\1))",
    r"arccot\((.+?)\)": r"arctan(1/(\1))",
    r"arccsc\((.+?)\)": r"arcsin(1/(\1))",
    r"arcsec\((.+?)\)": r"arccos(1/(\1))",
    r"arccoth\((.+?)\)": r"arctanh(1/(\1))",
    r"arccsch\((.+?)\)": r"arcsinh(1/(\1))",
    r"arcsech\((.+?)\)": r"arccosh(1/(\1))",
    
    r"\|(.+?)\|": r"(abs(\1))",
    r"\[(.+?)\]": r"(floor(\1))",
    r"(\d+)([xy\(])": r"\1*\2",
    r"([xy\)])(\d+)": r"\1*\2",
    r"^[xy]=": "",
    r"=[xy]$": "",
    r"([xy\d])\(": r"\1*(",
    r"\)([xy\d])": r")*\1",
    r"(\d+)i": r"\1j",
    r"([xy])i": r"\1*1j",
    r"([\*\+\-\^\/ ])i ?": r"\1 1j",
    r"\)i": r")*1j",
    r"i\(": r"1j*(",
    r"pi([\dxy])": r"3.141592653*\1",
    r"([\dxy])pi": r"\1*3.141592653",
    r"([\*\+\-\^\/ ])pi": r"\1 3.1415926535",
    r"pi([\*\+\-\^\/ ])": r"3.1415926535 \1",
    r"\)pi": r")*3.1415926535",
    r"pi\(": r"3.1415926535*(",
    r"e([\dxy])": r"2.718281828*\1",
    r"([\dxy])e": r"\1*2.718281828",
    r"([\*\+\-\^\/ ])e": r"\1 2.718281828",
    r"e([\*\+\-\^\/ ])": r"2.718281828 \1",
    r"\)e": r")*2.718281828",
    r"e\(": r"2.718281828*(",
}

unparser = {
    r"3\.1415926535\d*": "pi",
    r"2\.718281828\d*": "e",
    r"(\d)j": r"\1i",
    r"log\((.+?), (\d+)\)": (lambda m: "log" + to_sub(m[2]) + "(" + m[1] + ")"),
    r"\((.+?)\)\^\(1/(\d+)\)": (lambda m: to_super(m[2]) + "\u221a(" + m[1] + ")"),
    r"\(1/tan\((.+?)\)\)": r"cot(\1)",
    r"\(1/cos\((.+?)\)\)": r"sec(\1)",
    r"\(1/sin\((.+?)\)\)": r"csc(\1)",
    r"\(1/tanh\((.+?)\)\)": r"coth(\1)",
    r"\(1/cosh\((.+?)\)\)": r"sech(\1)",
    r"\(1/sinh\((.+?)\)\)": r"csch(\1)",
    r"arctan\(1/\((.+?)\)\)": r"arccot(\1)",
    r"arccos\(1/\((.+?)\)\)": r"arcsec(\1)",
    r"arcsin\(1/\((.+?)\)\)": r"arccsc(\1)",
    r"arctanh\(1/\((.+?)\)\)": r"arccoth(\1)",
    r"arccosh\(1/\((.+?)\)\)": r"arcsech(\1)",
    r"arcsinh\(1/\((.+?)\)\)": r"arccsch(\1)",
}

def parse_eq(eq, radians = False):
    eq = eq.replace('^','**').lower().strip()
    for r in parser:
        eq = re.sub(r, parser[r], eq)
    s = list(re.finditer(f"((arc)?(sin|cos|tan|sec|csc|cot)h?)\((.+?)\)", eq))
    if s and not radians:
        for match in s:
            func, arc, a, arg = match.group()
            if not arc:
                eq = eq[:match.start()] + f"{func}(({arg})*3.1415926535/180)" + eq[match.end():]
                s = list(re.finditer(f"((arc)?(sin|cos|tan|sec|csc|cot)h?)\((.+?)\)", eq))
    elif not s and radians:
        for match in s:
            func, arc, a, arg = match.group()
            if not arc:
                eq = eq[:match.start()] + f"{func}(({arg})*180/3.1415926535)" + eq[match.end():]
                s = list(re.finditer(f"((arc)?(sin|cos|tan|sec|csc|cot)h?)\((.+?)\)", eq))
            
    return eq

def unparse_eq(eq):
    eq = eq.replace('**','^').lower().strip()
    for r in unparser:
        eq = re.sub(r, unparser[r], eq)
    return eq
