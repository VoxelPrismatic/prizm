import os
os.system("pwd > loc.txt")
loc = "/".join(open("loc.txt").read().strip().split("/")[:-2]) + "/"
open("loc.txt", "w").write(loc)

def set_dirs(root):
    if root[-1] != "/":
        root += "/"
    ls = os.listdir(root)
    print("Scanning", root)
    for file in ls:
        if file == "__pycache__":
            continue
        if file.endswith(".py"):
            text = open(root + file).read()
            text = text.replace("/home/priz/Desktop/PRIZM/", loc)
            text = text.replace("/home/priz/Desktop/PRIZM", loc[:-1])
            open(root + file, "w").write(text)
        else:
            try:
                set_dirs(root + file)
            except:
                pass #Not a directory

set_dirs(loc)
