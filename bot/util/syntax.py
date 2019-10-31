def code(st, syntax = ""): return f"```{syntax}\n{st}```"

def md(st): return code(st, "md")

def diff(st): return code(st, "diff")
