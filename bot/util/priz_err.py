class PrizmError(Exception):
    "Base Error class for Prizm"
    pass
       
class PrizmRedditError(PrizmError):
    def __init__(self):
        self.message = f"-] This subreddit/user/multireddit does not exist"
        self.syntax = "diff"
        self.typ = "PrizmRedditError"

class PrizmNsfwError(PrizmError):
    def __init__(self):
        self.message = "-] NSFW Posts are not allowed here"
        self.syntax = "diff"
        self.typ = "PrizmNsfwError"

class PrizmSyntaxError(PrizmError):
    def __init__(self, good):
        self.message = f"-] Correct Syntax ] {good}"
        self.syntax = "diff"
        self.typ = "PrizmSyntaxError"

class PrizmUnknownError(PrizmError):
    def __init__(self):
        self.message = "-] An internal error occured, no further info is known"
        self.syntax = "diff"
        self.typ = "PrizmUnknownError"

class PrizmModeratorError(PrizmError):
    def __init__(self):
        self.message = "-] Only moderators can use this command"
        self.syntax = "diff"
        self.typ = "PrizmModeratorError"

class PrizmFileError(PrizmError):
    def __init__(self):
        self.message = "-] Please add an attachment to use this command"
        self.syntax = "diff"
        self.typ = "PrizmFileError"