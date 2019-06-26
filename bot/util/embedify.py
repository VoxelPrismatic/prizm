import discord
def embedify(title="PRIZM ;]", desc="",
             thumb=None, foot=None,
             img=None, url=None,
             color=0x00ffff, auth=";]",
             footicon=None, authurl=None,
             authicon=None):
    emb = discord.Embed(title=title, description=desc, color=color)
    if url          : emb = discord.Embed(title=title, description=desc, color=color, url=url)
    if thumb        : emb.set_thumbnail(url=thumb)
    if foot         : emb.set_footer(text=foot)
    if footicon     : emb.set_footer(icon_url=footicon)
    if auth != ";]" : emb.set_author(name=auth)
    if authicon     : emb.set_author(name=auth, icon_url=authurl)
    if authurl      : emb.set_author(name=auth, url=url)
    if img          : emb.set_image(url=img)
    return emb

def embfield(emb, fields):
    for field in fields: emb.add_field(name=field[0], value=field[1], inline=field[2])
    return emb
