############################################################
#               Ecole direct in Python                     #
#               Author : Intermarch3                       #
#               start at : 07/2021                         #
#               End at : work in progress                  #
############################################################

#################### - Import space - ######################

from time import sleep
from functions import *

############################################################

################### - Constant space - #####################

DEBUG = False
DEV = False

############################################################


def main():
    global inst
    if DEV == True:
        user = ''
        mdp = ''
    else:
        user = str(input("Votre nom d'utilisateur :\n>>> "))
        clear_screen()
        mdp = str(input("Votre mot de passe : \n>>> "))
        clear_screen()
    print("Authentification en cours . . .")
    inst = EcoleDirecte(user, mdp, DEBUG)
    clear_screen()
    menu(inst)


def menu(instance):
    print("=====================================- Menu Général -=====================================")
    print("\n1 = demander les devoirs \n2 = demander mes notes \n3 = voir mon agenda\n")
    print("==========================================================================================")
    choice = int(input("Que voulez vous faire ?\n>>> "))
    if choice == 1:
        clear_screen()
        menu_homework(instance)
    elif choice == 2:
        clear_screen()
        menu_grade(instance)
    elif choice == 3:
        clear_screen()
        menu_schredule(instance)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu(instance)


def menu_homework(instance):
    print("===================================- Menu des devoirs -===================================")
    print("\n1 = Devoirs du jour \n2 = Devoirs d'un jour précis \n3 = Devoirs à venir\n4 = retour\n")
    print("==========================================================================================")
    choice = int(input("Que choisie tu ?\n>>> "))
    if choice == 1:
        result = instance.fetch_homework()
        print(result)
    elif choice == 2:
        date = str(input("Quelle est la date du jour (YYYY-MM-DD) :\n>>> "))
        result = instance.fetch_homework(date)
        print(result)
    elif choice == 3:
        clear_screen()
        result = instance.fetch_homework(date_choisie="A_Venir")
    elif choice == 4:
        clear_screen()
        menu(instance)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_homework(instance)


def menu_grade(instance):
    print("====================================- Menu des notes -====================================")
    print("\n1 = Trimestre 1 \n2 = Trimestre 2 \n3 = Trimestre 3\n4 = Moyenne de l'année\n5 = retour\n")
    print("==========================================================================================")
    periode = int(input("Quelle période veut tu observé ?\n>>> "))
    if periode == 1:
        clear_screen()
        print("Note trimestre 1 : ")
    elif periode == 2:
        clear_screen()
        print("Note trimestre 2 : ...")
    elif periode == 3:
        clear_screen()
        print("Note trimestre 3 : ...")
    elif periode == 4:
        print("Moyenne de l'année : ...")
    elif periode == 5:
        clear_screen()
        menu(instance)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_grade(instance)


def menu_schredule(instance):
    print("===================================- Menu de l'agenda -===================================")
    print("\n1 = Agenda de la semaine \n2 = Agenda d'une date précise\n3 = retour\n")
    print("==========================================================================================")
    choice = int(input("Que veut tu observé ?\n>>> "))
    if choice == 1:
        result = instance.fetch_schredule()
        print(result)
    elif choice == 2:
        date_debut = str(input("Quelle est la date du début ?\n>>> "))
        date_fin = str(input("Quelle est la date de la fin ?\n>>> "))
        result = instance.fetch_schredule(date_debut, date_fin)
        print(result)
    elif choice == 3:
        clear_screen()
        menu(instance)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_schredule(instance)


if __name__ == '__main__':
    main()
