import discord, datetime
from discord import Embed
import discord, re
#from util.PrizErr import *
global NA
NA = Embed.Empty

def embedify(
    ##/// QUICK KWARGS
    title = "PRIZM ;]", desc="",
    thumb = "", foot = "",
    img = "",  url = "", time = "",
    color=0x00ffff, auth = "",
    foot_ico = "", auth_url = "",
    auth_ico = "", fields = [], typ="rich"
    ) -> discord.Embed:
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
    FOOT_ICO [STR     ] - HTTP[S] Url for footer icon
    AUTH_URL [STR     ] - I'm not too sure
    AUTH_ICO [STR     ] - HTTP[S] Url for author icon
    FIELDS   [LIST    ] - List of fields [[name: str, desc: str, inline: bool], ...]
    TYP      [STR     ] - The embed type, "rich" by default

    *All URLs must be HTTP[S], otherwise the function will silently ignore it
    *Any params not specified will be an empty string or the Embed.Empty thing
    """
    ##/// Check for valid time
    if time == 'now': time = datetime.datetime.utcnow()
    elif not time: time = NA
    elif type(time) != datetime.datetime: time = NA

    ##/// Check for valid URLs
    url_regex = r"https?\://"
    if not re.search(url_regex, str(auth_ico)): auth_ico = ""
    if not re.search(url_regex, str(url)): url = ""
    if not re.search(url_regex, str(thumb)): thumb = ""
    if not re.search(url_regex, str(img)): img = ""
    if not re.search(url_regex, str(auth_ico)): auth_ico = ""

    ##/// Create the embed
    emb = discord.Embed(
        title = str(title) or NA,
        description = str(desc) or "",
        color = color or 0x00ffff,
        url = str(url) or NA,
        timestamp = time or NA,
        type = str(typ) or "rich"
    )
    emb.set_footer(text = str(foot) or NA, icon_url = str(foot_ico) or NA)
    if thumb: emb.set_thumbnail(url = str(thumb))
    if auth: emb.set_author(name = str(auth), icon_url = str(auth_ico)or NA, url = str(auth_url) or NA)
    if img: emb.set_image(url = str(img))
    return embfield(emb, fields)

def embfield(emb, fld):
    fields = fld
    """
    >>> ADDS FIELD TO A GIVEN EMBED <<<
    Is designed to make what would've been many commands into one

    EMB    [Embed] - The embed instance
    FIELDS [LIST ] - List of fields [[name: str, value: str, inline: bool*], ...]
    *I actually support more than bools as it is converted into a string and check for manually
    """
    for field in fields:
        if len(field) == 3:
            emb.add_field(name = str(field[0]),
                      value = str(field[1]),
                      inline = str(field[2]) in ["True", "true", "y", "t", "ye", "yes", "1"])
        elif len(field) == 2:
            emb.add_field(name = str(field[0]),
                      value = str(field[1]),
                      inline = False)
        elif len(field) == 1:
            emb.add_field(name = ";]",
                          value = str(field[0]),
                          inline = False)
        else:
            pass#raise PrizmEmbedifyError(field)
    return emb

def emb_compat(
    ##/// COMPATIBLE KWARGS [CHECK D.PY DOCS]
    title = 'PRIZM ;]', description = '',
    thumbnail = "", footer = "",
    url = "", timestamp = "",
    image = "", author = "",
    author_icon = "", author_url = "",
    footer_icon = "", fields = [],
    type = "rich"
    ) -> discord.Embed:
    return embedify(title = title, desc = description, thumb = thumbnail,
                    url = url, time = timestamp, img = image, auth = author,
                    auth_ico = author_icon, auth_url = author_url, typ = type,
                    foot = footer, foot_ico = footer_icon, fields = fields)

##/// SHORTER CALL METHODS for ease of use
def emb(*args, **kwargs): return embedify(*args, **kwargs)
def emb_c(*args, **kwargs): return emb_compat(*args, **kwargs)
def emb_f(*args, **kwargs): return embfield(*args, **kwargs)
