import os
here = open("loc.txt").read()
home = "/".join(here.split("/")[:3]) + "/"
dirs = [
    ".config/",
    ".config/matplotlib/",
    ".config/matplotlib/stylelib/"
]
for d in dirs:
    try:
        os.listdir(home + d)
    except:
        os.mkdir(home + d)

for file in os.listdir(here + "mpl_stylelib"):
    thisfile = here + "mpl_stylelib/" + file
    thatfile = home + d + file
    print(f"'{thisfile}' -> '{thatfile}'")
    open(thatfile, "w+").write(open(thisfile).read())
