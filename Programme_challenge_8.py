# Classe représentant une personne
class Personne:
    def __init__(self, nom):
        self.nom = nom

    def se_presenter(self):
        return f"Bonjour, je m'appelle {self.nom}."

# Classe représentant un message envoyé par une personne
class Message:
    def __init__(self, auteur, contenu):
        self.auteur = auteur  # auteur est un objet de type Personne
        self.contenu = contenu

    def afficher(self):
        print(self.auteur.se_presenter())
        print(f"Message : {self.contenu}")

# Utilisation des classes
personne1 = Personne("Zakaria")
message1 = Message(personne1, "Bienvenue dans le monde de la programmation orientée objet en Python !")
message1.afficher()
