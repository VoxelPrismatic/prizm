#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
import random
from util.embedify import embedify
import io
import re
import time

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["brainfuck", "prizfuck"],
                  help = 'pub',
                  brief = 'PrizFuck, the better BrainFuck',
                  usage = ';]bf {?l} {code} | {?inp}',
                  description = '''\
L    [NUMBER] - How large the RAM should be, 16 bytes by default
CODE [TEXT  ] - The PrizFuck code to execute
INP  [TEXT  ] - The input text
*Type ';]bf help' to learn the new tokens
''')
async def bf(ctx, l: typing.Optional[int] = 16, *, bftxt):
    bf = bftxt
    if bf == "help":
        return await ctx.send("""```md
#] PRIZFUCK SYNTAX ---
CHAR | FUNCTION
-----|---------
 +   | Increment ram by 1
 -   | Decrement ram by 1
 >   | Shift right by 1
 <   | Shift left by 1
 .   | Print data
 ,   | Input data

 ^   | Mark location
 _   | Jump to marker

 ?   | Skip next command if ram != 0
 !   | Stop execution
 #   | Store X
 %   | Load X

 &   | 'AND' ram with X
 /   | 'OR' ram with X
 *   | 'XOR' ram with X
 ~   | 'NOT' ram

 [   | Jump to matching ] if ram == 0
 ]   | Jump to matching [ if ram != 0
 {   | Jump to matching } if ram != 0
 }   | Jump to matching { if ram == 0
 :   | Jump to matching ; if ram != 0
 ;   | End if statement
 X#  | Repeat an operation, eg +X64


#] NOTES ---
> You may only have 65535 bytes in RAM maximum, 
> - default is 16, but automatically increases.
> - You can put a number before your code to set
> - the ram size. It will automatically loop

> You may only loop 65535 times in the entire 
> - execution, it stops automatically

> You may only have 65535 tokens processed in
> - the entire execution, it stops automatically

> Once a number is greater than 255, it loops
> - back to 0

> Once a number is less than 0, it loops back
> - to 255

> To input data, use ;]bf <code> | <input>
```
""")
    msg = await ctx.send("```md\n#] INITIALIZING```")
    if l > 65535:
        await ctx.send("```diff\n-] RAM SIZE TOO BIG [65535 max]```")
        l = 65535
    if l % 8:
        l += 8 - (l % 8)
    if " | " in bf:
        inp = bf.split(" | ")[-1]
        bf = bf.split(" | ")[0]
    else:
        inp = ""
    ram = [0] * l
    i = 0
    x = 0
    z = 0
    p = 0
    brack = []
    curly = []
    ifs = []
    end_brack = {}
    end_curly = {}
    end_if = {}
    run_brack = {}
    run_curly = {}
    run_if = {}
    def repeater(matches):
        return matches[1] * int(matches[2])
    bf = re.sub(r"(.)X(\d+)", repeater, bf)
    bf = list(bftxt)
    for b in range(len(bf)):
        if bf[b] not in "?!<>[]{}#%^*+=-&~/:;.,_":
            bf[b] = ""
    bf = "".join(bf)
    if any(char in bf for char in "[]{}:;"):
        await msg.edit(content = "```md\n#] STORING LOOP DATA```")
        for x in range(len(bf)):
            y = bf[x]
            if y == "[":
                brack.append(x)
            elif y == "]":
                z = brack.pop()
                end_brack[x] = z
                run_brack[z] = x
            elif y == "{":
                curly.append(x)
            elif y == "}":
                z = curly.pop()
                end_curly[x] = z
                run_curly[z] = x
            elif y == ":":
                ifs.append(x)
            elif y == "]":
                z = ifs.pop()
                end_if[x] = z
                run_if[z] = x
    iter = 0
    tokens = 0
    out = []
    dbg = ""
    def stdinp(inp):
        for x in inp:
            yield x
    stdin = stdinp(inp)
    await msg.edit(content = "```md\n#] RUNNING...```")
    while p < len(bf) and tokens <= 65535 and iter <= 65535:
        tokens += 1
        b = bf[p]
        if b == "?":
            if ram[i] != 0:
                p += 1
        elif b == "]":
            if ram[i] != 0:
                p = end_brack[p]
                iter += 1
        elif b == "}":
            if ram[i] != 0:
                p = end_curly[p]
                iter += 1
        elif b == ":":
            if ram[i] != 0:
                p = run_if[p]
        elif b == ",":
            try:
                ram[i] = ord(stdin.__next__())
            except:
                pass
        elif b == "[": 
            if ram == 0:
                p = run_brack[p]
        elif b == "{": 
            if ram[i] != 0:
                p = run_curly[p]
        elif b == ".": out.append(f"{ram[i]:02x}")
        elif b == ">": i += 1
        elif b == "<": i -= 1
        elif b == "+": ram[i] += 1
        elif b == "-": ram[i] -= 1
        elif b == "^": z = i
        elif b == "_": i = z
        elif b == "!": break
        elif b == "#": x = ram[i]
        elif b == "%": ram[i] = x
        elif b == "&": ram[i] &= x
        elif b == "/": ram[i] |= x
        elif b == "*": ram[i] ^= x
        elif b == "~":
            s = f"{ram[i]:08b}"
            s = s.replace("0", ".")
            s = s.replace("1", "0")
            s = s.replace(".", "1")
            ram[i] = int(s, 2)
        
        p += 1
        if i == -1 and len(ram) < 65535:
            ram = [0] * 8 + ram
            i += 8
        elif i == -1:
            i = len(ram) - 1
        elif i == len(ram) and len(ram) < 65535:
            ram.extend([0] * 8)
        elif i == len(ram):
            i = 0
        if ram[i] > 255:
            ram[i] = 0
        elif ram[i] < 0:
            ram[i] = 255
        loc = (i % 8) * 8
        dbg += b + " | #" + hex(loc) + " - "
        dbg += " ".join(f"{c:02x}" for c in ram[loc:loc + 8]) + "\n"
        if iter > 65535:
            await ctx.send(f"```diff\n-] TOO MANY ITERATIONS [65535 max]```")
        elif tokens > 65535:
            await ctx.send(f"```diff\n-] TOO MANY TOKENS [65535 max]```")
    await msg.edit(content = "```md\n#] HEX EDITING```")
    unprintable = [f"{x:02x}" for x in list(range(0, 33)) + list(range(127, 160)) + [173]]
    for z in range(len(ram)):
        ram[z] = f"{ram[z]:02x}".upper()
    stdhex = ""
    stdraw = ""
    stdout = ""
    for x in range(0, len(out), 8):
        for y in range(4):
            try:
                stdout += out[x+y] + " "
            except IndexError:
                stdout += "   "
        stdout += " "
        for y in range(4, 8):
            try:
                stdout += out[x+y] + " "
            except IndexError:
                stdout += "   "
        stdout += " | "
        for y in range(8):
            try:
                if out[x+y] in unprintable:
                    stdout += "."
                else:
                    stdout += chr(int(out[x+y], 16))
                stdraw += chr(int(out[x+y], 16))
            except IndexError:
                stdout += " "
        stdout += "\n "
    stdout = " "+stdout.strip()
    for x in range(0, len(ram), 8):
        for y in range(4):
            stdhex += ram[x+y] + " "
            if x + y == i:
                stdhex = stdhex[:-4] + ">" + stdhex[-3:-1] + "<"
        stdhex += " "
        for y in range(4, 8):
            stdhex += ram[x+y] + " "
            if x + y == i:
                stdhex = stdhex[:-4] + ">" + stdhex[-3:-1] + "<"
        stdhex += " | "
        for y in range(8):
            if ram[x+y] in unprintable:
                stdhex += "."
            else:
                stdhex += chr(int(ram[x+y], 16))
        stdhex += "\n "
    stdhex = stdhex.strip()
    if not stdhex.startswith(">"):
        stdhex = " " + stdhex
    out = io.BytesIO(f'''OUTPUT ---
{stdraw}
{stdout}

RAM ---
{stdhex}

DEBUG ---
{dbg}
'''.encode("utf-8")) 

    r = "\n".join(stdhex.splitlines()[:15])
    o = "\n".join(stdout.splitlines()[:15])
    await msg.edit(content = "```md\n#] SENDING```")
    await ctx.send(
        embed = embedify(
            title = "PRIZFUCK ;]",
            desc = f"""```
#] OUTPUT
{stdraw[:200]}
{o[:1000]}``````md
#] RAM
{r[:1000]}``````md
#] TAPE
{bf[p:p+32]}END
^```""",
            foot = f"PRIZM ;] // TOKENS ] {tokens} // LOOPS ] {iter} // See file for more"
        ), 
        file = discord.File(out, "prizfuck.txt")
    )
    await msg.delete()
        
             
##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(bf)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('bf')
    print('GOOD')
