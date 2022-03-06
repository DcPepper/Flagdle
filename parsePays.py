def getCodeISO():
    with open("listePays.txt") as file:
        lignes = file.read()
        pays = lignes.split("\t")
        codes = [(e.split("\n")[0]).lower() for e in pays]
        codes.remove("afghanistan ")
        return codes
