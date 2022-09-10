############################################################
#               Ecole direct in Python                     #
#               Author : Intermarch3                       #
#               start at : 07/2021                         #
#               End at : work in progress                  #
############################################################

#################### - Import space - ######################

from time import sleep
import requests as rqs
import os, sys
import platform 
from datetime import date, datetime, timedelta 
from base64 import b64decode
from bs4 import BeautifulSoup

############################################################
DEBUG = True
DEV = True


def clear_screen():                                     # clear the terminal screen
        if platform.system() == "Windows":
            command = "cls"
        else: 
            command = "clear"
        os.system(command)


class EcoleDirecte:
    """
    
    """
    def __init__(self, user, password, debug_mode=False):
        self.user = user
        self.password = password
        self.token = ""
        self.debug_mode = debug_mode
        data = 'data={\n\t\"uuid\": \"\",\n\t\"identifiant\": \"' + self.user + '\",\n\t\"motdepasse\": \"' + self.password + '\"\n}'
        headers = {
            'authority': 'api.ecoledirecte.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-gpc': '1',
            'origin': 'https://www.ecoledirecte.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.ecoledirecte.com/',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        url = "https://api.ecoledirecte.com/v3/login.awp?v=4.17.10"
        response = rqs.post(url=url, data=data, headers=headers).json()      # post a request with data in body and make the response in a json file
        if debug_mode == True:
            print(response['token'])
        if response['code'] == 200:
            print("Authentification réussi !!!\n")
            self.token = response['token']
            self.id = response['data']['accounts'][0]['id']
            self.email = response['data']['accounts'][0]['email']
        elif response['code'] == 505:
            print("Nom d'utilisateur ou mot de passe invalide !!!\n\n")
            sys.exit()
        else:
            print("Erreur " + str(response['code']) + " : " + str(response['message']))

    def fetch_homework(self, date_choisie=None):               # get the list of homework
        data = 'data={\n\t\"token\": \"' + self.token + '\"\n}'
        if date_choisie == None:
            date_iso = datetime.now()
            date_today = datetime.strftime(date_iso, '%d-%m-%Y')
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte' + str(date_today) + '.awp?verbe=get'
            response = rqs.post(url, data).json()
            data = response['data']
            if self.debug_mode == True:
                print(data)
        elif date_choisie == 'A_Venir':
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte.awp?verbe=get'
            response = rqs.post(url=url, data=data).json()
            data = response['data']
            if self.debug_mode == True:
                print(data)
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
            self.token = response['token']
            data = 'data={\n\t\"token\": \"' + str(self.token) + '\"\n}'
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte/' + str(date_devoir) + '.awp?verbe=get&'
            response = rqs.post(url=url, data=data).json()
            clear_screen()
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
            self.token = response['token']
            clear_screen()
            menu(self)
        else:
            date = datetime.strftime(date_choisie, '%d-%m-%Y')
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte/' + str(date) + '.awp?verbe=get&'
            response = rqs.post(url=url, data=data).json()
            if response['code'] == 200:
                print(response['data'][0])
                return response
            else:
                print('erreur ' + str(response['code']) + '\t message : ' + str(response['message']))

    def fetch_schredule(self, date_debut=None, date_fin=None):   # get the planning of the week
        if date_debut or date_fin == None:
            day_iso = date.today()
            day_str = datetime.strftime(day_iso, '%d-%m-%Y')
            day_obj = datetime.strptime(day_str, '%d-%m-%Y')
            date_debut = day_obj - timedelta(days=day_obj.weekday())
            date_fin = date_debut + timedelta(days=5)
            print("Demande de l'emploi du temps de la semaine ( du " + str(date_debut) + " au " + str(date_fin) + " )")
            data = 'data={"dateDebut": "' + str(date_debut) + '", "dateFin": "' + str(date_fin) + '", "avecTrous": false, "token": "' + str(self.token) + '"}'
            url = "https://api.ecoledirecte.com/v3/E/" + str(self.id) + "/EmploiDuTemps.awp?verbe=get&"
            response = rqs.post(url, data).json()
            return response
        else:
            print("Demande de l'emploi du temps ( du " + str(date_debut) + " au " + str(date_fin) + " )")
            data = 'data={"dateDebut": "' + str(date_debut) + '", "dateFin": "' + str(date_fin) + '", "avecTrous": false, "token": "' + str(self.token) + '"}'
            url = "https://api.ecoledirecte.com/v3/E/" + str(id) + "/EmploiDuTemps.awp?verbe=get&"
            response = rqs.post(url, data).json()
            return response


#####- Menus -#####

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