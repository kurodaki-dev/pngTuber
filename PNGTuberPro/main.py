import tkinter as tk
from tkinter import filedialog,colorchooser

import pygame
import sounddevice as sd
import numpy as np

from PIL import Image

from plimb_loader import Plimb
from settings import settings



WIDTH=800
HEIGHT=800



pygame.init()


screen=pygame.display.set_mode(
    (WIDTH,HEIGHT)
)

pygame.display.set_caption(
    "PNGTuber Pro"
)



plimb=None


closed=None
opened=None


current=None



def pil_to_surface(img):

    return pygame.image.fromstring(
        img.tobytes(),
        img.size,
        img.mode
    )



def load_plimb():

    global plimb
    global closed
    global opened
    global current


    path=filedialog.askopenfilename(
        filetypes=[
            (
            "PLIMB",
            "*.plimb"
            )
        ]
    )


    if path:


        plimb=Plimb(path)


        settings.background=tuple(
            plimb.get_background()
        )


        c=plimb.load_image(
            "mouth_closed",
            (WIDTH,HEIGHT)
        )

        o=plimb.load_image(
            "mouth_open",
            (WIDTH,HEIGHT)
        )


        if c:
            closed=pil_to_surface(c)

        if o:
            opened=pil_to_surface(o)


        current=closed




def change_background():

    color=colorchooser.askcolor()

    if color[0]:

        settings.background=(
            int(color[0][0]),
            int(color[0][1]),
            int(color[0][2])
        )





root=tk.Tk()

root.title(
    "PNGTuber Control"
)


root.geometry(
    "350x200"
)



tk.Button(
    root,
    text="Charger PLIMB",
    command=load_plimb
).pack(
    pady=10
)



tk.Button(
    root,
    text="Changer fond",
    command=change_background
).pack()



root.mainloop()



mouth=False



def audio_callback(indata,frames,time,status):

    global mouth
    global current


    volume=np.sqrt(
        np.mean(
            indata**2
        )
    )


    volume*=settings.volume_boost



    if not mouth and volume>settings.open_threshold:

        mouth=True


    elif mouth and volume<settings.close_threshold:

        mouth=False



    if mouth and opened:

        current=opened

    elif closed:

        current=closed





stream=sd.InputStream(
    channels=1,
    callback=audio_callback
)

stream.start()



clock=pygame.time.Clock()


running=True


while running:


    for event in pygame.event.get():

        if event.type==pygame.QUIT:

            running=False



    screen.fill(
        settings.background
    )


    if current:

        screen.blit(
            current,
            (0,0)
        )


    pygame.display.flip()


    clock.tick(60)



stream.stop()

pygame.quit()