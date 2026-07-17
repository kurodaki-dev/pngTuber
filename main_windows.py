import tkinter as tk
from tkinter import filedialog
import pygame
from PIL import Image
import sounddevice as sd
import numpy as np
import random
import json
import os

CONFIG_FILE = "config_pngtuber.json"

def save_config(paths):
    with open(CONFIG_FILE, "w") as f:
        json.dump(paths, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

# Sélection des images
config = load_config()
root = tk.Tk()
root.withdraw()

img_paths = {}
labels = [
    ("closed_open", "Bouche FERMÉE / Yeux OUVERTS"),
    ("open_open", "Bouche OUVERTE / Yeux OUVERTS"),
    ("closed_closed", "Bouche FERMÉE / Yeux FERMÉS (Optionnel)")
]

for key, label in labels:
    if key in config and os.path.exists(config[key]):
        img_paths[key] = config[key]
    else:
        print(f"Sélectionnez : {label}")
        path = filedialog.askopenfilename(filetypes=[("PNG", "*.png")])
        if path:
            img_paths[key] = path

root.destroy()
save_config(img_paths)

# Initialisation Pygame
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PNGTuber Pro - Windows")
FONT = pygame.font.SysFont("Arial", 16)

def load_img(path):
    if not path: return None
    img = Image.open(path).convert("RGBA")
    img = img.resize((WIDTH, HEIGHT))
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

closed_idle = load_img(img_paths.get("closed_open"))
opened_talk = load_img(img_paths.get("open_open"))
closed_blink = load_img(img_paths.get("closed_closed")) or closed_idle

# Paramètres
OPEN_THRESHOLD = 0.03
VOLUME_CURRENT = 0.0
mouth_open = False
current_bg = (0, 255, 0) # Fond vert par défaut

# Animations
bounce_y = 0
bounce_speed = 0
is_blinking = False
blink_timer = random.randint(120, 240)
blink_duration = 0

def audio_callback(indata, frames, time, status):
    global VOLUME_CURRENT, mouth_open
    VOLUME_CURRENT = np.sqrt(np.mean(indata ** 2))
    if not mouth_open and VOLUME_CURRENT > OPEN_THRESHOLD:
        mouth_open = True
    elif mouth_open and VOLUME_CURRENT < (OPEN_THRESHOLD * 0.6):
        mouth_open = False

stream = sd.InputStream(channels=1, callback=audio_callback)
stream.start()

clock = pygame.time.Clock()
running = True

while running:
    W, H = screen.get_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                current_bg = (30, 30, 30) if current_bg == (0, 255, 0) else (0, 255, 0)
            elif event.key == pygame.K_UP:
                OPEN_THRESHOLD = max(0.005, OPEN_THRESHOLD - 0.005)
            elif event.key == pygame.K_DOWN:
                OPEN_THRESHOLD = min(0.5, OPEN_THRESHOLD + 0.005)

    # Logique Clignement
    if not is_blinking:
        blink_timer -= 1
        if blink_timer <= 0:
            is_blinking = True
            blink_duration = 6
    else:
        blink_duration -= 1
        if blink_duration <= 0:
            is_blinking = False
            blink_timer = random.randint(120, 300)

    # Logique de Rebond (Bounce) quand il parle
    if mouth_open:
        current_avatar = opened_talk
        bounce_speed += 1
        bounce_y = abs(int(np.sin(bounce_speed * 0.4) * 15)) # Effet de saut de 15 pixels max
    else:
        current_avatar = closed_blink if is_blinking else closed_idle
        bounce_y = 0
        bounce_speed = 0

    screen.fill(current_bg)
    
    if current_avatar:
        scaled = pygame.transform.smoothscale(current_avatar, (W, H))
        # Si le personnage ne parle pas, on peut lui appliquer une légère transparence (optionnel)
        if not mouth_open:
            scaled.set_alpha(220) # Légèrement plus sombre/effacé au repos
        else:
            scaled.set_alpha(255)
        screen.blit(scaled, (0, -bounce_y))

    # UI info
    text_color = (0, 0, 0) if current_bg == (0, 255, 0) else (255, 255, 255)
    ui_text = f"Seuil: {round(OPEN_THRESHOLD, 3)} | Vol: {round(VOLUME_CURRENT, 3)} | Fond [G]"
    screen.blit(FONT.render(ui_text, True, text_color), (10, 10))

    pygame.display.flip()
    clock.tick(60)

stream.stop()
stream.close()
pygame.quit()
