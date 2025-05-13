class AffichePrenoms:
    def __init__(self, prenoms):
        self.prenoms = prenoms

    def afficher(self):
        for prenom in self.prenoms:
            print(prenom)

# Exemple d'utilisation
liste_prenoms = ["Alice", "Léo", "Sophie", "Mehdi"]
afficheur = AffichePrenoms(liste_prenoms)
afficheur.afficher()
