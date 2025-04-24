"""Challenge 5 Jeux de précision 

Clique sur ON pour commencer le jeu.

Clique à nouveau n’importe où dans la fenêtre pour "lancer".

Le but est d’arrêter la barre bleue dans la zone rouge (zone de précision).

Clique sur OFF pour arrêter le jeu."""

import pygame
import sys

# Initialisation
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("===Jeu de précision===")
clock = pygame.time.Clock()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)

# États
game_on = False
bar_x = 100
bar_speed = 5
bar_direction = 1

# Boutons
font = pygame.font.SysFont(None, 36)
def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    label = font.render(text, True, WHITE)
    screen.blit(label, (x + 10, y + 10))
    return pygame.Rect(x, y, w, h)

# Boucle principale
while True:
    screen.fill(WHITE)
    
    # Boutons ON/OFF
    on_button = draw_button("ON", 50, 30, 100, 50, GREEN)
    off_button = draw_button("OFF", 450, 30, 100, 50, RED)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if on_button.collidepoint(event.pos):
                game_on = True
            elif off_button.collidepoint(event.pos):
                game_on = False
            elif game_on:
                # Lorsque le joueur clique pour "lancer"
                if 290 < bar_x < 310:
                    print("🎯 Parfait !")
                else:
                    print("❌ Raté...")

    if game_on:
        # Affichage de la zone cible
        pygame.draw.rect(screen, RED, (300 - 10, 200, 20, 40))

        # Barre mobile
        pygame.draw.rect(screen, BLUE, (bar_x, 200, 10, 40))
        bar_x += bar_speed * bar_direction
        if bar_x <= 100 or bar_x >= 500:
            bar_direction *= -1

    pygame.display.flip()
    clock.tick(60)
