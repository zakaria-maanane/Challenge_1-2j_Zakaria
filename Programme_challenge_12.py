
"""Peitite histoire des Vikings
Ce script affiche une petite histoire des Vikings avec un effet de machine à écrire."""


import time

histoire = """
🛡️ Petite histoire des Vikings

Les Vikings étaient des guerriers, commerçants et explorateurs venus de Scandinavie (Norvège, Suède, Danemark)
entre le VIIIe et le XIe siècle.

Connus pour leurs raids en bateaux appelés drakkars, ils attaquaient les villages et monastères,
mais étaient aussi de grands navigateurs et commerçants.

Ils ont voyagé jusqu'en Islande, au Groenland, et même en Amérique du Nord bien avant Christophe Colomb !

Leur mythologie parlait de dieux puissants comme Odin, Thor ou Loki, et du Valhalla, le paradis des guerriers.

Vers l’an 1000, ils se christianisent peu à peu et cessent les pillages. Mais leur héritage vit encore aujourd’hui.
"""

def effet_machine_à_ecrire(texte, vitesse=0.02):
    for caractere in texte:
        print(caractere, end='', flush=True)
        time.sleep(vitesse)

effet_machine_à_ecrire(histoire)
