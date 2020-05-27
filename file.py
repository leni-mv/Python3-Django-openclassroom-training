# -*-coding utf8 -*-
#!bin/python3.8

Citations = {"Kakashi" : "Dans ce monde, il y a des enfants plus jeune que toi qui sont plus doué que moi.",
            "Gay" : "Tous tes efforts ne servirons à rien si tu ne crois pas vraiment en toi.",
            "Gaara" : "Détrompes-toi. On peut être conscient de cette noirceur et la préférer à la solitude.."
}
personnages = [
    "Kakashi",
    "Gaara",
    "Gay",
    "Shino"]

personnage = input("Dis-moi mon nom est je te dirais ce que je pense : ")

if personnage == "Gaara" :
    print(Gaara_citation)
elif personnage == "Gay" :
    print(Gay_citation)
else:
    print('Le paradis des citations ferme boutique, salut ^^')

