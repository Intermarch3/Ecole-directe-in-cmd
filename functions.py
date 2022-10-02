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
    Ecole direct class that return your data like grades, course schedule, homework ...
    - - - - - - -
    Attributes:
        user: your username (str)
        password: your password (str)
        debug_mode: display request response and more (bool)
    - - - - - - -
    Methods:
        fetch_homework(date_choisie):
            - get your homework
        fetch_schedule(date_start, date_end):
            - get your schedule 
        ScheduleInCalendar (class)
            - create calendar object, add events and export it
    """
    def __init__(self, user, password, version="4.18.3"):
        """
        Constructs all the necessary attributes and login with your credentials
        - - - - - - -
        args:
            user: your username (str)
            password: your password (str)
            version: the api version (str)
        - - - - - - -
        return: none
        """
        # assert test on args
        try:
            assert type(user) == str and user != ''
            assert type(password) == str and password != ''
        except:
            raise ValueError("Bad args !!!")
        # initialize attributs
        self.v = version
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
        url = "https://api.ecoledirecte.com/v3/login.awp?v=" + self.v
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
            assert type(date_choisie) == bool or type(date_choisie) == str
        except:
            raise ValueError("Bad args !!!")
        # return homework of today
        data_rqs = 'data={\n\t\"token\": \"' + self.token + '\"\n}'
        if date_choisie == False:
            date_iso = datetime.now()
            date_today = datetime.strftime(date_iso, '%Y-%m-%d')
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte/' + str(date_today) + '.awp?v=' + self.v + '&verbe=get&'
            response = rqs.post(url, data_rqs, headers=self.header).json()
            if response['code'] == 200:
                self.token = response['token']
                return date_today, response['data']
            else:
                raise RequestError('Error {}: {}'.format(response['code'], response['message']))
        # return list of incoming homework
        elif date_choisie == "A_venir":
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte.awp?v=' + self.v + '&verbe=get'
            response = rqs.post(url=url, data=data_rqs, headers=self.header).json()
            if response['code'] == 200:
                self.token = response['token']
                return response['data']
            else:
                raise RequestError('Error {}: {}'.format(response['code'], response['message']))
        # return homework of a given date
        elif date_choisie != False and date_choisie != "A_venir":
            url = 'https://api.ecoledirecte.com/v3/Eleves/' + str(self.id) + '/cahierdetexte/' + str(date_choisie) + '.awp?v=' + self.v + '&verbe=get&'
            response = rqs.post(url=url, data=data_rqs, headers=self.header).json()
            if response['code'] == 200:
                self.token = response['token']
                return response['data']
            else:
                raise RequestError('Error {}: {}'.format(response['code'], response['message']))
        else:
            raise ValueError("Bad args !!!")


    def fetch_schedule(self, date_start="", date_end="", today=False):
        """
        Get your schedule of the week or of a choosen date
        - - - - - - -
        args:
            date_start: the start date of the wanted period in DD-MM-YYYY date format (str)
            date_end: the end date of the wanted period in DD-MM-YYYY date format (str)
            today: if True, fetch schedule of today (bool)
            if no args: return week schedule
        - - - - - - -
        return: response: request response (json)
        """
        # assert test on args
        try:
            assert type(date_start) == str and type(date_end) == str and type(today) == bool
        except:
            raise ValueError("Bad args !!!")
        # get week schedule
        if date_start == "" and date_end == "" and today == False:
            day_iso = date.today()
            day_str = datetime.strftime(day_iso, '%d-%m-%Y')
            day_obj = datetime.strptime(day_str, '%d-%m-%Y')
            date_start = day_obj - timedelta(days=day_obj.weekday())
            date_end = date_start + timedelta(days=5)
            data = 'data={"dateDebut": "' + str(date_start) + '", "dateFin": "' + str(date_end) + '", "avecTrous": false, "token": "' + str(self.token) + '"}'
            url = "https://api.ecoledirecte.com/v3/E/" + str(self.id) + "/EmploiDuTemps.awp?v=" + self.v + "&verbe=get&"
            response = rqs.post(url, data, headers=self.header).json()
            if response['code'] == 200:
                self.token = response['token']
                return response['data']
            else:
                raise RequestError('Error {}: {}'.format(response['code'], response['message']))
        # get today schedule
        elif today == True:
            day = date.today()
            data = 'data={"dateDebut": "' + str(day) + '", "dateFin": "' + str(day) + '", "avecTrous": false, "token": "' + str(self.token) + '"}'
            url = "https://api.ecoledirecte.com/v3/E/" + str(self.id) + "/EmploiDuTemps.awp?v=" + self.v + "&verbe=get&"
            response = rqs.post(url, data, headers=self.header).json()
            if response['code'] == 200:
                self.token = response['token']
                return response['data']
            else:
                raise RequestError('Error {}: {}'.format(response['code'], response['message']))
        # get schedule of given date
        else:
            try:
                assert date_start != "" and date_end != ""
            except:
                raise BadPeriode("Date manquantes !!!")
            data = 'data={"dateDebut": "' + str(date_start) + '", "dateFin": "' + str(date_end) + '", "avecTrous": false, "token": "' + str(self.token) + '"}'
            url = "https://api.ecoledirecte.com/v3/E/" + str(self.id) + "/EmploiDuTemps.awp?v=" + self.v + "&verbe=get&"
            response = rqs.post(url, data, headers=self.header).json()
            if response['code'] == 200:
                self.token = response['token']
                return response['data']
            else:
                raise RequestError('Error {}: {}'.format(response['code'], response['message']))


    def fetch_grades(self):
        """
        Get your grades
        - - - - - - -
        args: none
        - - - - - - -
        return: response: request response (json)
        """
        data = 'data={\n\t\"token\": \"' + self.token + '\"\n}'
        url = 'https://api.ecoledirecte.com/v3/eleves/'+ str(self.id) +'/notes.awp?v=' + self.v + '&verbe=get&'
        response = rqs.post(url, data, headers=self.header).json()
        if response['code'] == 200:
            self.token = response['token']
            return response['data']
        else:
            raise RequestError('Error {}: {}'.format(response['code'], response['message']))


    class ScheduleInCalendar:
        """
        Schedule in Calendar class that create a calendar object, add event and export it (.ics)
        - - - - - - -
        Attributes:
            name: name of the calendar file (str)
        - - - - - - -
        Methods:
            add_calendar_event(calendar, data)
                - add event to calendar object
            export_calendar(calendar, name)
                - create a calendar file with a calendar object
        """
        def __init__(self, name=""):
            """
            create calendar object
            - - - - - - -
            args:
                name: the file name (str)
            - - - - - - -
            return: none
            """
            # assert test on args
            try:
                assert type(name) == str and name != ""
            except:
                raise ValueError("Bad args !!!")
            # initialize attributs
            self.name = name
            self.calendar = Calendar(creator="Intermarch3")


        def add_calendar_event(self, data):
            """
            add event in a calendar object with your schedule data
            - - - - - - -
            args: 
                data: the response of schedule request (json)
            - - - - - - -
            return: 
                calendar object (obj)
            """
            # assert test on args
            try:
                assert type(data) == dict or type(data) == list
            except:
                raise ValueError("Bad args !!!")
            # add event of each course
            for cour in data:
                e = Event()
                e.name = cour['matiere']
                e.begin = cour['start_date']
                e.end = cour['end_date']
                desc = "Prof: " + cour['prof']
                if cour['salle'] != "":
                    desc += "\nSalle:" + cour['salle']
                e.description = desc
                self.calendar.events.add(e)
            return self.calendar


        def export_calendar(self):
            """
            Create a calendar file (ics)
            - - - - - - -
            args:
                calendar: the calendar object (obj)
                name: the file name (str)
            - - - - - - -
            return: none
            """
            name = str(self.name) + ".ics"
            with open(name, 'w') as file:
                file.writelines(self.calendar.serialize_iter())
                file.close()

