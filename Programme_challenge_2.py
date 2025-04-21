'''Challenge 2 17/04/2025 '''

import os
import time
import random
import msvcrt  # pour Windows ; sur Linux/macOS, remplace par 'getch' de 'curses'

# Paramètres du jeu
largeur = 30
personnage = 'O'
saut = '^'
sol = '_'
obstacle = '|'

# Position
pos = 2
en_air = False
score = 0

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def affichage(obstacles, en_air, score):
    ligne = [' '] * largeur
    for i in range(largeur):
        if i in obstacles:
            ligne[i] = obstacle
    if en_air:
        ligne[pos] = saut
    else:
        ligne[pos] = personnage
    print(''.join(ligne))
    print(sol * largeur)
    print(f"Score : {score}")

def collision(obstacles, en_air):
    return pos in obstacles and not en_air

def jeu():
    global en_air, score
    obstacles = []
    tick = 0
    while True:
        clear()

        if tick % 10 == 0:
            if random.random() < 0.4:
                obstacles.append(largeur - 1)

        obstacles = [x - 1 for x in obstacles if x > 0]

        if msvcrt.kbhit():
            touche = msvcrt.getch()
            if touche == b' ' and not en_air:
                en_air = True

        affichage(obstacles, en_air, score)

        if collision(obstacles, en_air):
            print("💥 GAME OVER 💥")
            break

        if en_air:
            time.sleep(0.2)
            en_air = False
        else:
            time.sleep(0.1)

        score += 1
        tick += 1

jeu()
 