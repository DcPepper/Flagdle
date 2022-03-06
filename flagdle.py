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

# Step 1: Count how many (different) colors a flag has

# Download the image

image = get("https://flagcdn.com/w640/az.png")

# Display the image

with open("flag.png", "wb") as file:
    file.write(image.content)

im = Image.open("flag.png")
width, height = im.size
rgb = im.convert("RGB")
colors = {}
# around = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
around = [(0, 1), (0, -1), (-1, 0), (1, 0)]
for i in range(width):
    for j in range(height):
        aroundIJ = []
        for e in around:
            if (
                (i + e[0] >= 0)
                and (i + e[0] < width)
                and (j + e[1] >= 0)
                and (j + e[1] < height)
            ):
                aroundIJ.append((i + e[0], j + e[1]))
        pixelColor = rgb.getpixel((i, j))
        bool = False
        for voisins in aroundIJ:
            x, y = voisins
            if rgb.getpixel((x, y)) == pixelColor:
                bool = True

        if bool and (pixelColor not in colors):
            colors[pixelColor] = 1
        elif bool:
            colors[pixelColor] += 1
        else:
            colors[pixelColor] += 1
            """
            if i - 1 >= 0:
                rgb.putpixel((i, j), rgb.getpixel((i - 1, j)))
                pixelColor = rgb.getpixel((i, j))
                colors[pixelColor] += 1
            else:
                rgb.putpixel((i, j), rgb.getpixel((i, j - 1)))
                pixelColor = rgb.getpixel((i, j))
                colors[pixelColor] += 1
            """

print(colors)
nbr = 0
trueColor = []
for n in colors:
    if colors[n] >= 1000:
        nbr += 1
        trueColor.append(n)

grisRange = [int(100 + ((100 * k) / nbr)) for k in range(nbr)]

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

print(nbr)
rgb.show()

# im.show()
