############################################################
#               Ecole direct in Python                     #
#               Author : Intermarch3                       #
#               start at : 07/2021                         #
#               End at : work in progress                  #
############################################################

#################### - Import space - ######################

import requests as rqs
import os 
import platform 
from datetime import date, datetime, timedelta 
from main import debug_mode, dev_mod, menu, token, id
from base64 import b64decode
from bs4 import BeautifulSoup

'''
a faire :
finir fetch_devoir:
    verifier option 1 et 2
agenda: 
    faire fichier a importer dans calendrier
    verifier le reste
note :
    faire tous
peut etre bug ailleur a voir
'''

def clear_screen():                                     # clear the terminal screen
        if platform.system() == "Windows":
            command = "cls"
        else: 
            command = "clear"
        os.system(command)


def login():                                            # log with your user and password to get token and information
    if dev_mod == True:
        user = ''
        mdp = ''
    else:
        user = str(input("Votre nom d'utilisateur :\n>>> "))
        clear_screen()
        mdp = str(input("Votre mot de passe : \n>>> "))
        clear_screen()
    print("Authentification en cours . . .")
    data = 'data={\n\t\"identifiant\": \"' + user + '\",\n\t\"motdepasse\": \"' + mdp + '\"\n}'
    url = "https://api.ecoledirecte.com/v3/login.awp"
    response = rqs.post(url=url, data=data).json()      # post a request with data in body and make the response in a json file
    if debug_mode == True:
        print(response)
    if response['code'] == 200:
        print("Authentification réussi !!!\n")
        account_data = {                                        # make an array with the response information
            'token' : response['token'],
            'id' : response['data']['accounts'][0]['id'],
            'email': response['data']['accounts'][0]['email'],
        }
        return account_data
    elif response['code'] == 505:
        print("Nom d'utilisateur ou mot de passe invalide !!!\n\n")
        login()
    else:
        print("Erreur " + str(response['code']) + " : " + str(response['message']))


def fetch_devoirs(date_choisie=None):               # get the list of homework
    global token, id
    data = 'data={\n\t\"token\": \"' + str(token) + '\"\n}'
    if date_choisie == None:
        date_iso = datetime.now()
        date_today = datetime.strftime(date_iso, '%d-%m-%Y')
        url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(id) + '/cahierdetexte' + str(date_today) + '.awp?verbe=get'
        response = rqs.post(url, data).json()
        data = response['data']
        if debug_mode == True:
            print(data)
    elif date_choisie == 'A_Venir':
        url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(id) + '/cahierdetexte.awp?verbe=get'
        response = rqs.post(url=url, data=data).json()
        data = response['data']
        if debug_mode == True:
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
        token = response['token']
        data = 'data={\n\t\"token\": \"' + str(token) + '\"\n}'
        url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(id) + '/cahierdetexte/' + str(date_devoir) + '.awp?verbe=get&'
        response = rqs.post(url=url, data=data).json()
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
        token = response['token']
        clear_screen()
        menu()
    else:
        date = datetime.strftime(date_choisie, '%d-%m-%Y')
        url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(id) + '/cahierdetexte/' + str(date) + '.awp?verbe=get&'
        response = rqs.post(url=url, data=data).json()
        if response['code'] == 200:
            print(response['data'][0])
            return response
        else:
            print('erreur ' + str(response['code']) + '\t message : ' + str(response['message']))



def fetch_emploi_du_temps(date_debut=None, date_fin=None):   # get the planning of the week
    global token, id
    if date_debut or date_fin == None:
        day_iso = date.today()
        day_str = datetime.strftime(day_iso, '%d-%m-%Y')
        day_obj = datetime.strptime(day_str, '%d-%m-%Y')
        date_debut = day_obj - timedelta(days=day_obj.weekday())
        date_fin = date_debut + timedelta(days=5)
        print("Demande de l'emploi du temps de la semaine ( du " + str(date_debut) + " au " + str(date_fin) + " )")
        data = 'data={"dateDebut": "' + str(date_debut) + '", "dateFin": "' + str(date_fin) + '", "avecTrous": false, "token": "' + str(token) + '"}'
        url = "https://api.ecoledirecte.com/v3/E/" + str(id) + "/EmploiDuTemps.awp?verbe=get&"
        response = rqs.post(url, data).json()
        return response
    else:
        print("Demande de l'emploi du temps ( du " + str(date_debut) + " au " + str(date_fin) + " )")
        data = 'data={"dateDebut": "' + str(date_debut) + '", "dateFin": "' + str(date_fin) + '", "avecTrous": false, "token": "' + str(token) + '"}'
        url = "https://api.ecoledirecte.com/v3/E/" + str(id) + "/EmploiDuTemps.awp?verbe=get&"
        response = rqs.post(url, data).json()
        return response

