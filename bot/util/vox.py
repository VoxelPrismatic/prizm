def vox(sr):
    say=[];
    punc = ';,./?\'"[]{}\\|-_=+~`!@#$%^&*()'
    nums = ['zero','one','two','three','four','five','six','seven','eight','nine']
    for x in punc: sr = sr.replace(x,' ')
    for x in range(10): sr = sr.replace(str(x),nums[x]+' ')
    sf = sr.lower().split()
    words = {'er':['ur','ir','er','ear','ar '],
             'er':['ur','ir','er','ear','ar '],
             'th':['th'],
             'ar':['ar'],
             'kr':['cr'],
             'ng':['ng','nk'],
             'ir':['irr','eer'],
             'yr':['ir','ear ','are'],
             'ah':['au','a','ot','aw','ought'],
             'ay':['ao','a_e','ay','ai','ey','ei',' a '],
             'sh':['sh','ss','che','ti','ci'],
             'ch':['ch','tch'],
             'zh':['asu','isi'],
             'wh':['wh'],
             'ee':[' e','e_e','ee','ey','ie','y ','feat','ea_ '],
             'ea':['ea '],
             'eh':['ea','e','eh'],
             'oo':['oo','oul'],
             'oh':['o_e','oa','ou','oh','o'],
             'ie':[' i'],
             'iy':['i_e','igh','ie','i'],
             'uh':['u','o','u_y'],
             'uu':[' u_e','w'],
             'ow':['ow','o',' ou','ou_e'],
             'oy':['oi','oy'],
             'r':['rr','wr','r','re'],
             'h':['h'],
             'f':['ph','f'],
             'b':['bb','b'],
             'g':['gg','g'],
             'd':['dd','ed','d'],
             'j':['dge','ge','j'],
             'k':['que','ck','cc','k','c','q'],
             'l':['ll','l'],
             'm':['mm','m'],
             'n':['kn','nn','gn','n'],
             'p':['pp','p'],
             's':['sci','ce','ss','s'],
             't':['tt','t'],
             'v':['v'],
             'w':['w'],
             'y':['y','i'],
             'z':['zz','ze','as','is','z',' x'],
             'ks': ['x'],
             ' ':[' ']}
    for sd in sf:
        st = f'{sd} ';w=0
        for x in range(len(st)):
            if w>=len(st):break
            for y in words:
                for z in words[y]:
                    try:v=z.replace('_',st[w:][z.find('_')])
                    except:v=z
                    if st[w:].startswith(v):
                        if z==' i':y=' '+y
                        say.append(y);w+=len(z)
                        if z.endswith(' ') and z.count('_'):w-=2
                        break
            if st[w:].startswith(v):break

    return f"```md\n#] {''.join(say).strip()}```"