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
from base64 import b64decode
from bs4 import BeautifulSoup
from main import *

############################################################


def clear_screen():
    """
    Clear the terminal screen
    """
    if platform.system() == "Windows":
        command = "cls"
    else: 
        command = "clear"
    os.system(command)


class BadCreditentials(Exception):
    def __init__(self, message):
        super(BadCreditentials, self).__init__(message)


class UnknownError(Exception):
    def __init__(self, message):
        super(UnknownError, self).__init__(message)


class BadToken(Exception):
    def __init__(self, message):
        super(BadToken, self).__init__(message)


class BadPeriode(Exception):
    def __init__(self):
        super(BadPeriode, self).__init__()


class BadMatiere(Exception):
    def __init__(self):
        super(BadMatiere, self).__init__()


class EcoleDirecte:
    """
    Ecole direct class tha return you data like grades, course schredule, homework ...
    - - - - - - -
    Attributes:
        user: your username (str)
        password: your password (str)
        debug_mode: display request response and more (bool)
    - - - - - - -
    Methods:
        fetch_homework(date_choisie):
            - get your homework
        fetch_schredule(date_debut, date_fin):
            - get your schredule 
    """
    def __init__(self, user, password, debug_mode=False):
        """
        Constructs all the necessary attributes and login with your credentials
        - - - - - - -
        args:
            user: your username (str)
            password: your password (str)
            debug_mode: display request response and more (bool)
        - - - - - - -
        return: 
            response code (str)
            response message (str)
        """
        # assert test on args
        try:
            assert type(user) == str and user != ''
            assert type(password) == str and password != ''
            assert type(debug_mode) == bool
        except:
            print("Bad or empty args !!!")
        # initialize object var
        self.user = user
        self.password = password
        self.token = ""
        self.debug_mode = debug_mode
        self.header = {
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
        # login
        data = 'data={\n\t\"uuid\": \"\",\n\t\"identifiant\": \"' + self.user + '\",\n\t\"motdepasse\": \"' + self.password + '\"\n}'
        url = "https://api.ecoledirecte.com/v3/login.awp?v=4.18.3"
        response = rqs.post(url=url, data=data, headers=self.header).json()
        if debug_mode == True:
            print(response['token'])
        if response['code'] == 200:
            self.token = response['token']
            self.header['x-token'] = self.token
            self.id = response['data']['accounts'][0]['id']
            self.email = response['data']['accounts'][0]['email']
            self.header['origin'] = "https://www.ecoledirecte.com"
        elif response['code'] == 505:
            raise BadCreditentials("Bad username or password !!!")
        else:
            raise UnknownError('Error {}: {}'.format(response['code'], response['message']))


    def fetch_homework(self, date_choisie=False):
        """
        Get your homework of today or a choosen date
        - - - - - - -
        args:
            date_choisie: if true return the upcoming homework (bool)
        - - - - - - -
        return: None
        """
        data = 'data={\n\t\"token\": \"' + self.token + '\"\n}'
        if date_choisie == False:
            date_iso = datetime.now()
            date_today = datetime.strftime(date_iso, '%Y-%m-%d')
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte' + str(date_today) + '.awp?v=4.18.3&verbe=get&'
            response = rqs.post(url, data, headers=self.header).text
            print(response)
            response = response.json()
            data = response['data']
            if self.debug_mode == True:
                print(data)
        elif date_choisie == "A_venir":
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte.awp?v=4.18.3&verbe=get'
            response = rqs.post(url=url, data=data, headers=self.header).json()
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
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte/' + str(date_devoir) + '.awp?v=4.18.3&verbe=get&'
            response = rqs.post(url=url, data=data, headers=self.header).json()
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
        elif date_choisie != False and date_choisie != "A_venir":
            date = datetime.strftime(date_choisie, '%Y-%m-%d')
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte/' + str(date) + '.awp?v=4.18.3&verbe=get&'
            response = rqs.post(url=url, data=data, headers=self.header).json()
            if response['code'] == 200:
                print(response['data'][0])
                return response
            else:
                print('erreur ' + str(response['code']) + '\t message : ' + str(response['message']))
        else:
            raise ValueError("Bad args !!!")


    def fetch_schredule(self, date_debut=None, date_fin=None):
        """
        Get your schredule of the week or of a choosen date
        - - - - - - -
        args:
            date_debut: the start date of the wanted period in DD-MM-YYYY date format (str)
        - - - - - - -
        return: None
        """
        if date_debut or date_fin == None:
            day_iso = date.today()
            day_str = datetime.strftime(day_iso, '%d-%m-%Y')
            day_obj = datetime.strptime(day_str, '%d-%m-%Y')
            date_debut = day_obj - timedelta(days=day_obj.weekday())
            date_fin = date_debut + timedelta(days=5)
            print("Demande de l'emploi du temps de la semaine ( du " + str(date_debut) + " au " + str(date_fin) + " )")
            data = 'data={"dateDebut": "' + str(date_debut) + '", "dateFin": "' + str(date_fin) + '", "avecTrous": false, "token": "' + str(self.token) + '"}'
            url = "https://api.ecoledirecte.com/v3/E/" + str(self.id) + "/EmploiDuTemps.awp?v=4.18.3&verbe=get&"
            response = rqs.post(url, data, headers=self.header).json()
            return response
        else:
            print("Demande de l'emploi du temps ( du " + str(date_debut) + " au " + str(date_fin) + " )")
            data = 'data={"dateDebut": "' + str(date_debut) + '", "dateFin": "' + str(date_fin) + '", "avecTrous": false, "token": "' + str(self.token) + '"}'
            url = "https://api.ecoledirecte.com/v3/E/" + str(id) + "/EmploiDuTemps.awp?v=4.18.3&verbe=get&"
            response = rqs.post(url, data).json()
            return response
