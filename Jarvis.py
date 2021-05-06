# This is the code for Assistant
import random
import requests
import json
import datetime
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import os
import smtplib

# For Voice Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)  # 0 is the voice of David, and 1 is voice of zara
engine.setProperty('voice', voices[1].id)
# newVoiceRate is integer speech rate in words per minute. Defaults to 200 word per minute.
newVoiceRate = 175
engine.setProperty('rate', newVoiceRate)

# For IP Api
send_url = "http://api.ipstack.com/check?access_key=ce6cb418cc573c66fac939da9586a09e"
ipApi = requests.get(send_url).text
ipApi_dict = json.loads(ipApi)

# For Weather Api
weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={ipApi_dict['city']},{ipApi_dict['country_code']}" \
              f"&units=metric&appid=2280467803ab89d334334c94299ceef3"
weather = requests.get(weather_url).text
weather_dict = json.loads(weather)

# For E-Mail IDs
email_dict = {
#   Write name of person by which you will call and their E-Mail
    'Friend1': 'Friend1.email@gmail.com',
    'Friend2': 'Friend2.email@gmail.com',
    'Friend3': 'Friend3.email@gmail.com'
}


def speak(words):
    engine.say(words)
    engine.runAndWait()


def wishMe():
    """
    Wishes the User on startup of the program
    """
    hour = int(datetime.datetime.now().hour)
    minutes = int(datetime.datetime.now().minute)

    if 0 <= hour <= 12:
        time = f"{hour} AM"
    else:
        time = f"{hour - 12} PM"

    if 0 <= hour <= 12:
        speak("Good Morning")
    elif 12 <= hour <= 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak(f"I am Jarvis. It's {time} and {minutes} minutes, {weather()}")


def weather():
    """
    This function takes the weather updates from the Weather API website and then we convert it into an intelligible
    message.
    :return: String Output
    """

    message = f"The Weather in {weather_dict['name']} is {weather_dict['main']['temp']} degrees, and it feels like " \
              f"{weather_dict['main']['feels_like']} degrees with {weather_dict['weather'][0]['description']}. "
    return message


def takeCommand():
    """
    It Listens to your command and does the needful to execute them
    :return: String Output
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.5  # seconds of non-speaking audio before a phrase is considered complete
        r.energy_threshold = 350  # minimum audio energy to consider for recording (if increased then speak loudly)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said : ", query, '\n')

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


def sendEmail(recievers_email, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    with open("account.txt", "rt") as f:
        data = f.read().split(" ")
    server.login(data[0], data[1])
    server.sendmail(data[0], recievers_email, content)
    speak("E-Mail has been sent")
    server.close()


if __name__ == '__main__':
    # wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak("Searching in Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            print(results)
            speak(f"According to Wikipedia, {results}")

        # Web browser Actions
        elif 'open youtube' in query:
            webbrowser.open('https://www.youtube.com/')

        elif 'open google' in query:
            webbrowser.open('https://www.google.co.in/')

        elif 'open college mail id' in query:
            webbrowser.open(r'https://mail.google.com/mail/u/1/#inbox')

        elif 'open personal mail id' in query:
            webbrowser.open('https://mail.google.com/mail/u/0/#inbox')

        # Say 'Open' then the whole url for it to open
        elif 'open www.' in query:
            query = query.replace("open ", "")
            webbrowser.open('https://' + query)

        # Say 'Ok Google' then all other words will be searched on Google
        elif 'ok google' in query:
            query = query.replace("ok google ", "")
            webbrowser.open('https://www.google.co.in/search?q=' + query)

        # Say 'Ok Youtube' then all other words will be searched on Youtube
        elif 'ok youtube' in query:
            query = query.replace("ok youtube ", "")
            webbrowser.open('https://www.youtube.com/results?search_query=' + query)

        # Plays Marvel Movies
        elif 'play marvel' in query:
            marvel_dir = r"D:\VIDEOS\Marvel\The Infinity Saga"
            movies = os.listdir(marvel_dir)
            randomNumber = random.randint(0, len(movies))
            os.startfile(os.path.join(marvel_dir, movies[randomNumber]))

        # Plays Random Music and Syntax for running anything in a directory
        elif 'play music' in query:
            song_dir = r"D:\VIDEOS\HIMANSHU'S VIDEO'S\Mobile\Music\English Songs"
            songs = os.listdir(song_dir)
            randomNumber = random.randint(0, len(songs) - 1)
            os.startfile(os.path.join(song_dir, songs[randomNumber]))

        # Opens Grammarly and Syntax for Opening an app for you
        elif 'open grammarly' in query:
            grammarly_path = r'C:\Users\himan\AppData\Local\GrammarlyForWindows\GrammarlyForWindows.exe'
            os.startfile(grammarly_path)

        # Sends Email to the Friend whose name and E-Mail is in Dictionary
        elif 'send email to' in query:
            try:
                new = query.split(' ')[-1].lower()
                email = email_dict.get(new)
                while True:
                    speak("What should be written in the mail")
                    content = takeCommand()
                    print(f"\nContent said by you is : {content}\n")
                    speak(f"Content said by you is : {content}")
                    print("If the content is correct say 'Yes', else say 'No', or to write content yourself "
                          "say 'Content'. To discard mail say 'Discard'")
                    speak("If the content is correct say 'Yes', else say 'No', or to write content yourself "
                          "say 'Content'. To discard mail say 'Discard'")
                    permission = takeCommand()
                    if permission == "content":
                        content = input("Write Content : ")
                        sendEmail(email, content)
                        break
                    elif permission == "yes":
                        sendEmail(email, content)
                        break
                    elif permission == "discard":
                        break
                    else:
                        continue

            except Exception as e:
                speak(f"There was an ERROR!!!\n"
                      f"{e}")

        # Tells the Time
        elif 'time' in query:
            hour = int(datetime.datetime.now().hour)
            minutes = int(datetime.datetime.now().minute)

            if 0 <= hour <= 12:
                time = f"{hour} AM"
            else:
                time = f"{hour - 12} PM"
            print(f"Sir, the Time is {time} and {minutes} minutes")
            speak(f"Sir, the Time is {time} and {minutes} minutes")

        # Weather Api Actions, Tells the Weather of your current location
        elif 'weather' in query:
            print(weather())
            speak(weather())

        elif 'stop assistant' in query:
            exit()

        else:
            continue
