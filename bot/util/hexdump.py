unprintable = []
for x in list(range(0, 33)) + list(range(127, 160)):
    if x == 32:
        continue
    unprintable.append(f"{x:02x}")
unprintable.append(f"{173:02x}")

def hexdump(out):
    stdout = ""
    stdraw = ""
    for x in range(0, len(out), 8):
        for y in range(4):
            try:
                stdout += out[x + y] + " "
            except IndexError:
                stdout += "   "
        stdout += " "
        for y in range(4, 8):
            try:
                stdout += out[x + y] + " "
            except IndexError:
                stdout += "   "
        stdout += " | "
        for y in range(8):
            try:
                if out[x + y] in unprintable:
                    stdout += "•"
                else:
                    stdout += chr(int(out[x + y], 16))
                stdraw += chr(int(out[x + y], 16))
            except IndexError:
                stdout += " "
        stdout += "\n "
    stdout = " " + stdout.strip()

    return stdout, stdraw
