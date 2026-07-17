import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox

from plimb_format import create_plimb



images = {
    "mouth_closed":None,
    "mouth_open":None,
    "idle":None
}


background = [0,255,0]



def choose_image(role):

    path = filedialog.askopenfilename(
        filetypes=[
            (
            "PNG",
            "*.png"
            )
        ]
    )

    if path:

        images[role]=path

        labels[role].config(
            text=path
        )



def choose_background():

    global background

    c = colorchooser.askcolor()

    if c[0]:

        background=[
            int(c[0][0]),
            int(c[0][1]),
            int(c[0][2])
        ]

        bg_label.config(
            text=str(background)
        )



def save():

    file = filedialog.asksaveasfilename(
        defaultextension=".plimb",
        filetypes=[
            (
            "PLIMB",
            "*.plimb"
            )
        ]
    )


    if file:

        create_plimb(
            file,
            name.get(),
            images,
            background
        )

        messagebox.showinfo(
            "OK",
            "PLIMB créé"
        )




root=tk.Tk()

root.title(
    "PLIMB Creator"
)

root.geometry(
    "600x500"
)


name=tk.Entry(root)

name.insert(
    0,
    "Mon Chibi"
)

name.pack()



labels={}


for role in images:

    frame=tk.Frame(root)

    frame.pack(
        fill="x"
    )


    tk.Button(
        frame,
        text="Choisir "+role,
        command=lambda r=role:choose_image(r)
    ).pack(
        side="left"
    )


    labels[role]=tk.Label(
        frame,
        text="aucune image"
    )

    labels[role].pack(
        side="left"
    )



tk.Button(
    root,
    text="Changer fond",
    command=choose_background
).pack()


bg_label=tk.Label(
    root,
    text=str(background)
)

bg_label.pack()



tk.Button(
    root,
    text="Créer PLIMB",
    command=save
).pack(
    pady=20
)



root.mainloop()