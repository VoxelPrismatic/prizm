import json
def getPre(bot,msg):
    try:
        return json.load(open('json/prefixes.json'))[str(msg.guild.id)]
    except Exception as ex:
        print(ex)
        return ";]"
