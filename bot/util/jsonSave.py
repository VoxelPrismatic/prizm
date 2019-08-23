import discord,json
from dyn import refresh
def saver(bot) -> None:
    """
    >>> SAVES DATA TO JSON FILE <<<
    BOT [BOT] - Bot, has all commands and things
    """
    allext, lodtxt = refresh.refresh()
    try:
        pre = json.load(open('json/prefixes.json'))
    except:
        open('prefixes.json','w').write('{"hi":"bye"}')
        pre = json.load(open('json/prefixes.json'))

    com = json.load(open('json/servers.json'))

    defaults = {'com':{},
                'tag':{},
                'wrd':{'wrd':[],'act':'None'},
                'mod':[],
                'rcf':True,
                'dr1':True,
                'nou':True,
                'lCH':None,
                'log':{'del':False, 'mVC':False, 'bot':False,
                       'blk':False, 'edt':False, 'em/':False,
                       'gc+':False, 'gc-':False, 'gc/':False,
                       'pin':False, 'int':False, 'web':False,
                       'mb+':False, 'mb-':False, 'mb/':False,
                       'gl/':False, 'rl+':False, 'bn-':False,
                       'rl-':False, 'rl/':False, 'bn+':False
                       }
                }
    # defaults is used instead of many 'try, except' statements
    for g in bot.guilds:
        try:
            x = pre[str(g.id)]
        except:
            pre[str(g.id)] = ';]'
        try:
            x = com[str(g.id)]
        except:
            com[str(g.id)]={}
        for key in defaults:
            try:
                x = com[str(g.id)][key]
                if type(x) == dict:
                    for ky in list(defaults[key]):
                        if ky not in list(com[str(g.id)][key]): # Adds missing keys
                            com[str(g.id)][key][ky] = defaults[key][ky]
                    #for ky in list(com[str(g.id)][key]):
                        #if ky == 'tag': continue
                        #if ky not in list(defaults[key]): del com[str(g.id)][key][ky]
            except:
                com[str(g.id)][key] = defaults[key]

        try:
            x = com[str(g.id)]["nam"]
        except:
            com[str(g.id)]["nam"]=g.name
        for ext in allext[:-1]:
            for nam in ext:
                c = bot.get_command(nam)
                try:
                    x = com[str(g.id)]["com"][c.name]
                except:
                    com[str(g.id)]["com"][c.name] = True # True means Enabled

    open('json/servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    open('json/prefixes.json','w').write(json.dumps(pre,sort_keys=True,indent=4))
