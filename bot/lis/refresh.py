def refresh():
    owncom = ["calc","clr0","clrin0","exe","helpown",
              "pin0","unpin0","pwr","chng", "dump",
              "edit","nick0"]

    modcom = ["ban","clr","clrin","kick","pin",
              "unpin","nick"]

    infcom = ["data","git","hlep","hlepmod","info",
              "os","ping", "hlepmini","hleptest","dir"]

    pubcom = ["binary","blkjck","coin","cool","dnd",
              "echo","react","rick","rng","slots",
              "snd","spam","emji","rev",
              "asci","optn","md"]

    discom = ["chnl","emj","gld","mbr","rol",
              "usr"]

    mathcom = ["graph","quad","rto","stats","fct",
               "rad","fact"]

    list_n = ["gld","err","mtn","com","rctf","druaga"]

    allext = [owncom,modcom,infcom,pubcom,discom,mathcom,list_n]

    lodtxt = ["com.own.","com.mod.","com.inf.","com.pub.","com.dis.","com.math.","lis."]

    return allext, lodtxt