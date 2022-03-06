"""
Like wordle but guess the flag by adding colors.
By DcPepper
"""
import colorsys
from turtle import color
from requests import get
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from parsePays import getCodeISO
from tkinter import Tk, Button, LEFT, RIGHT, Frame, Label, PhotoImage, BOTTOM

# Step 1: Count how many (different) colors a flag has

# get All the colors

pays = getCodeISO()


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

    nbr = 0

    trueColor = []
    for n in colors:
        if colors[n] >= 2500:
            nbr += 1
            trueColor.append(n)

    nbrColor = 0
    for i in range(width):
        for j in range(height):
            color = rgb.getpixel((i, j))

            if color not in trueColor:
                rgb.putpixel((i, j), (0, 0, 0))
            else:
                rgb.putpixel((i, j), (255, 255, 255))
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
    rgb.show()

    rgb.save("flag_uncolored.png")

    return nbr, trueColor


problemenbr, problemeColor = getColors("pg")
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


spectrecouleur = spectre(usedColor)


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


def passer():
    pass


gui = Tk()
frame = Frame(gui)
framePicture = Frame(gui)
GOOD = 0
for i, col in enumerate(spectrecouleur):
    btn = Button(
        frame, bg=_from_rgb(col), width=5, height=5, command=lambda i=i: click(i)
    )
    btn.grid(row=0, column=i)
img = PhotoImage(file="flag_uncolored.png")
label = Label(framePicture, image=img).pack()
frame.pack()
framePicture.pack()

gui.mainloop()
