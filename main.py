from __future__ import print_function
import pickle
import engine
import auth_google
import skills
import Audio
import openfun
import os
import datetime
import requests,json
import urllib.request
import strlists

SERVICE =auth_google.authenticate_google()
while True:
    print ("listening....")
    text = Audio.get_audio()


    if text.count(strlists.WAKE1) > 0:
        engine.speak("yes master proceed")
        text = Audio.get_audio()
    if text.count(strlists.WAKE2) > 0:
        engine.speak("I am ready master")
        text = Audio.get_audio()
    if text.count(strlists.WAKE3) > 0:
        engine.speak("yes master,i am here")
        text = Audio.get_audio()
    if text.count(strlists.WAKE4) > 0:
        engine.speak("I am ready master")
        text = Audio.get_audio()
    if text.count(strlists.WAKE5) > 0:
        engine.speak("yeah master")
        text = Audio.get_audio()
    if text.count(strlists.WAKE6) > 0:
        engine.speak("I am ready master")
        text = Audio.get_audio()
    if text.count(strlists.WAKE7) > 0:
        engine.speak("yes master")
        text = Audio.get_audio()
    if text.count(strlists.WAKE8) > 0:
        engine.speak("I am ready master")
        text = Audio.get_audio()
    if text.count(strlists.WAKE9) > 0:
        engine.speak("yes i am master")
        text = Audio.get_audio()

    
    for phrase in strlists.GREETING_STR1:
        if phrase in text:
            engine.speak("yes master")
        else:
            pass
   
    for phrase in strlists.GREETING_STR2:
        if phrase in text:
            engine.speak("I am fine master")

        else:
            pass
   

    for phrase in strlists.CALENDAR_STRS:
        if phrase in text:
            date = skills.get_date(text)
            if date:
                skills.get_events(date,SERVICE)
            else:
                engine.speak("Please say again master ,I can't understand")

    for phrase in strlists.WEATHER_STRS:
        if phrase in text:
            engine.speak("which place master?")
            area = Audio.get_audio()
            skills.get_weather(area)
            engine.speak("Anything Else Master?")
            break

        else:
            pass


    for phrase in strlists.SEARCH_STRS:
        for phrase in strlists.SEARCH_GOOGLE_STR:
            if phrase in text:
                engine.speak("what to search master?,please tell me again")
                text = Audio.get_audio()
                skills.google_search(text)
                engine.speak("searching master!")
                break
            else:
                pass
        for phrase in strlists.SEARCH_WIKIPEDIA_STR:
            if phrase in text:
                skills.wikipedia_search()
                break
            else:
                pass
        for phrase in strlists.SEARCH_YOUTUBE_STR:
            if phrase in text:
                engine.speak("what to search master ?,please tell me!")
                query = Audio.get_audio()
                skills.youtube_search(query)
                break
            else:pass
            






    for phrase in strlists.NOTE_STRS:
        if phrase in text:
            engine.speak("what would you like me to write down master?")
            note_text = Audio.get_audio()
            skills.note(note_text)
            engine.speak("I've made a note of that.")


    for phrase in strlists.SCREENSHOT_STR:
        if phrase in text:
            engine.speak("taking screen shot master")
            skills.scrnshot()
            break
        else:
            pass

    for phrase in strlists.ASKFOR_GAME:
        if phrase in text:
            engine.speak("do you want to play chess master?")
            text = Audio.get_audio()
            if "yes" in text:
                openfun.xboard()
            else:
                engine.speak("ok master")
        else:
            pass
    
    for phrase in strlists.OPEN_STR:
        if phrase in text:
            for phrase in strlists.GOOGLE_STR:
                if phrase in text:
                    engine.speak("opening google chrome master")
                    openfun.google()
                    break
                else:
                    pass

            for phrase in strlists.FIREFOX_STR:
                if phrase in text:
                    engine.speak("opening firefox master")
                    openfun.firefox()
                    break
                else:
                    pass
            
            for phrase in strlists.NMAP_STR:
                if phrase in text:
                    engine.speak("opening nmap")
                    openfun.nmap()
                    break
                else:
                    pass
            
            for phrase in strlists.TERMINAL_STR:
                if phrase in text:
                    engine.speak("opening terminal master")
                    openfun.terminal()
                    break
                else:
                    pass
            
            for pharse in strlists.PLUMA_STR:
                if phrase in text:
                    engine.speak("opening pluma master")
                    openfun.pluma()
                    break
                else:
                    pass


            for phrase in strlists.NITKO_STR:
                if phrase in text:
                    engine.speak("opening the nitko scanner master!")
                    openfun.nitko()
                    break
                else:
                    pass
        
                    
            for phrase in strlists.CALC_STR:
                if phrase in text:
                    engine.speak("opening calculator master!")
                    openfun.calc()
                    break
                else:
                    pass
            for phrase in strlists.NVIM_STR:
                if phrase in text:
                    engine.speak("openig the nvim text editor master")
                    openfun.nvim()
                    break
                else:
                    pass
            for phrase in strlists.VSCODE_STR:
                if phrase in text:
                    engine.speak("opening visual studio code master!")
                    openfun.vscode()
                    break
                else:
                    pass
            for pharse in strlists.ANONSURF_STR:
                if phrase in text:
                    engine.speak("starting anonsurf master")
                    openfun.anonsurf()
                    break
                else:
                    pass
            for phrase in strlists.LIBREOFFICE_STR:
                if phrase in text:
                    for phrase in strlists.LIBREOFFICE_BASE:
                        if phrase in text:
                            engine.speak("opening the libre office base master!")
                            openfun.libre_office_base()
                            break
                        else:
                            pass
                    for phrase in strlists.LIBREOFFICE_CALC:
                        if phrase in text:
                            engine.speak("opening the libreoffice calc master!")
                            openfun.libre_office_calc()
                            break
                        else:
                            pass
                    for phrase in strlists.LIBREOFFICE_DRAW:
                        if phrase in text:
                            engine.speak("opening the libreoffice draw master!")
                            openfun.libre_office_draw()
                            break
                        else:
                            pass
                    
                    for phrase in strlists.LIBREOFFICE_IMPRESS:
                        if phrase in text:
                            engine.speak("opening the libreoffice impress master!")
                            openfun.libre_office_impress()
                            break
                        else:
                            pass
                    for phrase in strlists.LIBREOFFICE_WRITER:
                        if phrase in text:
                            engine.speak("opening the libre office writer master!")
                            openfun.libre_office_writer()
                            break
                        else:
                            pass
                    for phrase in strlists.LIBREOFFICE_MATH:
                        if phrase in text:
                            engine.speak("opneing the libreoffice maths master!")
                            openfun.libre_office_math()
                            break
                        else:
                            pass  
                    break
                else:
                    pass

            for phrase in strlists.CHESS_STR:
                if phrase in text:
                    engine.speak("opening the xboard master!")
                    openfun.xboard()
                    break
                else:
                    pass

            for phrase in strlists.PHOTOEDITOR_STR:
                if phrase in text:
                    engine.speak("opening the gimp image manupulation program")
                    openfun.photoeditor()
                    break
                else:
                    pass


        else:
            pass
   