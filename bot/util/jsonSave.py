import discord,json
from dyn import refresh
def saver(bot):
    allext, lodtxt = refresh.refresh()
    try:pre = json.load(open('prefixes.json'))
    except: 
        open('prefixes.json','w').write('{"hi":"bye"}')
        pre = json.load(open('prefixes.json'))
    com = json.load(open('servers.json'))
    for g in bot.guilds:
        try: x = pre[str(g.id)]
        except: pre[str(g.id)] = ';]'
        try: x = com[str(g.id)]
        except: com[str(g.id)]={}
        try: x = com[str(g.id)]["com"]
        except: com[str(g.id)]["com"]={}
        try: x = com[str(g.id)]["tag"]
        except: com[str(g.id)]["tag"]={}
        try: x = com[str(g.id)]["wrd"]
        except: com[str(g.id)]["wrd"]={'wrd':[],'act':'None'}
        try: x = com[str(g.id)]["wrd"]["wrd"]
        except: com[str(g.id)]["wrd"]={'wrd':[],'act':'None'}
        try: x = com[str(g.id)]["mod"]
        except: com[str(g.id)]["mod"]=[]
        try: x = com[str(g.id)]["nam"]
        except: com[str(g.id)]["nam"]=g.name
        try: x = com[str(g.id)]["rcf"]
        except: com[str(g.id)]["rcf"] = True
        try: x = com[str(g.id)]["dr1"]
        except: com[str(g.id)]["dr1"] = True
        try: x = com[str(g.id)]["nou"]
        except: com[str(g.id)]["nou"] = True
        for ext in allext[:-1]:
            for nam in ext:
                c = bot.get_command(nam)
                try: x = com[str(g.id)]["com"][c.name]
                except: com[str(g.id)]["com"][c.name] = True
    open('servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    open('prefixes.json','w').write(json.dumps(pre,sort_keys=True,indent=4)) 
