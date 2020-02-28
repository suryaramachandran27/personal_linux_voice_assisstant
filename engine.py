import os
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume',1.0) 
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[2].id)  
    engine.say(text)
    engine.runAndWait()