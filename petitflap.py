"""
Like wordle but guess the flag by adding colors.
By DcPepper
"""
import colorsys
from faulthandler import disable
from turtle import color
from requests import get
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from parsePays import getCodeISO
from tkinter import *
from PIL import Image
from choixCouleurs import choixCouleurs
import random

# Step 1: Count how many (different) colors a flag has

# get All the colors

paysetISO = getCodeISO()
pays = [e[1].lower() for e in paysetISO]
paysNames = [e[0] for e in paysetISO]
paysNamesdict = {}
for p in paysetISO:
    paysNamesdict[p[0]] = p[1].lower()
chosenPay = pays[random.randint(0, len(pays) - 1)]
PAYS = ""
for p in paysetISO:
    p = [e.lower() for e in p]
    if chosenPay in p:
        PAYS = p[0]
        break
PAYS = PAYS[0].upper() + PAYS[1:]
print(chosenPay)
# Download the image
def getFlag(country):
    image = get("https://flagcdn.com/w640/" + country + ".png")

    # Save the image

    with open("flag.png", "wb") as file:
        file.write(image.content)


def getColors(country):
    getFlag(country)
    im = Image.open("flag.png")
    width, height = im.size
    rgb = im.convert("RGB")
    colors = {}
    # around = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    around = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    for i in range(width):
        for j in range(height):

            pixelColor = rgb.getpixel((i, j))

            if pixelColor not in colors:
                colors[pixelColor] = 1
            else:
                colors[pixelColor] += 1

    rankedcolors = {k: v for k, v in sorted(colors.items(), key=lambda item: item[1])}
    print(rankedcolors)
    nbr = 0

    trueColor = []
    almostColor = []
    for n in colors:
        if colors[n] >= 2500:
            nbr += 1
            trueColor.append(n)
        elif colors[n] >= 2500:
            almostColor.append(n)

    nbrColor = 0
    for i in range(width):
        for j in range(height):
            color = rgb.getpixel((i, j))

            if color not in trueColor and color not in almostColor:
                rgb.putpixel((i, j), (1, 1, 1))
            elif color in almostColor:
                pass
            else:
                rgb.putpixel((i, j), (200, 200, 200))
            """
            if color not in trueColor:
                rgb.putpixel((i, j), (0, 0, 0))
            else:
                gris = grisRange[trueColor.index(color)]
                rgb.putpixel((i, j), (gris, gris, gris))
            """
            pass
    # print(trueColor)
    print(nbr)
    # rgb.show()

    rgb.save("flag_uncolored.png")

    return nbr, trueColor


problemenbr, problemeColor = getColors(chosenPay)
print(problemeColor)
usedColor = problemeColor[:]
colore = problemeColor
for i, c in enumerate(colore):
    temp = []
    for ent in c:
        temp.append(max(round(ent / 128) * 128 - 1, 0))
    colore[i] = tuple(temp)
problemeColor = colore

im2 = Image.open("flag_uncolored.png")
rgb2 = im2.convert("RGB")
bonnereponse = 10
while bonnereponse < problemenbr:
    rep = input("Choisir couleur (RGB):")
    rep = tuple([int(e) for e in rep.split(",")])
    im = Image.open("flag.png")

    width, height = im.size
    rgb = im.convert("RGB")

    if rep in problemeColor:
        bonnereponse += 1
        print("Bonne réponse !")
        for i in range(width):
            for j in range(height):
                colore = rgb.getpixel((i, j))
                temp = []
                for ent in colore:
                    temp.append(max(0, round(ent / 128) * 128 - 1))
                color_simple = tuple(temp)

                if rep == color_simple:
                    rgb2.putpixel((i, j), colore)
    else:
        print("MAuvaise réponse")
    rgb2.show()


def spectre(trueColor):
    countCouleur = 0
    imcouleur = Image.new("RGB", (4 * 27, 50))
    spectreCouleur = []

    for r in range(0, 257, 128):
        r = max(0, r - 1)
        for g in range(0, 257, 128):
            g = max(0, g - 1)
            for b in range(0, 257, 128):
                b = max(0, b - 1)
                raux, gaux, baux = r, g, b
                for couleur in trueColor:

                    # print(r, g, b, couleur[0], couleur[1], couleur[2])
                    if (
                        round(couleur[0] / 128) * 128 >= r
                        and round(couleur[1] / 128) * 128 >= g
                        and round(couleur[2] / 128) * 128 >= b
                        and round(couleur[0] / 128) * 128 < r + 128
                        and round(couleur[1] / 128) * 128 < g + 128
                        and round(couleur[2] / 128) * 128 < b + 128
                    ):
                        print(raux, gaux, baux, couleur)
                        (raux, gaux, baux) = couleur
                        break
                spectreCouleur.append((raux, gaux, baux))
                for i in range(4):
                    for j in range(50):

                        imcouleur.putpixel(
                            (i + 4 * countCouleur, j), (raux, gaux, baux)
                        )
                countCouleur += 1
    # imcouleur.show()
    print(spectreCouleur)
    return spectreCouleur


spectrecouleur = choixCouleurs(usedColor)


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return "#%02x%02x%02x" % rgb


def click(i):
    global rgb2, problemeColor, GOOD, frame, spectrecouleur, im, rgb2, framePicture, gui
    name = spectrecouleur[i]
    if GOOD >= len(problemeColor):
        gui.destroy()
        print("GG")
    else:
        rep = name
        # rep = tuple([int(e) for e in rep.split(",")])
        im = Image.open("flag.png")

        width, height = im.size
        rgb = im.convert("RGB")

        temp = []
        for ent in rep:
            temp.append(max(0, round(ent / 128) * 128 - 1))
        rep = tuple(temp)
        # textFrame = Frame(gui)
        # textLabel = Label(textFrame, text="")
        # textLabel.grid()
        if rep in problemeColor:
            GOOD += 1
            print("Bonne réponse !")
            for i in range(width):
                for j in range(height):
                    colore = rgb.getpixel((i, j))
                    temp = []
                    for ent in colore:
                        temp.append(max(0, round(ent / 128) * 128 - 1))
                    color_simple = tuple(temp)

                    if rep == color_simple:
                        rgb2.putpixel((i, j), colore)
            rgb2.save("flag_uncolored.png")
            img = PhotoImage(file="flag_uncolored.png")
            print(framePicture.winfo_children())
            label = framePicture.winfo_children()[0]
            label.configure(image=img)
            label.image = img
            # textLabel["text"] = "OUI"
            # textFrame.grid()

        else:
            print("MAuvaise réponse")
            # textLabel["text"] = "NON"
            # textFrame.grid()


def changeCouleur(step):
    global rgb2, problemeColor, GOOD, frame, spectrecouleur, im, framePicture, gui, x, y, a, etape, btns, label, chosenOne, chosenColors, btncouleur
    etape = step
    name = a.winfo_name()
    text = a["text"]

    if name == "img":
        text = btns[0]["text"]
        if "." in text:
            btncouleur["bg"] = "#c8c8c8"
            print("Couleur placée")
            for btn in btns:
                btn["text"] = btn["text"][:-1]

            col = chosenOne[1:]
            r = int(col[:2], 16)
            g = int(col[2:4], 16)
            b = int(col[4:], 16)
            rep = (r, g, b)
            im = Image.open("flag.png")
            rgb = im.convert("RGB")
            width, height = im.size
            colHere = rgb.getpixel((x, y))
            chosenColors[colHere] = rep
            for i in range(width):
                for j in range(height):
                    if rgb.getpixel((i, j)) == colHere:
                        rgb2.putpixel((i, j), rep)
            rgb2.save("flag_uncolored.png")
            img = PhotoImage(file="flag_uncolored.png")
            label = framePicture.winfo_children()[0]
            label.configure(image=img)
            label.image = img
        else:
            print("Choisir une couleur d'abord")

    else:
        btncouleur["bg"] = a["bg"]
        chosenOne = a["bg"]
        print("Couleur choisie:" + chosenOne)
        for btn in btns:
            btn["text"] = btn["text"] + "."
    pass


def validerPays():
    global my_entry, consignes
    answer = my_entry.get()
    if paysNamesdict[answer] == chosenPay:
        consignes["text"] = "Bravo ! Tu as même réussi à trouver le pays !"
        print("Win")
    else:
        consignes["text"] = f"Dommage ! Le pays était: {PAYS}"
        print("Lose")


def update(elt):
    global my_list
    my_list.delete(0, END)
    for country in elt:
        my_list.insert(END, country)


def fillout(e):
    my_entry.delete(0, END)
    my_entry.insert(END, my_list.get(ANCHOR))


def check(e):
    typed = my_entry.get()
    if typed == "":
        data = paysNames
    else:
        data = []
        for country in paysNames:

            if typed.lower() in country.lower():
                data.append(country)

    update(data)


def valide():
    global chosenColors, consignes, usedColor, rgb2, btns, btns_valide, wrong_colors, GOOD, TRY, valider, carresgris, my_entry, my_list
    TRY += 1
    im = Image.open("flag.png")
    rgb = im.convert("RGB")
    width, height = im.size
    wrong_colors = []
    close_colors = []
    good_colors = []
    if TRY < 6:
        changecarregris = framePicture.winfo_children()[TRY]

        w, h = rgb2.size
        imtemp = rgb2.resize((w // 5, h // 5))
        imtemp.save("imtemp" + str(TRY) + ".png")
        imgcarre = PhotoImage(file="imtemp" + str(TRY) + ".png")
        changecarregris.configure(image=imgcarre)
        changecarregris.image = imgcarre
    for col in chosenColors.keys():
        tryColor = chosenColors[col]
        if tryColor != col:
            if tryColor not in usedColor:
                if tryColor not in wrong_colors:
                    wrong_colors.append(tryColor)
                for i in range(width):
                    for j in range(height):
                        if rgb2.getpixel((i, j)) == tryColor:
                            rgb2.putpixel((i, j), (200, 200, 200))
            else:
                if tryColor not in close_colors:
                    close_colors.append(tryColor)
                for i in range(width):
                    for j in range(height):
                        if (
                            rgb2.getpixel((i, j)) == tryColor
                            and rgb.getpixel((i, j)) != tryColor
                        ):
                            rgb2.putpixel((i, j), (200, 200, 200))
        else:
            if tryColor not in good_colors:
                good_colors.append(tryColor)
            pass
    for col in wrong_colors:
        colHex = "#"
        for bit in col:
            bit = hex(bit)[2:]
            if len(bit) == 1:
                bit = "0" + bit
            colHex += bit
        for but in btns:
            if but["bg"] == colHex:
                break
        btns_valide[btns.index(but)]["bg"] = "#000000"
    for col in close_colors:
        colHex = "#"
        for bit in col:
            bit = hex(bit)[2:]
            if len(bit) == 1:
                bit = "0" + bit
            colHex += bit
        for but in btns:
            if but["bg"] == colHex:
                break
        btns_valide[btns.index(but)]["bg"] = "#f6e072"

    for col in good_colors:
        colHex = "#"
        for bit in col:
            bit = hex(bit)[2:]
            if len(bit) == 1:
                bit = "0" + bit
            colHex += bit
        for but in btns:
            if but["bg"] == colHex:
                break
        btns_valide[btns.index(but)]["bg"] = "#68f31f"

    GOOD = len(good_colors)

    if GOOD == len(usedColor):
        valider.pack_forget()
        consignes["text"] = "VICTOIRE ! Saurais-tu trouver le pays de ce drapeau?"
        img = PhotoImage(file="flag.png")
        label = framePicture.winfo_children()[0]
        label.configure(image=img)
        label.image = img

        my_entry.pack(side=LEFT)
        my_list.pack(side=LEFT)
        my_button.pack(side=RIGHT)

    elif TRY == 6:
        valider.pack_forget()
        consignes["text"] = f"Dommage... Le drapeau était: {PAYS}"
        img = PhotoImage(file="flag.png")
        label = framePicture.winfo_children()[0]
        label.configure(image=img)
        label.image = img

    else:
        rgb2.save("flag_uncolored.png")
        close_colors = []

        img = PhotoImage(file="flag_uncolored.png")
        label = framePicture.winfo_children()[0]
        label.configure(image=img)
        label.image = img


gui = Tk()
frame = Frame(gui)
frameText = Frame(gui)
framePicture = Frame(gui)
frameButton = Frame(gui)

TRY = 0
GOOD = 0
etape = 1
btns = []
btns_valide = []
chosenColors = {}
for i, col in enumerate(spectrecouleur):
    btn_valide = Button(frame, name=str(i), width=4, state=DISABLED)
    btn = Button(
        frame,
        text=str(i),
        fg=_from_rgb(col),
        bg=_from_rgb(col),
        width=4,
        height=5,
        command=lambda etape=etape: changeCouleur(etape),
    )
    btns_valide.append(btn_valide)
    btns.append(btn)
    btn_valide.grid(row=1, column=i)
    btn.grid(row=0, column=i)
btncouleurframe = Frame(
    frame, width=4, height=5, highlightbackground="black", highlightthickness=2
)
btncouleur = Button(btncouleurframe, width=4, height=5, state=DISABLED)
btncouleur.pack()
btncouleurframe.grid(row=0, column=i + 1)
img = PhotoImage(file="flag_uncolored.png")
label = Button(
    framePicture,
    image=img,
    name="img",
    command=lambda etape=etape: changeCouleur(etape),
)

label.pack(side=LEFT)


message = f"Nombre de couleur à trouver: {len(usedColor)}"
consignes = Label(frameText, state=DISABLED, height=1, text=message)
print(message)
consignes.pack()
print(consignes)

frame.pack()
frameText.pack()
framePicture.pack()

carresgris = []
imsize = Image.open("flag.png")
w, h = imsize.size
for i in range(5):
    carregris = PhotoImage(file="greyblock.png", name=str(i))
    labelgris = Button(
        framePicture,
        name=str(i),
        image=carregris,
        state=DISABLED,
        height=h // 5 - 1,
        width=w // 5,
    )
    carresgris.append(carregris)
    labelgris.pack()

valider = Button(frameButton, text="Valider", command=valide)
valider.pack()


quit = Button(frameButton, text="Quitter", command=gui.destroy)
quit.pack()

frameButton.pack()


def getorigin(eventorigin):
    global x, y, label, a, btns
    a = eventorigin.widget
    x = eventorigin.x
    y = eventorigin.y
    X = label.winfo_rootx()
    Y = label.winfo_rooty()
    # print(x, y, X, Y, eventorigin, a.winfo_name())


my_entry = Entry(frameButton)


my_list = Listbox(frameButton)

my_button = Button(frameButton, text="VALIDER", command=validerPays)
my_list.bind("<<ListboxSelect>>", fillout)
my_entry.bind("<KeyRelease>", check)

update(paysNames)

gui.bind("<Button 1>", getorigin)

gui.mainloop()
