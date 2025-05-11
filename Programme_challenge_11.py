
"""
Ce script permet de gérer une liste de courses simple."""

def afficher_liste(liste):
    if not liste:
        print("Votre liste de courses est vide.")
    else:
        print("Votre liste de courses :")
        for i, item in enumerate(liste, 1):
            print(f"{i}. {item}")

def menu():
    liste_courses = []

    while True:
        print("\nMenu :")
        print("1. Ajouter un article")
        print("2. Supprimer un article")
        print("3. Afficher la liste")
        print("4. Quitter")

        choix = input("Choisissez une option : ")

        if choix == "1":
            article = input("Entrez le nom de l'article à ajouter : ")
            liste_courses.append(article)
            print(f"{article} a été ajouté.")
        elif choix == "2":
            afficher_liste(liste_courses)
            try:
                index = int(input("Entrez le numéro de l'article à supprimer : ")) - 1
                if 0 <= index < len(liste_courses):
                    supprimé = liste_courses.pop(index)
                    print(f"{supprimé} a été supprimé.")
                else:
                    print("Numéro invalide.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")
        elif choix == "3":
            afficher_liste(liste_courses)
        elif choix == "4":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Réessayez.")

menu()
