
"""Challenge 1 - Jeu PONG en Python """


import os
import time
import random
import keyboard
import threading

# Dimensions du jeu
LARGEUR = 60
HAUTEUR = 20

# Position et taille des raquettes
TAILLE_RAQUETTE = 4
raquette_gauche_y = HAUTEUR // 2 - TAILLE_RAQUETTE // 2
raquette_droite_y = HAUTEUR // 2 - TAILLE_RAQUETTE // 2

# Position et vitesse de la balle
balle_x = LARGEUR // 2
balle_y = HAUTEUR // 2
vitesse_x = 1
vitesse_y = 0.5

# Scores
score_gauche = 0
score_droite = 0

# Contrôle du jeu
en_cours = True
pause = False

def effacer_ecran():
    """Efface l'écran du terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def dessiner_terrain():
    """Dessine le terrain de jeu avec les raquettes, la balle et les scores."""
    global raquette_gauche_y, raquette_droite_y, balle_x, balle_y, score_gauche, score_droite, pause
    
    # Création d'un tableau vide pour le terrain
    terrain = [[' ' for _ in range(LARGEUR)] for _ in range(HAUTEUR)]
    
    # Ajout des bordures
    for x in range(LARGEUR):
        terrain[0][x] = '─'
        terrain[HAUTEUR-1][x] = '─'
    
    # Ajout de la ligne médiane
    for y in range(HAUTEUR):
        if y % 2 == 0:
            terrain[y][LARGEUR // 2] = '┊'
    
    # Ajout des raquettes
    for i in range(TAILLE_RAQUETTE):
        if 0 <= raquette_gauche_y + i < HAUTEUR:
            terrain[raquette_gauche_y + i][1] = '█'
        if 0 <= raquette_droite_y + i < HAUTEUR:
            terrain[raquette_droite_y + i][LARGEUR - 2] = '█'
    
    # Ajout de la balle
    if 0 <= int(balle_y) < HAUTEUR and 0 <= int(balle_x) < LARGEUR:
        terrain[int(balle_y)][int(balle_x)] = '●'
    
    # Affichage du terrain
    effacer_ecran()
    print(f" PONG - Score: {score_gauche} | {score_droite} " + ("- PAUSE" if pause else ""))
    for ligne in terrain:
        print(''.join(ligne))
    print("\nContrôles: Z/S pour raquette gauche, ↑/↓ pour raquette droite, P pour pause, Q pour quitter")

def gestion_entrees():
    """Gère les entrées clavier pour déplacer les raquettes."""
    global raquette_gauche_y, raquette_droite_y, en_cours, pause
    
    while en_cours:
        if not pause:
            # Raquette gauche (touches Z et S)
            if keyboard.is_pressed('z') and raquette_gauche_y > 1:
                raquette_gauche_y -= 1
            if keyboard.is_pressed('s') and raquette_gauche_y < HAUTEUR - TAILLE_RAQUETTE - 1:
                raquette_gauche_y += 1
            
            # Raquette droite (flèches haut et bas)
            if keyboard.is_pressed('up') and raquette_droite_y > 1:
                raquette_droite_y -= 1
            if keyboard.is_pressed('down') and raquette_droite_y < HAUTEUR - TAILLE_RAQUETTE - 1:
                raquette_droite_y += 1
        
        # Pause
        if keyboard.is_pressed('p'):
            pause = not pause
            time.sleep(0.2)  # Éviter les doubles appuis
        
        # Quitter
        if keyboard.is_pressed('q'):
            en_cours = False
        
        time.sleep(0.05)

def mettre_a_jour_balle():
    """Met à jour la position de la balle et gère les collisions."""
    global balle_x, balle_y, vitesse_x, vitesse_y, raquette_gauche_y, raquette_droite_y, score_gauche, score_droite
    
    if not pause:
        # Déplacement de la balle
        balle_x += vitesse_x
        balle_y += vitesse_y
        
        # Collision avec les bords supérieur et inférieur
        if balle_y <= 1 or balle_y >= HAUTEUR - 2:
            vitesse_y = -vitesse_y
        
        # Collision avec la raquette gauche
        if (1 <= balle_x <= 2 and 
            raquette_gauche_y <= balle_y < raquette_gauche_y + TAILLE_RAQUETTE):
            vitesse_x = abs(vitesse_x)
            # Ajustement de l'angle en fonction de l'impact sur la raquette
            impact = (balle_y - raquette_gauche_y) / TAILLE_RAQUETTE
            vitesse_y = 2 * (impact - 0.5)
        
        # Collision avec la raquette droite
        if (LARGEUR - 2 <= balle_x <= LARGEUR - 1 and 
            raquette_droite_y <= balle_y < raquette_droite_y + TAILLE_RAQUETTE):
            vitesse_x = -abs(vitesse_x)
            # Ajustement de l'angle en fonction de l'impact sur la raquette
            impact = (balle_y - raquette_droite_y) / TAILLE_RAQUETTE
            vitesse_y = 2 * (impact - 0.5)
        
        # But marqué
        if balle_x < 0:
            score_droite += 1
            reinitialiser_balle()
        elif balle_x >= LARGEUR:
            score_gauche += 1
            reinitialiser_balle()

def reinitialiser_balle():
    """Réinitialise la position de la balle au centre et lui donne une direction aléatoire."""
    global balle_x, balle_y, vitesse_x, vitesse_y
    
    balle_x = LARGEUR // 2
    balle_y = HAUTEUR // 2
    vitesse_x = 1 if random.random() > 0.5 else -1
    vitesse_y = random.uniform(-0.5, 0.5)
    time.sleep(1)  # Petite pause après un but

def boucle_principale():
    """Boucle principale du jeu."""
    global en_cours
    
    # Démarrage du thread de gestion des entrées
    thread_entrees = threading.Thread(target=gestion_entrees)
    thread_entrees.daemon = True
    thread_entrees.start()
    
    # Boucle de jeu
    while en_cours:
        if not pause:
            mettre_a_jour_balle()
        dessiner_terrain()
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        print("Bienvenue à PONG! Le jeu commence dans 3 secondes...")
        time.sleep(3)
        boucle_principale()
    except KeyboardInterrupt:
        pass 
    finally:
        print("Merci d'avoir joué à PONG!") 