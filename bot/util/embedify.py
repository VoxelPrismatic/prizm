import discord, datetime
def embedify(title="PRIZM ;]", desc="",
             thumb=None, foot=None,
             img=None,  url=None, time=None,
             color=0x00ffff, auth=";]",
             footicon=None, authurl=None,
             authicon=None, fields=None) -> discord.Embed:
    """
    >>> CREATES AN EMBED <<<
    Is designed to make what would've been many commands into one

    TITLE    [STR     ] - The Title
    DESC     [STR     ] - Description
    THUMB    [STR     ] - HTTP[S] Url for thumbnail
    FOOT     [STR     ] - The footer
    IMG      [STR     ] - HTTP[S] Url for image
    URL      [STR     ] - HTTP[S] Url for when the embed is tapped on

    TIME     [DATETIME] - Datetime instance for the timestamp
                        - if time == 'now', then the current time will be used
                        - ^ that is a timesaver on purpose

    COLOR    [HEX     ] - The color of the embed, in hex
    AUTH     [STR     ] - The author, places on top of the title
    FOOTICON [STR     ] - HTTP[S] Url for footer icon
    AUTHURL  [STR     ] - I'm not too sure
    AUTHICON [STR     ] - HTTP[S] Url for author icon
    FIELDS   [LIST    ] - List of fields [[name,desc,inline],[name,desc,inline]]
    """
    if time == 'now': time = datetime.datetime.utcnow()
    elif not time: time = discord.Embed.Empty
    elif type(time) != datetime.datetime: time = discord.Embed.Empty

    emb = discord.Embed(title=title,
                        description=desc,
                        color=color,
                        timestamp=time)

    if url          : emb = discord.Embed(title=title,
                                          description=desc,
                                          color=color,
                                          url=url,
                                          timestamp=time)

    if thumb        : emb.set_thumbnail(url=thumb)
    if foot         : emb.set_footer(text=foot)
    if footicon     : emb.set_footer(icon_url=footicon)
    if auth != ";]" : emb.set_author(name=auth)
    if authicon     : emb.set_author(name=auth, icon_url=authurl)
    if authurl      : emb.set_author(name=auth, url=url)
    if img          : emb.set_image(url=img)
    if fields       : emb = embfield(emb,fields)

    return emb

def embfield(emb, fields):
    """
    >>> ADDS FIELD TO A GIVEN EMBED <<<
    Is designed to make what would've been many commands into one

    EMB    [discord.Embed] - The embed instance
    FIELDS [LIST         ] - List of fields [[name,desc,inline],[name,desc,inline]]
    """
    for field in fields: emb.add_field(name=field[0], value=field[1], inline=field[2])
    return emb
