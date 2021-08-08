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
# for sending email :
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

############################################################


def clear_screen():                                     # clear the terminal screen
        if platform.system() == "Windows":
            command = "cls"
        else: 
            command = "clear"
        os.system(command)


def login():                                            # log with your user ans password to get token and information
    user = str(input("Votre nom d'utilisateur :\n>>> "))
    clear_screen()
    mdp = str(input("Votre mot de passe : \n>>> "))
    clear_screen()
    print("Authentification en cours . . .")
    data = 'data={\n\t\"identifiant\": \"' + user + '\",\n\t\"motdepasse\": \"' + mdp + '\"\n}'
    url = "https://api.ecoledirecte.com/v3/login.awp"
    response = rqs.post(url=url, data=data).json()      # post a request with data in body and make the response in a json file
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
        url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(id) + '/cahierdetexte/' + date + '.awp?verbe=get&'
    response = rqs.post(url=url, data=data).json()
    if response['code'] == 200:
        return response
    else:
        print('erreur ' + str(response['code']) + '\t message : ' + str(response['message']))


def fetch_emploi_du_temps(token, id, date_debut=None, date_fin=None):   # get the planning of the week
    if date_debut or date_fin == None:
        day = date.today().isoformat()
        dt = datetime.strptime(day, '%d/%b/%Y')
        date_debut = dt - timedelta(days=dt.weekday())
        date_fin = date_debut + timedelta(days=5)
        data = 'data={"dateDebut": "' + date_debut + '", "dateFin": "' + date_fin + '", "avecTrous": false, "token": "' + token + '"}'
        url = "https://api.ecoledirecte.com/v3/E/" + str(id) + "/EmploiDuTemps.awp?verbe=get&"
        response = rqs.post(url, data).json()
        return response
    else:
        data = 'data={"dateDebut": "' + date_debut + '", "dateFin": "' + date_fin + '", "avecTrous": false, "token": "' + token + '"}'
        url = "https://api.ecoledirecte.com/v3/E/" + str(id) + "/EmploiDuTemps.awp?verbe=get&"
        response = rqs.post(url, data).json()
        return response

