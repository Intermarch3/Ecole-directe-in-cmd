############################################################
#               Ecole-direct-in-Python                     #
#               Author : Intermarch3                       #
#               start at : 07/2021                         #
#               End at : 02/2022                           #
############################################################

#################### - Import space - ######################

from time import sleep
from functions import *
from base64 import b64decode
from bs4 import BeautifulSoup

################### - Constant space - #####################

APIVERSION = "4.19.0"
DEV = False

############################################################


def main():
    if DEV == True:
        user = ''
        mdp = ''
    else:
        user = str(input("Votre nom d'utilisateur :\n>>> "))
        clear_screen()
        mdp = str(input("Votre mot de passe : \n>>> "))
        clear_screen()
    print("Authentification en cours . . .")
    inst = EcoleDirecte(user, mdp, APIVERSION)
    clear_screen()
    menu(inst)


def menu(instance):
    print("=====================================- Menu Général -=====================================")
    print("\n1 = Devoirs \n2 = Notes \n3 = Agenda \n4 = Quitter \n")
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
        menu_schedule(instance)
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
            print("===========================================================================================")
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
    print("\n1 = Trimestre 1 \n2 = Trimestre 2 \n3 = Trimestre 3\n4 = Notes Annuel\n5 = retour\n")
    print("==========================================================================================")
    periode = int(input("Quelle période veut tu observé ?\n>>> "))
    if periode == 1:
        clear_screen()
        menu_grades_periode(instance, "A001")
    elif periode == 2:
        clear_screen()
        menu_grades_periode(instance, "A002")
    elif periode == 3:
        clear_screen()
        menu_grades_periode(instance, "A003")
    elif periode == 4:
        clear_screen()
        menu_grades_annuel(instance)
    elif periode == 5:
        clear_screen()
        menu(instance)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_grade(instance)


def menu_grades_periode(instance, IDperiode):
    print("====================================- Menu des notes -====================================")
    print("\n1 = Moyenne \n2 = Notes \n3 = retour\n")
    print("==========================================================================================")
    choice = int(input("Que veut tu voire ?\n>>> "))
    clear_screen()
    if choice == 1:
        result = instance.fetch_grades()
        for periode in result['periodes']:
            if periode['idPeriode'] == IDperiode:
                print("====================================- " + periode['periode'] + " -====================================")
                print("\nMoyenne général: ", periode['ensembleMatieres']['moyenneGenerale'])
                print("Moyenne classe: ", periode['ensembleMatieres']['moyenneClasse'])
                print("Moyenne classe minimal: ", periode['ensembleMatieres']['moyenneMin'])
                print("Moyenne classe maximal: ", periode['ensembleMatieres']['moyenneMax'])
                print("")
                for matiere in periode['ensembleMatieres']['disciplines']:
                    if matiere['moyenne'] != "":
                        print("Moyenne en", matiere['discipline'], ": ", matiere['moyenne'], "/ 20")
                    else:
                        print("Moyenne en", matiere['discipline'], "non existante (ou pas de note) !!!")
                print("\n========================================================================" + "=" * len(periode['periode']))
                input("Tape [ENTRER] pour revenir au menu: ")
                clear_screen()
                menu(instance)
    elif choice == 2:
        result = instance.fetch_grades()
        print("====================================- Notes -====================================\n")
        for note in result['notes']:
            if note['codePeriode'] == IDperiode:
                print(note['libelleMatiere'], " [", note['valeur'], "/", note['noteSur'], "]: ", note['devoir'])
        print("\n=================================================================================")
        input("Tape [ENTRER] pour revenir au menu: ")
        clear_screen()
        menu(instance)
    elif choice == 3:
        clear_screen()
        menu_grade(periode)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_grades_periode(periode)



def menu_grades_annuel(instance):
    result = instance.fetch_grades()
    print("====================================- Notes -====================================\n")
    for note in result['notes']:
        print(note['libelleMatiere'], " [", note['valeur'], "/", note['noteSur'], "]: ", note['devoir'])
    print("\n===============================================================================")
    input("Tape [ENTRER] pour revenir au menu: ")
    clear_screen()
    menu(instance)


def menu_schedule(instance):
    print("=============================- Menu exportation de l'agenda -=============================")
    print("\n1 = Exporter agenda de la semaine \n2 = Exporter agenda d'une date précise \n3 = Exporter agenda du jour \n4 = retour \n")
    print("==========================================================================================")
    choice = int(input("Que veut tu faire ?\n>>> "))
    if choice == 1:
        result = instance.fetch_schedule()
        if len(result) > 0:
            export(instance, result)
        else:
            print("Il n'y a pas de cours le(s) jour(s) demandé(s) !!!")
            input("Tape [ENTRER] pour revenir au menu: ")
            clear_screen()
            menu(instance)
    elif choice == 2:
        date_debut = str(input("Quelle est la date du début ? (DD-MM-YYYY) \n>>> "))
        date_fin = str(input("Quelle est la date de la fin ? (DD-MM-YYYY) \n>>> "))
        result = instance.fetch_schedule(date_debut, date_fin)
        if len(result) > 0:
            export(instance, result)
        else:
            print("Il n'y a pas de cours le(s) jour(s) demandé(s) !!!")
            input("Tape [ENTRER] pour revenir au menu: ")
            clear_screen()
            menu(instance)
    elif choice == 3:
        clear_screen()
        result = instance.fetch_schedule(today=True)
        if len(result) > 0:
            export(instance, result)
        else:
            print("Il n'y a pas de cours le(s) jour(s) demandé(s) !!!")
            input("Tape [ENTRER] pour revenir au menu: ")
            clear_screen()
            menu(instance)
    elif choice == 4:
        clear_screen()
        menu(instance)
    else:
        print("Tape un nombre compris dans la liste")
        sleep(1.5)
        clear_screen()
        menu_schedule(instance)


def export(instance, data):
    name = input("Nom du fichier: \n>>> ")
    cal = instance.ScheduleInCalendar(name)
    cal.add_calendar_event(data=data)
    clear_screen()
    cal.export_calendar()
    print("\nFichier créer dans le dossier actuel !!!")
    input("Tape [ENTRER] pour revenir au menu: ")
    clear_screen()
    menu(instance)


if __name__ == '__main__':
    if DEV == True:
        mode = input("Dev mode on (tape off pour le desactiver ou tape [ENTRER] pour continuer)\n>>> ")
        if mode == "off" or mode == "OFF":
            DEV = False
    clear_screen()
    main()
