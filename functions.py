############################################################
#               Ecole-direct-in-Python                     #
#               Author : Intermarch3                       #
#               start at : 07/2021                         #
#               End at : work in progress                  #
############################################################

#################### - Import space - ######################

import requests as rqs
import os
import platform 
from datetime import date, datetime, timedelta 
from ics import Calendar, Event

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
    def __init__(self, message):
        super(BadPeriode, self).__init__(message)


class RequestError(Exception):
    def __init__(self, message):
        super(RequestError, self).__init__(message)


class EcoleDirecte:
    """
    Ecole direct class that return you data like grades, course schredule, homework ...
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
        create_calendar()
            - create a calendar object
        add_calendar_event(calendar, data)
            - add event to calendar object
        export_calendar(calendar, name)
            - create a calendar file with a calendar object
    """
    def __init__(self, user, password):
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
        except:
            raise ValueError("Bad args !!!")
        # initialize object var
        self.user = user
        self.password = password
        self.token = ""
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
        if response['code'] == 200:
            self.token = response['token']
            self.header['x-token'] = self.token
            self.id = response['data']['accounts'][0]['id']
            self.email = response['data']['accounts'][0]['email']
            self.header['origin'] = "https://www.ecoledirecte.com"
        elif response['code'] == 505:
            raise BadCreditentials("Bad username or password !!!")
        else:
            raise RequestError('Error {}: {}'.format(response['code'], response['message']))


    def fetch_homework(self, date_choisie=False):
        """
        Get your homework of today or a choosen date
        - - - - - - -
        args:
            date_choisie: if true return the upcoming homework (bool)
        - - - - - - -
        return: None
        """
        # assert test on args
        try:
            assert type(date_choisie) == False or type(date_choisie) == str
        except:
            raise ValueError("Bad args !!!")
        # return homework of today
        data_rqs = 'data={\n\t\"token\": \"' + self.token + '\"\n}'
        if date_choisie == False:
            date_iso = datetime.now()
            date_today = datetime.strftime(date_iso, '%Y-%m-%d')
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte/' + str(date_today) + '.awp?v=4.18.3&verbe=get&'
            response = rqs.post(url, data_rqs, headers=self.header).json()
            if response['code'] == 200:
                self.token = response['token']
                return date_today, response['data']
            else:
                raise RequestError('erreur ' + str(response['code']) + '\t message : ' + str(response['message']))
        # return list of incoming homework
        elif date_choisie == "A_venir":
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte.awp?v=4.18.3&verbe=get'
            response = rqs.post(url=url, data=data_rqs, headers=self.header).json()
            if response['code'] == 200:
                self.token = response['token']
                return response['data']
            else:
                raise RequestError('erreur ' + str(response['code']) + '\t message : ' + str(response['message']))
        # return homework of a given date
        elif date_choisie != False and date_choisie != "A_venir":
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte/' + str(date_choisie) + '.awp?v=4.18.3&verbe=get&'
            response = rqs.post(url=url, data=data_rqs, headers=self.header).json()
            if response['code'] == 200:
                self.token = response['token']
                return response['data']
            else:
                raise RequestError('erreur ' + str(response['code']) + '\t message : ' + str(response['message']))
        else:
            raise ValueError("Bad args !!!")


    def fetch_schredule(self, date_debut=None, date_fin=None, today=False):
        """
        Get your schredule of the week or of a choosen date
        - - - - - - -
        args:
            date_debut: the start date of the wanted period in DD-MM-YYYY date format (str)
        - - - - - - -
        return: None
        """
        if date_debut == None or date_fin == None and today == False:
            day_iso = date.today()
            day_str = datetime.strftime(day_iso, '%d-%m-%Y')
            day_obj = datetime.strptime(day_str, '%d-%m-%Y')
            date_debut = day_obj - timedelta(days=day_obj.weekday())
            date_fin = date_debut + timedelta(days=5)
            data = 'data={"dateDebut": "' + str(date_debut) + '", "dateFin": "' + str(date_fin) + '", "avecTrous": false, "token": "' + str(self.token) + '"}'
            url = "https://api.ecoledirecte.com/v3/E/" + str(self.id) + "/EmploiDuTemps.awp?v=4.18.3&verbe=get&"
            response = rqs.post(url, data, headers=self.header).json()
            return response['data']
        elif today == True:
            day = date.today()
            data = 'data={"dateDebut": "' + str(day) + '", "dateFin": "' + str(day) + '", "avecTrous": false, "token": "' + str(self.token) + '"}'
            url = "https://api.ecoledirecte.com/v3/E/" + str(self.id) + "/EmploiDuTemps.awp?v=4.18.3&verbe=get&"
            response = rqs.post(url, data, headers=self.header).json()
            return response['data']
        else:
            data = 'data={"dateDebut": "' + str(date_debut) + '", "dateFin": "' + str(date_fin) + '", "avecTrous": false, "token": "' + str(self.token) + '"}'
            url = "https://api.ecoledirecte.com/v3/E/" + str(id) + "/EmploiDuTemps.awp?v=4.18.3&verbe=get&"
            response = rqs.post(url, data).json()
            return response['data']


    def create_calendar(self):
        """
        create a calendar object
        - - - - - - -
        args: none
        - - - - - - -
        return: 
            calendar object (obj)
        """
        c = Calendar()
        return c


    def add_calendar_event(self, calendar, data):
        """
        add event in a calendar object with your schredule
        - - - - - - -
        args: 
            data: the response of schredule request (json)
        - - - - - - -
        return: 
            calendar object (obj)
        """
        for cour in data:
            e = Event()
            e.name = cour['matiere']
            e.begin = cour['start_date']
            e.end = cour['end_date']
            desc = "Prof: " + cour['prof']
            if cour['salle'] != "":
                desc += "\nSalle:" + cour['salle']
            e.description = desc
            calendar.events.add(e)
        return calendar


    def export_calendar(self, calendar, file_name):
        """
        Create a calendar file (ics)
        - - - - - - -
        args:
            calendar: the calendar object (obj)
            name: the file name (str)
        - - - - - - -
        return: none
        """
        name = str(file_name) + ".ics"
        with open(name, 'w') as file:
            file.writelines(calendar.serialize_iter())
            file.close()

