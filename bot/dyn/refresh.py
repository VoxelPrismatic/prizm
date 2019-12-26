def refresh():
    """
    >>> PROVIDES EASY EXTENSION LOADING <<<
    RETURNS - 2 LISTS
    """
    owncom = ["exe",  "pwr",  "chng",
              "dump", "pin0", "clr0",
              "edit","nick0", "shell",
              "clrin0", "srvedit", "lines",
              "helpown", "iedit", "dl"]

    modcom = ["clr", "pin", "ban",
              "kick", "nick", "enbl",
              "roles", "mng", 'audit']

    infcom = ["os", "git", "dir",
              "ping", "info", "hlep",
              "data", "hlepmod", "inv",
              'find']

    pubcom = ["md", "dnd", "snd",
              "rng", "rev", "poll",
              "rick", "coin", "asci",
              "optn", "echo", "spam",
              "cool", "emji", "slots",
              "react", "blkjck", "binary",
              "vox", "djq", "8ball",
              "reddit", "mines","hman",
              "mock", "bug", '2048',
              "captcha", "draw",
              "hexadecimal", "brainfuck"]

    discom = ["ci", "ei", "gi",
              "mi", "ri", "ui",
              'ti']

    mathcom = ["graph", "quad", "rto",
               "stats", "fct", "rad",
               "fact", 'rpn', 'simple',
               'calc', 'substitute',
               'triangle']

    intcom = ["slap", "hug", 'cuddle',
              'throw', 'kiss']

    othcom = ['mix', 'tag', "char",
              'text', 'code', 'convert']

    muscom = ['play', 'leave', 'pause']

    list_n = ["err", "com", "rctf",
              "druaga", 'log']

    allext = [owncom, modcom, infcom,
              pubcom, discom, mathcom,
              intcom, othcom, muscom,
              list_n]

    lodtxt = ["com.own.", "com.mod.", "com.inf.",
              "com.pub.", "com.dis.", "com.math.",
              "com.int.", "com.oth.", "com.music.",
              "lis."]

    return allext, lodtxt
