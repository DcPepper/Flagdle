from tkinter import *

from matplotlib.pyplot import text

root = Tk()
my_label = Label(root, text="Can you guess the flag?")
my_label.pack()


my_entry = Entry(root)
my_entry.pack()

my_list = Listbox(root)
my_list.pack()


def validerPays():
    answer = my_entry.get()
    if answer == "Canada":
        print("Win")
    else:
        print("Lose")


my_button = Button(root, text="Valider", command=validerPays)
my_button.pack()

countries = [
    "Antigua and Barbuda",
    "Bahamas",
    "Barbados",
    "Belize",
    "Canada",
    "Costa Rica ",
    "Cuba",
    "Dominica",
    "Dominican Republic",
    "El Salvador ",
    "Grenada",
    "Guatemala ",
    "Haiti",
    "Honduras ",
    "Jamaica",
    "Mexico",
    "Nicaragua",
    "Saint Kitts and Nevis",
    "Panama ",
    "Saint Lucia",
    "Saint Vincent and the Grenadines",
    "Trinidad and Tobago",
    "United States of America",
]


def update(elt):
    my_list.delete(0, END)
    for country in elt:
        my_list.insert(END, country)


def fillout(e):
    my_entry.delete(0, END)
    my_entry.insert(END, my_list.get(ANCHOR))


my_list.bind("<<ListboxSelect>>", fillout)


def check(e):
    typed = my_entry.get()
    if typed == "":
        data = countries
    else:
        data = []
        for country in countries:

            if typed.lower() in country.lower():
                data.append(country)

    update(data)


my_entry.bind("<KeyRelease>", check)

update(countries)

root.mainloop()
