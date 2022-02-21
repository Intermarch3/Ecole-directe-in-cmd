############################################################
#               Ecole direct in Python                     #
#               Author : Intermarch3                       #
#               start at : 07/2021                         #
#               End at : work in progress                  #
############################################################

#################### - Import space - ######################

from function import *
from time import sleep

############################################################
debug_mode = False
dev_mod = True
token = ""
id = 0

'''
a faire :
finir fetch_devoir:
    erreur avec .json sur plusieur options
agenda: 
    faire fichier a importer dans calendrier
note :
    faire tous
peut etre bug ailleur a voir
'''

def main():
    global token, id
    clear_screen()
    account_data = login()
    if debug_mode == True:
        print("account data = " + str(account_data))
        print("affichage menu")
    token = account_data['token']
    id = account_data['id']
    menu()


def menu():
    print("=====================================- Menu Général -=====================================")
    print("\n1 = demander les devoirs \n2 = demander mes notes \n3 = voir mon agenda\n")
    print("==========================================================================================")
    choice = int(input("Que voulez vous faire ?\n>>> "))
    if choice == 1:
        clear_screen()
        menu_devoir()
    elif choice == 2:
        clear_screen()
        menu_note()
    elif choice == 3:
        clear_screen()
        menu_agenda()
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu()


def menu_devoir():
    print("===================================- Menu des devoirs -===================================")
    print("\n1 = Devoirs du jour \n2 = Devoirs d'un jour précis \n3 = Devoirs à venir\n4 = retour\n")
    print("==========================================================================================")
    choice = int(input("Que choisie tu ?\n>>> "))
    if choice == 1:
        result = fetch_devoirs()
        print(result)
    elif choice == 2:
        date = str(input("Quelle est la date du jour (YYYY-MM-DD) :\n>>> "))
        result = fetch_devoirs(date)
        print(result)
    elif choice == 3:
        clear_screen()
        result = fetch_devoirs(date_choisie="A_Venir")
    elif choice == 4:
        clear_screen()
        menu()
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_devoir()


def menu_note():
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
        menu()
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_note()


def menu_agenda():
    print("===================================- Menu de l'agenda -===================================")
    print("\n1 = Agenda de la semaine \n2 = Agenda d'une date précise\n3 = retour\n")
    print("==========================================================================================")
    choice = int(input("Que veut tu observé ?\n>>> "))
    if choice == 1:
        result = fetch_emploi_du_temps()
        print(result)
    elif choice == 2:
        date_debut = str(input("Quelle est la date du début ?\n>>> "))
        date_fin = str(input("Quelle est la date de la fin ?\n>>> "))
        result = fetch_emploi_du_temps(date_debut, date_fin)
        print(result)
    elif choice == 3:
        clear_screen()
        menu()
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_agenda()


if __name__ == '__main__':
    main()