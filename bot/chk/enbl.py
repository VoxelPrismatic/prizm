import json
def enbl(ctx): 
    print(ctx.guild)
    try:
        if ctx.guild: return json.load(open('servers.json'))[str(ctx.guild.id)]["com"][ctx.command.name]
        else: return True
    except: return True
