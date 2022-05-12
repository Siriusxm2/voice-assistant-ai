import speech_recognition as sr
import webbrowser
import os
import random
import requests
import json
import pywhatkit

from playsound2 import playsound
from neuralintents import GenericAssistant
from gtts import gTTS
from datetime import datetime

listener = sr.Recognizer()


def burt_speech(audio_string):
    tts = gTTS(text=audio_string, tld='co.uk', lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def burt_introduction():
    i_responses = ["I am Burt", "My name is Burt. I am a virtual assistant.",
                   "I'm a virtual assistant. My friends call me Burt but you can call me tonight."]
    rand = random.randint(0, 2)
    burt_speech(i_responses[rand])


def burt_greeting():
    g_responses = ["Good day to you too.", "Howdy.", "Hello"]
    rand = random.randint(0, 2)
    burt_speech(g_responses[rand])


def burt_exit():
    e_responses = ["Goodbye", "See you", "Cya", "Arrivederci", "Bye"]
    rand = random.randint(0, 3)
    burt_speech(e_responses[rand])
    exit()


def burt_search():
    global listener
    burt_speech("What do you want to search for?")
    done = False

    while not done:
        try:
            with sr.Microphone() as source:
                audio = listener.listen(source)
                search_data = listener.recognize_google(audio)

            search_data = search_data.lower()
            if 'nothing' in search_data:
                done = True
                burt_speech('Stopping the search.')
                break
            else:
                done = True
                url = 'https://google.com/search?q=' + search_data
                webbrowser.get().open(url)
                burt_speech('Here is what I found for ' + search_data)

        except sr.UnknownValueError:
            burt_speech('Can you repeat that?')
            listener = sr.Recognizer()


def burt_time():
    timenow = datetime.now().strftime("%H:%M")
    burt_speech("The time is " + timenow)


def burt_date():
    datenow = datetime.now().strftime("%A %B %d")
    burt_speech("Today is " + datenow)


def burt_weather():
    response = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?q=Varna,bg&appid=490d99177878fdcc1d12a2d2dc90c047&units=metric')
    url = response.text
    data = json.loads(url)
    for i in data['weather']:
        weather = i['main']
    temp = data['main']['temp']
    burt_speech("It is " + str(round(temp, 1)) +
                " degrees Celsius and " + weather + ' outside.')


mappings = {
    "greeting": burt_greeting,
    "introduction": burt_introduction,
    "search": burt_search,
    "time": burt_time,
    "date": burt_date,
    "weather": burt_weather,
    "exit": burt_exit
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

burt_speech("How may I be of your service today?")
while True:
    try:
        with sr.Microphone() as source:
            audio = listener.listen(source)
            message = listener.recognize_google(audio)

        message = message.lower()
        if 'play' in message:
            songName = message.replace('play ', '')
            burt_speech('Playing ' + songName)
            pywhatkit.playonyt(songName)

        assistant.request(message)

    except sr.UnknownValueError:
        burt_speech("Can you repeat that?")
        listener = sr.Recognizer()
