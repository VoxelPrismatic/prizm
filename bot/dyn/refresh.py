def refresh():
    owncom = ["exe",  "pwr",  "chng",
              "dump", "pin0", "clr0",
              "calc", "edit","nick0",
              "shell", "clrin0", "unpin0",
              "helpown","iedit","dl",
              "srvedit"]

    modcom = ["clr","pin","ban",
              "kick","nick","clrin",
              "unpin","enbl","role",
              "mng",'audit']

    infcom = ["os","git","dir",
              "ping","info","hlep",
              "data","hlepmod","hlepmini",
              "inv"]

    pubcom = ["md","dnd","snd",
              "rng","rev","poll",
              "rick","coin","asci",
              "optn","echo","spam",
              "cool","emji","slots",
              "react","blkjck","binary",
              "vox","djq","char",
              "mines","hman","mock",
              "tag","bug"]

    discom = ["chnl","emj","gld",
              "mbr","rol","usr"]

    mathcom = ["graph","quad","rto",
               "stats","fct","rad",
               "fact",'rpn']
    
    intcom = ["slap","hug"]

    list_n = ["gld","err","mtn",
              "com","rctf","druaga"]

    allext = [owncom,modcom,infcom,
              pubcom,discom,mathcom,
              intcom,list_n]

    lodtxt = ["com.own.","com.mod.","com.inf.",
              "com.pub.","com.dis.","com.math.",
              "com.int.","lis."]

    return allext, lodtxt
