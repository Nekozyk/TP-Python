import inventaire

info_yaml=inventaire.charger_hotes("hotes.yaml") #chargement du fichier
# print(inventaire.ping("127.0.0.1")) renvoie vrai
# print(inventaire.ping("192.0.2.1",2)) renvoie vrai 1 fois sur 4 car perte de 2 paquets et reception de 2 paquets sur 4
rapport =inventaire.controler_hotes(info_yaml) #utilisation des données pour ping et construction du rapport

print(rapport)
if rapport != False :
    if inventaire.ecrire_rapport(rapport,"rapport.json"):
        print("Le rapport a été crée")
    else:
        print("un erreur est survenue à la création du rapport")