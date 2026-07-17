import tkinter as tk
from tkinter import filedialog, colorchooser

import pygame
from PIL import Image
import sounddevice as sd
import numpy as np

import threading
import zipfile
import json
import os


# ==========================
# VARIABLES GLOBALES
# ==========================

WIDTH = 800
HEIGHT = 800

closed_img = None
opened_img = None
current_img = None

background_color = (0, 255, 0)

open_threshold = 0.03

mouth_open = False

running = True


# ==========================
# CHARGEMENT IMAGE
# ==========================

def load_image(path):

    img = Image.open(path).convert("RGBA")

    img = img.resize(
        (WIDTH, HEIGHT)
    )

    return pygame.image.fromstring(
        img.tobytes(),
        img.size,
        img.mode
    )


# ==========================
# CHARGEMENT PLIMB
# ==========================

def load_plimb():

    global closed_img
    global opened_img

    path = filedialog.askopenfilename(
        filetypes=[
            ("PNG Tuber Mod", "*.plimb")
        ]
    )

    if not path:
        return


    temp = "plimb_temp"


    if os.path.exists(temp):
        import shutil
        shutil.rmtree(temp)


    os.mkdir(temp)


    with zipfile.ZipFile(path,"r") as z:
        z.extractall(temp)


    config = os.path.join(
        temp,
        "plimb.json"
    )


    if os.path.exists(config):

        with open(config,"r") as f:
            data=json.load(f)


        if "mouth_closed" in data:
            closed_img = load_image(
                os.path.join(
                    temp,
                    data["mouth_closed"]
                )
            )


        if "mouth_open" in data:
            opened_img = load_image(
                os.path.join(
                    temp,
                    data["mouth_open"]
                )
            )


    print("PLIMB chargé :",path)



# ==========================
# MICRO
# ==========================

def audio_callback(
    indata,
    frames,
    time,
    status
):

    global mouth_open
    global current_img


    volume = np.sqrt(
        np.mean(
            indata ** 2
        )
    )


    if volume > open_threshold:

        mouth_open=True

    else:

        mouth_open=False


    if mouth_open:

        current_img=opened_img

    else:

        current_img=closed_img



def start_micro():

    stream = sd.InputStream(
        channels=1,
        callback=audio_callback
    )

    stream.start()

    return stream



# ==========================
# FENETRE TKINTER
# ==========================


def change_sensitivity(value):

    global open_threshold

    open_threshold=float(value)



def change_background():

    global background_color

    color=colorchooser.askcolor()

    if color[0]:

        background_color=(
            int(color[0][0]),
            int(color[0][1]),
            int(color[0][2])
        )



root=tk.Tk()

root.title(
    "PNGTuber Control"
)

root.geometry(
    "350x300"
)



btn=tk.Button(
    root,
    text="Charger un PLIMB",
    command=load_plimb
)

btn.pack(
    pady=20
)



tk.Label(
    root,
    text="Sensibilité micro"
).pack()



slider=tk.Scale(
    root,
    from_=0.001,
    to=0.2,
    resolution=0.001,
    orient="horizontal",
    command=change_sensitivity
)

slider.set(
    open_threshold
)

slider.pack()



tk.Button(
    root,
    text="Changer le fond",
    command=change_background
).pack(
    pady=20
)



# ==========================
# THREAD PYGAME
# ==========================


def pygame_window():


    global current_img


    pygame.init()


    screen=pygame.display.set_mode(
        (
            WIDTH,
            HEIGHT
        )
    )


    pygame.display.set_caption(
        "PNGTuber"
    )


    clock=pygame.time.Clock()



    while running:


        for event in pygame.event.get():

            if event.type==pygame.QUIT:

                pygame.quit()
                return



        screen.fill(
            background_color
        )


        if current_img:

            screen.blit(
                current_img,
                (0,0)
            )


        pygame.display.flip()


        clock.tick(60)



# ==========================
# DEMARRAGE
# ==========================


stream=start_micro()


threading.Thread(
    target=pygame_window,
    daemon=True
).start()



root.mainloop()



stream.stop()
stream.close()

pygame.quit()