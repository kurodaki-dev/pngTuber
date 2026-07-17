import pygame
import random

# Sur Android, on charge des images fixes situées dans le dossier de l'application
# Nomme tes images exactement comme ça dans ton dossier de build
IMG_CLOSED = "avatar_closed.png"
IMG_OPEN = "avatar_open.png"

pygame.init()
pygame.font.init()

# Récupération de la taille de l'écran du smartphone
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PNGTuber Mobile")
FONT = pygame.font.SysFont("Arial", 24)

def load_img(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except:
        # Surface de secours si l'image n'est pas encore là
        surf = pygame.Surface((400, 400), pygame.SRCALPHA)
        pygame.draw.circle(surf, (200, 50, 50), (200, 200), 150)
        return surf

closed_idle = load_img(IMG_CLOSED)
opened_talk = load_img(IMG_OPEN)

current_bg = (0, 255, 0) # Fond vert pour overlay mobile
mouth_open = False
is_blinking = False
blink_timer = random.randint(120, 240)
blink_duration = 0

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Gestion du tactile sur Android
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouth_open = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouth_open = False

    # Clignement automatique
    if not is_blinking:
        blink_timer -= 1
        if blink_timer <= 0:
            is_blinking = True
            blink_duration = 8
    else:
        blink_duration -= 1
        if blink_duration <= 0:
            is_blinking = False
            blink_timer = random.randint(120, 300)

    # Assignation de l'image
    if mouth_open:
        current_avatar = opened_talk
    else:
        current_avatar = closed_idle

    screen.fill(current_bg)
    
    # Centre et adapte l'avatar à l'écran du téléphone
    if current_avatar:
        scaled = pygame.transform.smoothscale(current_avatar, (WIDTH, WIDTH))
        screen.blit(scaled, (0, (HEIGHT - WIDTH) // 2))

    # Affichage d'une aide visuelle pour le streamer sur mobile
    txt = FONT.render("Maintenez l'écran pour parler", True, (0, 0, 0))
    screen.blit(txt, (20, 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
