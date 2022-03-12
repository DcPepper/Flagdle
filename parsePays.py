def getCodeISO():
    with open("listePays.txt", encoding="utf-8") as file:
        lignes = file.read()
        pays = lignes.split("\n")
        codes = [e.split(" \t") for e in pays]
        return codes
