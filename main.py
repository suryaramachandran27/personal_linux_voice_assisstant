from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import pyttsx3
import pytz
import speech_recognition as sr
import subprocess
import requests,json
import urllib.request
from googlesearch import *
import webbrowser
import socket

APPS = ["google-chrome","firefox","nmap"]


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", 
"sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said.lower()


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    try:
        creds = None
    
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        
        return service

    except Exception as e:
        speak("sorry master"+str(e))

    

SERVICE =authenticate_google()

def get_events(day,service):
    

    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)


    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak("No upcoming events found master ")
    else:
        speak(f"you have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time =str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                start_time = start_time + "pm"
            speak(event["summary"]+ "at" + start_time)



def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass



    if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the next
        year = year+1

    
    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if month== -1 or day ==-1:
        pass
        return None
          
    return datetime.date(month=month, day=day, year=year)                


def note(text):
    date=datetime.datetime.now()
    file_name = str(date).replace(":","-") + "note.txt"
    with open(file_name,"w") as f:
        f.write(text)

    subprocess.Popen(["pluma",file_name])


def get_weather(text):
    api_key = "707a14b1964cdcfc1aeb7b471d5c3322"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + text
    response = requests.get(complete_url)
    x=response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"]
        print(" Temperature (in kelvin unit) = " +
                    str(current_temperature) + 
          "\n atmospheric pressure (in hPa unit) = " +
                    str(current_pressure) +
          "\n humidity (in percentage) = " +
                    str(current_humidiy) +
          "\n description = " +
                    str(weather_description))
        speak(" Temperature (in kelvin unit) = " +
                    str(current_temperature) + 
          "\n atmospheric pressure (in hPa unit) = " +
                    str(current_pressure) +
          "\n humidity (in percentage) = " +
                    str(current_humidiy) +
          "\n description = " +
                    str(weather_description))
    else:
        speak("sorry master I am unable to find the city master")

def google_search(text):
    IPaddress=socket.gethostbyname(socket.gethostname())
    
    if IPaddress=="127.0.0.1":
       speak("there is something wrong while connecting master")

    else:
        url='https://www.google.com/search?q='
        search_url=url+text
        speak("connecting master")
        webbrowser.get('google-chrome').open_new_tab(search_url)

def open_chrome():    
    os.system("google-chrome")

def open_firefox():
    os.system("firefox")
def open_nmap():
    os.system("nmap")
def open_terminal():
    os.system("gnome-terminal")
def open_wifte_with_kill():
    os.system("wifite")





WAKE1 = "hello baby"
WAKE2 = "hey baby"
WAKE3 = "are you there"
WAKE4 = "are you listening baby"
WAKE5 = "wake up baby"
WAKE6 = "are you ready"
WAKE7 = "baby"
WAKE8 = "baby are you ready"
WAKE9 = "you are listening right?"








while True:
    print ("listening....")
    text = get_audio()


    if text.count(WAKE1) > 0:
        speak("yes master proceed")
        text = get_audio()
    if text.count(WAKE2) > 0:
        speak("I am ready master")
        text = get_audio()
    if text.count(WAKE3) > 0:
        speak("yes master,i am here")
        text = get_audio()
    if text.count(WAKE4) > 0:
        speak("I am ready master")
        text = get_audio()
    if text.count(WAKE5) > 0:
        speak("i am up master")
        text = get_audio()
    if text.count(WAKE6) > 0:
        speak("I am ready master")
        text = get_audio()
    if text.count(WAKE7) > 0:
        speak("yes master")
        text = get_audio()
    if text.count(WAKE8) > 0:
        speak("I am ready master")
        text = get_audio()
    if text.count(WAKE9) > 0:
        speak("yes i am master")
        text = get_audio()




    GREETING_STR1 = ["hello","hi"]
    for phrase in GREETING_STR1:
        if phrase in text:
            speak("yes master")
        else:
            pass
    GREETING_STR2 = ["how are you"]
    for phrase in GREETING_STR2:
        if phrase in text:
            speak("I am fine master")

        else:
            pass
   
          


    

    CALENDAR_STRS = ["what do i have","what are my plans","check my events ","check plans","do i have anything planned","do i have plans","am i busy ","what are the plans"]
    for phrase in CALENDAR_STRS:
        if phrase in text:
            date = get_date(text)
            if date:
                get_events(date,SERVICE)
            else:
                speak("Please say again master ,I can't understand")


    WEATHER_STRS = ["check weather","check weather condition","how is the weather","get weather report"]
    for phrase in WEATHER_STRS:
        if phrase in text:
            speak("which place master?")
            place = get_audio()
            get_weather(place)
            speak("Anything Else Master?")

        else:
            pass




    SEARCH_STRS = ["search","google-search","google search"]
    for phrase in SEARCH_STRS:
        if phrase in text:
            speak("searching Master")
            google_search(text)
        else:
            pass


    OPEN_CHROME = ["open google","launch google","start google","open chrome","launch google","start google"]
    for phrase in OPEN_CHROME:
        if phrase in text:
            speak("opening google chrome master")
            open_chrome()
        else:
            pass
    OPEN_FIREFOX = ["open firefox","open mozilla firefox","open browser","launch firefox","launch browser","launch mozilla","start firefox"]
    for phrase in text:
        if phrase in text:
            speak("opening the mozilla firefox Master")
            open_firefox()
        else:
            pass








    NOTE_STRS = ["make a note ","make a file", "create a file","create new file","write this down","create file "]
    for phrase in NOTE_STRS:
        if phrase in text:
            speak("what would you like me to write down master?")
            note_text = get_audio()
            note(note_text)
            speak("I've made a note of that.")






