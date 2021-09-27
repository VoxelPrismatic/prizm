import aiohttp
import asyncio
import json
import zlib
import time
import os
import importlib

class Classify:
    def __init__(self, dic, __parent__ = None):
        self.__dic__ = dic
        self.__parent__ = __parent__
        for key in dic:
            if type(dic[key]) == dict:
                self.__setattr__(key, Classify(dic[key]))
            else:
                self.__setattr__(key, dic[key])
    def __update__(self, dic):
        self.__dic__.update(dic)
        for key in dic:
            if type(dic[key]) == dict:
                self.__setattr__(key, Classify(dic[key], __parent__ = self))
            else:
                self.__setattr__(key, dic[key])
    def __call__(key, _del = False, _upd = None, **kwargs):
        id = list(kwargs)[0]
        i = -1
        for item in self.__dic__[key]:
            i += 1
            if item[id] == kwargs[id]:
                if _del is True:
                    del self.__dic__[key][i]
                elif _up is not Noned:
                    item = _upd
                    self.__dic__[key][i] = upd
                return item


class Cache:
    def __init__(self):
        pass

class Everything:
    API_VERSION = 9
    API_ENCODING = "json"
    GATEWAY_VERSION = 9
    GATEWAY_ENCODING = "json"
    TOKENS = Classify(eval(open("tokens.json").read()))
    def __init__(self):
        self.cache = Cache()
        self.cache.guilds = {}
        self.cache.user = {}
        self.cache.imports = {}
        self.cache.commands = {}

    @property
    def API(self):
        return f"https://discord.com/api/v{self.API_VERSION}"

    def commands_url(self, g = None):
        if g:
            return f"{self.API}/applications/{self.API_ID}/guilds/{g}/commands"
        return f"{self.API}/applications/{self.API_ID}/commands"

    @property
    def gateway_url(self):
        return f"{self.API}/gateway"

    @property
    def gateway_args(self):
        return f"?v={self.GATEWAY_VERSION}&encoding={self.GATEWAY_ENCODING}"

    @property
    def API_ID(self):
        return self.cache.user.id

    @property
    def NOW(self):
        return time.strftime("%Y-%m-%dT%H:%M:%S%z")

    def interaction(self, resp, edit = False):
        if edit:
            st = f"{self.API}/webhooks/{resp['application_id']}/{resp['token']}/messages/{'@original' if edit == 1 or edit is True else edit}"
        else:
            st = f"{self.API}/interactions/{resp['id']}/{resp['token']}/callback"
        print("\x1b[94;1m" + st + "\x1b[0m")
        return st

    def member(self, msg):
        return msg["member"]["user"]["username"] + "#" + msg["member"]["user"]["discriminator"]

    async def fetch(self, m, *a, **kw):
        try:
            kw["headers"]["Authorization"] = "Bot " + self.TOKENS.bot
        except KeyError:
            kw["headers"] = {"Authorization": "Bot " + self.TOKENS.bot}
        print(kw)
        async with aiohttp.ClientSession() as sess:
            async with sess.request(m, *a, **kw) as resp:
                try:
                    return await resp.json()
                except:
                    return await resp.text()

    async def get(self, *a, **kw):
        return await self.fetch("GET", *a, **kw)
    async def post(self, *a, **kw):
        print("\x1b[92;1mPOST", a[0], "\x1b[0m")
        return await self.fetch("POST", *a, **kw)
    async def delete(self, *a, **kw):
        return await self.fetch("DELETE", *a, **kw)
    async def put(self, *a, **kw):
        return await self.fetch("PUT", *a, **kw)
    async def patch(self, *a, **kw):
        print("\x1b[93;1mPATCH", a[0], "\x1b[0m")
        return await self.fetch("PATCH", *a, **kw)

    def form(self, d = {}, f = None):
        form_data = aiohttp.FormData()
        if d:
            form_data.add_field("payload_json", json.dumps(d, separators = [",", ":"], ensure_ascii = True))
        if f:
            form_data.add_field(
                name = "file",
                content_type = "application/octet-stream",
                **f
            )
        return form_data

    def classify(self, a):
        return Classify(a)



WS = Everything()

async def load_commands(ctx):
    async with aiohttp.ClientSession() as sess:
        for dn, dr, fn in os.walk("commands"):
            for f in fn:
                if f.endswith(".py"):
                    k = dn.replace("/", ".") + "." + f[:-3]
                    print(k)
                    current = __import__(dn.replace("/", "."), None, None, [f[:-3]])
                    current = current.__getattribute__(f[:-3])
                    u = ctx.commands_url(533290351184707584 if "/owner" in dn else None)
                    id_ = 0
                    while True:
                        async with sess.post(u, headers = {"Authorization": "Bot " + ctx.token}, json = current.info) as resp:
                            print(resp)
                            d = await resp.json()
                            print(d)
                            ctx.cache.commands[current.info["name"]] = Classify({
                                "command": current.command,
                                "module": current,
                                "data": d,
                                "url": u
                            })
                            try:
                                id_ = d["id"]
                                break
                            except:
                                await asyncio.sleep(d["retry_after"])
                    if "/guilds/" in u:
                        async with sess.put(
                            u + "/" + id_ + "/permissions",
                            headers = {"Authorization": "Bot " + ctx.token},
                            json = {
                                "permissions": [{
                                    "id": '481591703959240706',
                                    "type": 2,
                                    "permission": True
                                }]
                            }
                        ) as resp:
                            print(await resp.json())
                        #input()

async def heartbeat(ctx):
    while True:
        print("Heartbeat:", ctx.heartbeat_interval)
        ctx.LATENCY = time.time()
        await ctx.websocket.send_json({"d": ctx.sequence, "op": 1})
        print("Heartbeat sent")
        await asyncio.sleep(ctx.heartbeat_interval / 1000)
        print(list(ctx.cache.commands))

async def login(token):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(WS.gateway_url) as resp:
            ws = (await resp.json())["url"] + WS.gateway_args
    WS.token = token
    data = {
        "token": token,
        "compress": True,
        "properties": {
            "$os": "Linux",
            "$browser": "PRIZM ;]",
            "$device": "PRIZM ;]"
        },
        "intents": sum([
            #1 << 14, #DM Typing
            #1 << 13, #DM Reactions
            #1 << 12, #DM Messages
            #1 << 11, #Guild Typing
            #1 << 10, #Guild Reactions
            #1 << 9,  #Guild Messages
            #1 << 8,  #Member Status
            #1 << 7,  #Member Voice
            #1 << 6,  #Guild Invite
            #1 << 5,  #Guild Webhooks
            #1 << 4,  #Guild Integrations
            #1 << 3,  #Guild Emojis
            #1 << 2,  #Guild Bans
            #1 << 1,  #Guild Members,
            1 << 0,  #Guilds
        ])
    }
    reconnect = False
    while True:
        async with aiohttp.ClientSession() as sess:
            async with sess.ws_connect(ws) as sock:
                WS.websocket = sock
                if not reconnect:
                    await sock.send_json({"d": data, "op": 2})
                    msg = (await sock.receive()).json()
                    print(msg)
                    WS.sequence = msg["s"]
        #            WS.heartbeat_loop = asyncio.new_event_loop()
                    WS.heartbeat_interval = msg["d"]["heartbeat_interval"]
                    WS.heartbeat_task = asyncio.create_task(heartbeat(WS))
                else:
                    await sock.send_json({"op": 6, "d": {"token": token, "session_id": WS.SESSION_ID, "seq": WS.sequence}})
                    msg = (await sock.receive()).json()
                    if msg["op"] == 9:
                        reconnect = False
                        continue
                async for msg in sock:
                    try:
                        d = msg.json()
                    except:
                        d = json.loads(zlib.decompress(msg.data))
                    print(d)
                    open(f"gateway/{time.monotonic()} op={d['op']} t={d['t']}.json", "w+").write(json.dumps(d, indent = 4))
                    if d["op"] == 0: #Dispatch event
                        t = d["t"]
                        if t == "READY":
                            WS.cache.user = Classify(d["d"]["user"])
                            await load_commands(WS)
    #                        input()
                            for g in d["d"]["guilds"]:
                                WS.cache.guilds[g["id"]] = Classify(g)
                            WS.SESSION_ID = d["d"]["session_id"]
                        elif t == "GUILD_CREATE":
                            try:
                                WS.cache.guilds[d["d"]["id"]].__update__(d["d"])
                            except KeyError:
                                WS.cache.guilds[d["d"]["id"]] = Classify(d["d"])
                        elif t == "INTERACTION_CREATE":
                            try:
                                asyncio.create_task(WS.cache.commands[d["d"]["data"]["name"]].command(WS, d["d"]))
                            except:
                                try:
                                    asyncio.create_task(WS.cache.commands[d["d"]["message"]["interaction"]["name"]].command(WS, d["d"]))
                                except:
                                    print("\x1b[94;1mERROR: Command not found\x1b[0m")
                    elif d["op"] == 1: #Heartbeat
                        pass
                    elif d["op"] == 7: #Reconnect
                        print({"op": 6, "d": {"token": token, "session_id": WS.SESSION_ID, "seq": WS.sequence}})
                        await sock.send_json({"op": 6, "d": {"token": token, "session_id": WS.SESSION_ID, "seq": WS.sequence}})
                        reconnect = True
                    elif d["op"] == 9: #Invalid Session
                        await sock.send_json({"d": data, "op": 2})
                    elif d["op"] == 10: #Hello
                        WS.heartbeat_interval = d["d"]["heartbeat_interval"]
                    elif d["op"] == 11: #Heartbeat ACK
                        WS.LATENCY = time.time() - WS.LATENCY
                    WS.sequence = d["s"] or WS.sequence
    #            exit()

for f in os.listdir("gateway"):
    os.remove("gateway/" + f)

while True:
    asyncio.run(login(WS.TOKENS.bot))
