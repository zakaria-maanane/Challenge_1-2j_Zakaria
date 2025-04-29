import os
import time

# Représentation du poisson
fish = "<°)))><"

# Largeur du terminal (ajuste si nécessaire)
terminal_width = 80

try:
    while True:
        for i in range(terminal_width - len(fish)):
            print(" " * i + fish, end="\r")
            time.sleep(0.05)
except KeyboardInterrupt:
    print("\nPoisson attrapé ! 🎣")
