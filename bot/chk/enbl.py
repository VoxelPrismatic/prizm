import json
def enbl(ctx): return json.load(open('servers.json'))[str(ctx.guild.id)]["com"][ctx.command.name]
