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
from main import debug_mode

############################################################


def clear_screen():                                     # clear the terminal screen
        if platform.system() == "Windows":
            command = "cls"
        else: 
            command = "clear"
        os.system(command)


def login():                                            # log with your user and password to get token and information
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


def fetch_homework(token, id, date=None):               # get the list of homework
    data = 'data={\n\t\"token\": \"' + str(token) + '\"\n}'
    if date == None:
        url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(id) + '/cahierdetexte.awp?verbe=get'
    else:
        url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(id) + '/cahierdetexte/' + str(date) + '.awp?verbe=get&'
    response = rqs.post(url=url, data=data).json()
    if response['code'] == 200:
        return response
    else:
        print('erreur ' + str(response['code']) + '\t message : ' + str(response['message']))


def fetch_emploi_du_temps(token, id, date_debut=None, date_fin=None):   # get the planning of the week
    if date_debut or date_fin == None:
        day_iso = date.today()
        day_str = datetime.strftime(day_iso, '%d-%m-%Y')
        day_obj = datetime.strptime(day_str, '%d-%m-%Y')
        date_debut = day_obj - timedelta(days=day_obj.weekday())
        date_fin = date_debut + timedelta(days=5)
        data = 'data={"dateDebut": "' + str(date_debut) + '", "dateFin": "' + str(date_fin) + '", "avecTrous": false, "token": "' + str(token) + '"}'
        url = "https://api.ecoledirecte.com/v3/E/" + str(id) + "/EmploiDuTemps.awp?verbe=get&"
        response = rqs.post(url, data).json()
        return response
    else:
        data = 'data={"dateDebut": "' + str(date_debut) + '", "dateFin": "' + str(date_fin) + '", "avecTrous": false, "token": "' + str(token) + '"}'
        url = "https://api.ecoledirecte.com/v3/E/" + str(id) + "/EmploiDuTemps.awp?verbe=get&"
        response = rqs.post(url, data).json()
        return response

