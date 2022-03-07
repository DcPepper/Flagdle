def choixCouleurs(trueColor):
    with open("colours.txt","r") as file:
        l = file.read()

    couleurs = [e.replace("\t", "").strip() for e in l.split('\n')][:-1]

    spectre={}

    for c in couleurs:
         col,hex = c.split(',')
         hex = hex.lstrip('#')
         r=int(hex[:2],16)
         g=int(hex[2:4],16)
         b=int(hex[4:],16)
         spectre[col]=(r,g,b)
    
    
    for col in trueColor:

        pmin=100
        kmin='None'
        for k in spectre:
            p=0
            for i in range(3):
                    p+=abs((spectre[k][i]-col[i])/256)
            p=p/3
            if p<pmin:
                    pmin=p
                    kmin=k
    
    
