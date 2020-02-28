from __future__ import print_function
import pickle
import engine
import auth_google
import Audio
import os
import pytz
import datetime
import time
import requests,json
import urllib.request
import socket
import subprocess
import webbrowser
import wikipedia
import pyscreenshot as ImageGrab
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googlesearch import *
import strlists

def wikipedia_search():
    engine.speak("what to search in wikipedia master?please tell me again clearly master")
    search_string=Audio.get_audio()
    engine.speak("searching master")
    print(wikipedia.summary(search_string, sentences=2))
    engine.speak(wikipedia.summary(search_string, sentences=2))
               

def get_events(day,service):
    try:
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
            engine.speak("No upcoming events found master ")
        else:
            engine.speak(f"you have {len(events)} events on this day.")

            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
                start_time = str(start.split("T")[1].split("-")[0])
            
                if int(start_time.split(":")[0]) < 12:
                    start_time = start_time + "am"
            
                else:
                    start_time =str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                    start_time = start_time + "pm"
                engine.speak(event["summary"]+ "at" + start_time)
    except:
        pass

def google_search(text):    
    try:
        IPaddress=socket.gethostbyname(socket.gethostname())    
        if IPaddress=="127.0.0.1":
            engine.speak("there is something wrong while connecting master")

        else:
            url='https://www.google.com/search?q='
            search_url=url+text
            engine.speak("connecting master")
            webbrowser.get('google-chrome').open_new_tab(search_url)
    except:
        pass

def youtube_search(text):
    try:
        IPaddress=socket.gethostbyname(socket.gethostname())    
        if IPaddress=="127.0.0.1":
            engine.speak("there is something wrong while connecting master")
        else:
            url='https://www.youtube.com/results?search_query='
            search_url=url+text
            engine.speak("opening results master")
            webbrowser.get('google-chrome').open_new_tab(search_url)
    except:
        pass


    


def scrnshot():
    try:
        im = ImageGrab.grab()
        im.save('screenshot.png')
        im.show()
    except:
        pass







def get_weather(text):
    api_key = "707a14b1964cdcfc1aeb7b471d5c3322"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + text
    response = requests.get(complete_url)
    x=response.json()
    try:
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
            engine.speak(" Temperature (in kelvin unit) = " +
                        str(current_temperature) + 
            "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
            "\n humidity (in percentage) = " +
                        str(current_humidiy) +
            "\n description = " +
                        str(weather_description))
        else:
            engine.speak("sorry master I am unable to find the city master")

    except:
        engine.speak("sorry master something happened while checking weather")
        pass


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
        if word in strlists.MONTHS:
            month = strlists.MONTHS.index(word) + 1
        elif word in strlists.DAYS:
            day_of_week = strlists.DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in strlists.DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass



    if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the next
        year = year+1

    # This is slighlty different from the video but the correct version
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
