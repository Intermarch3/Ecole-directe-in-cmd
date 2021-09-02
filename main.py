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

def main():
    clear_screen()
    account_data = login()
    if debug_mode == True:
        print("account data = " + str(account_data))
        print("affichage menu")
    token = account_data['token']
    id = account_data['id']
    menu(token, id)



def menu(account_token, account_id):
    print("=====================================- Menu Général -=====================================")
    print("\n1 = demander les devoirs \n2 = demander mes notes \n3 = voir mon agenda\n")
    print("==========================================================================================")
    choice = int(input("Que voulez vous faire ?\n>>> "))
    if choice == 1:
        clear_screen()
        menu_devoir(account_token, account_id)
    elif choice == 2:
        clear_screen()
        menu_note(account_token, account_id)
    elif choice == 3:
        clear_screen()
        menu_agenda(account_token, account_id)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu(account_token, account_id)


def menu_devoir(account_token, account_id):
    print("===================================- Menu des devoirs -===================================")
    print("\n1 = Devoirs a venir \n2 = Devoirs d'un jour précis\n3 = retour\n")
    print("==========================================================================================")
    choice = int(input("Que choisie tu ?\n>>> "))
    if choice == 1:
        result =fetch_homework(account_token, account_id)
        print(result)
    elif choice == 2:
        date = str(input("Quelle est la date du jour (YYYY-MM-DD) :\n>>> "))
        result = fetch_homework(account_token, account_id, date)
        print(result)
    elif choice == 3:
        clear_screen()
        menu(account_token, account_id)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_devoir(account_token, account_id)


def menu_note(account_token, account_id):
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
        print("Moyenne de l'anné : ...")
    elif periode == 5:
        clear_screen()
        menu(account_token, account_id)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_note(account_token, account_id)


def menu_agenda(account_token, account_id):
    print("===================================- Menu de l'agenda -===================================")
    print("\n1 = Agenda de la semaine \n2 = Agenda d'une date précise\n3 = retour\n")
    print("==========================================================================================")
    choice = int(input("Que veut tu observé ?\n>>> "))
    if choice == 1:
        result = fetch_emploi_du_temps(account_token, account_id)
        print(result)
    elif choice == 2:
        date_debut = str(input("Quelle est la date du début ?\n>>> "))
        date_fin = str(input("Quelle est la date de la fin ?\n>>> "))
        result = fetch_emploi_du_temps(account_token, account_id, date_debut, date_fin)
        print(result)
    elif choice == 3:
        clear_screen()
        menu(account_token, account_id)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_agenda(account_token, account_id)


if __name__ == '__main__':
    main()