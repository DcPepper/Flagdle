import random


def choixCouleurs(trueColor):
    with open("colours.txt", "r") as file:
        l = file.read()

    couleurs = [e.replace("\t", "").strip() for e in l.split("\n")][:-1]

    spectre = {}

    for c in couleurs:
        col, hex = c.split(",")
        hex = hex.lstrip("#")
        r = int(hex[:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:], 16)
        spectre[col] = (r, g, b)

    for col in trueColor:

        pmin = 100
        kmin = "None"
        for k in spectre:
            p = 0
            for i in range(3):
                p += abs((spectre[k][i] - col[i]) / 256)
            p = p / 3
            if p < pmin:
                pmin = p
                kmin = k
        spectre.pop(kmin)

    for i, col in enumerate(trueColor):
        spectre[str(i)] = col

    keys = list(spectre.keys())
    random.shuffle(keys)
    spectrefinal = {}
    for key in keys:
        spectrefinal[key] = spectre[key]
    return spectrefinal.values()


trueColor = [
    (0, 119, 73),
    (255, 184, 28),
    (0, 0, 0),
    (255, 255, 255),
    (224, 60, 49),
    (0, 20, 137),
]

choixCouleurs(trueColor)
