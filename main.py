############################################################
#               Ecole-direct-in-Python                     #
#               Author : Intermarch3                       #
#               start at : 07/2021                         #
#               End at : work in progress                  #
############################################################

#################### - Import space - ######################

from time import sleep
from functions import *

################### - Constant space - #####################

DEV = True

############################################################


def main():
    global inst
    if DEV == True:
        user = 'lucasleclerc74@gmail.com'
        mdp = 'Lulu-ecoledirect-74'
    else:
        user = str(input("Votre nom d'utilisateur :\n>>> "))
        clear_screen()
        mdp = str(input("Votre mot de passe : \n>>> "))
        clear_screen()
    print("Authentification en cours . . .")
    inst = EcoleDirecte(user, mdp)
    clear_screen()
    menu(inst)


def menu(instance):
    print("=====================================- Menu Général -=====================================")
    print("\n1 = demander les devoirs \n2 = demander mes notes \n3 = voir mon agenda \n4 = Quitter \n")
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
    elif choice == 4:
        clear_screen()
        exit()
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
    # devoir du jour
    if choice == 1:
        date, response = instance.fetch_homework()
        if len(response['matieres']) == 0:
            print("Il n'y a aucun devoir le", date, ". C'est la fête !!!")
        else:
            print("================================- Devoirs le ", date_devoir, " -================================")
            for i in range(len(response['data']['matieres'])):
                if response['data']['matieres'][i]['aFaire']['effectue'] == True:
                    print("\n", response['data']['matieres'][i]['matiere'], ":   [X]")
                else:
                    print("\n", response['data']['matieres'][i]['matiere'], ":   [ ]")
                contenu = b64decode(response['data']['matieres'][i]['aFaire']['contenu'])
                contenu_soup = BeautifulSoup(contenu, 'html.parser')
                print(" A faire:\n", contenu_soup.get_text())
            print("\n===========================================================================================")
        input("Tape [ENTRER] pour revenir au menu: ")
        clear_screen()
        menu(instance)
    # devoir d'un jour donner
    elif choice == 2:
        date = str(input("Quelle est la date du jour (DD-MM-YYYY) :\n>>> "))
        date = datetime.strptime(date, '%d-%m-%Y')
        date = date.strftime("%Y-%m-%d")
        response = instance.fetch_homework(date)
        if len(response['matieres']) == 0:
            print("Il n'y a aucun devoir le", date, ". C'est la fête !!!")
        else:
            print("================================- Devoirs le ", date, " -================================")
            for i in range(len(response['matieres'])):
                try:
                    if response['matieres'][i]['aFaire']['effectue'] == True:
                        print("\n", response['matieres'][i]['matiere'], ":   [X]")
                    else:
                        print("\n", response['matieres'][i]['matiere'], ":   [ ]")
                    contenu = b64decode(response['matieres'][i]['aFaire']['contenu'])
                    contenu_soup = BeautifulSoup(contenu, 'html.parser')
                    print(" A faire:\n", contenu_soup.get_text())
                except:
                    pass
            print("\n===========================================================================================")
        input("Tape [ENTRER] pour revenir au menu: ")
        clear_screen()
        menu(instance)
    # devoir a venir
    elif choice == 3:
        clear_screen()
        data = instance.fetch_homework(date_choisie="A_venir")
        # affiche les devoirs a venir
        print("===================================- Devoirs à venir -====================================")
        for jour in data:
            date = datetime.strptime(jour, '%Y-%m-%d')
            date = date.strftime("%d-%m-%Y")
            print("\n", date, ": ")
            for i in range(len(data[jour])):
                if data[jour][i]['effectue'] == False:
                    print("\t", data[jour][i]['matiere'], ": Effectué: [ ]")
                else:
                    print("\t", data[jour][i]['matiere'], ": Effectué: [X]")
        print("\n==========================================================================================")
        date_devoir = input("Quelle jour veut tu voir le contenu des devoirs ? (DD-MM-YYYY)\n>>> ")
        date_devoir = datetime.strptime(date_devoir, '%d-%m-%Y')
        date_devoir = date_devoir.strftime("%Y-%m-%d")
        response = instance.fetch_homework(date_choisie=date_devoir)
        clear_screen()
        # affiche le contenu des devoirs du jour demander
        if len(response['matieres']) == 0:
            print("Il n'y a aucun devoir le", date, ". C'est la fête !!!")
        else:
            print("================================- Devoirs le ", date, " -================================")
            for i in range(len(response['matieres'])):
                try:
                    if response['matieres'][i]['aFaire']['effectue'] == True:
                        print("\n", response['matieres'][i]['matiere'], ":   [X]")
                    else:
                        print("\n", response['matieres'][i]['matiere'], ":   [ ]")
                    contenu = b64decode(response['matieres'][i]['aFaire']['contenu'])
                    contenu_soup = BeautifulSoup(contenu, 'html.parser')
                    print(" A faire:\n", contenu_soup.get_text())
                except:
                    pass
            print("\n===========================================================================================")
        input("Tape [ENTRER] pour revenir au menu: ")
        clear_screen()
        menu(instance)
    # quitter
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
