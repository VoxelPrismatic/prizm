def has_attachment(ctx):
    return bool(len(ctx.message.attachments))

def has_embed(ctx):
    return bool(len(ctx.message.embeds))

def file_type(ctx, filetype, attnum = 0):
    if not has_attachment(ctx): return False
    return ctx.message.attachments[attnum].endswith(filetype)