import speech_recognition as sr
import win32com.client
import pyautogui as p
from faceRecognition import face_auth

bot = "Kaajin"  # Kashikoi yuujin - wise friend
close = 0  # if greater than 0 the program would end
speaker = win32com.client.Dispatch("SAPI.SpVoice")


def say(text):
    speaker.Speak(text)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        say("Listening sir")
        print("Listening...")
        r.pause_threshold = 1

        # Adjusting for ambient noise
        r.adjust_for_ambient_noise(source)

        # Capture the audio
        audio = r.listen(source)

        say("Recognizing your command sir")
        print("Recognizing...")

        try:
            query = r.recognize_google(audio)
            return query
        except Exception as exc:
            print(f"Error in take_command: {exc}")
            say(f"An Error occurred sir, sorry from {bot}, Please say again")
            take_command()


def ai(messages, model="gpt-3.5-turbo"):
    import openai
    from config import apikey

    openai.api_key = apikey
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        max_tokens=256,
        n=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        msg = response.choices[0].message.content
        messages.append(response.choices[0].message)
        say(msg)

    except Exception as exc:
        print(f"Error in ai: {exc}")
        say(f"An Error occurred in ai, sorry from {bot}")


def find_location():
    from geopy.geocoders import Nominatim

    say("Tell the name of the place sir")
    place = take_command()
    say("wait sir let me check")
    geolocator = Nominatim(user_agent="GetLoc")

    try:
        location = geolocator.geocode(place)
        if location:
            say(f"Sir The full address of this place is {location.address},")
            say(f"The Longitude is{location.longitude} and the Latitude is {location.latitude}")
            print(f"Address: {location.address}")
            print(f"Longitude: {location.longitude}")
            print(f"Latitude: {location.latitude}")

            say(f"Sir Do you want to know more about {place}?")
            permit = take_command()
            if "yes" in permit or "sure" in permit:
                say("Ok sir, let me gather the information")
                q = [{"role": "user", "content": f"Tell me about {location}"}]
                ai(q)
            else:
                say("ok sir")
        else:
            say("sorry sir I could not find out The location")
    except Exception as exc:
        print(f"Error occurred in find_location: {exc}")
        say(f"an error occurred sir, sorry from {bot}")


def take_screenshot():
    import time

    say("Please Tell the name of the file sir")
    name = take_command()
    say("Please sir hold the screen for a few seconds, I am taking a screenshot")
    time.sleep(3)
    img = p.screenshot()
    img.save(f"ss/{name}.png")
    print("Screenshot saved!")
    say("I am done sir, the screenshot is saved in the ss folder")


def check_internet_speed():
    say("I need some time to check the internet speed sir, please wait a few moment")
    import speedtest

    try:
        st = speedtest.Speedtest()
        n = 8000000
        say("Calculating The Downloading Speed sir")
        dl = round(st.download() / n, 2)
        say("The Downloading speed has been calculated. Calculating the uploading speed sir")
        up = round(st.upload() / n, 2)
        say(f"We have {dl} MB per second downloading and {up} MB per second uploading speed sir")

    except Exception as exc:
        print(f"Error in check_internet_speed: {exc}")
        say(f"An Error occurred, sorry from {bot} sir")


def check_battery():
    import psutil

    say("Checking The Battery Level sir")
    battery = psutil.sensors_battery()
    battery_percentage = battery.percent
    say(f"The Current Level of Battery charge is {battery_percentage} percent")


def get_weather_report(place):
    from bs4 import BeautifulSoup
    import requests

    say("Gathering Weather Report Sir")
    search = f"Weather in {place}"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    say(f"The Current Temperature of {place} is {temp}")


def get_last_word(string):
    words = string.split()
    if words:
        return words[-1]


def main(c):
    p.press('esc')
    say("Verification Successful, Welcome back sir")
    say(f"Hello sir, I'm {bot} AI, Your personal Assistant")
    while 1:
        say("How can I help you sir?")
        t = take_command()

        if "close" in t or "exit" in t:
            say("I'm signing of sir, Please Come again whenever you want")
            c += 1
            return 0

        elif "open site" in t:
            import webbrowser

            site = get_last_word(t)
            try:
                webbrowser.open(f"https://{site}")
                say(f"Opening {site} sir")
            except Exception as e:
                print(f"Error in Open Site: {e}")
                say("I could not find the site sir, here is the search results")
                webbrowser.open(f"https://www.google.com/search?q={site}")

        elif "what's the time" in t:
            import datetime

            say("ok I'm checking the time sir")
            say(f"Sir the time is {datetime.datetime.now().strftime("%H %M %S")}")

        elif "what's the weather" in t or "what's the temperature" in t:
            get_weather_report(get_last_word(t))

        elif "what's the charge" in t or "what's the battery" in t:
            check_battery()

        elif "my internet speed" in t:
            check_internet_speed()

        elif "volume up" in t or "volume high" in t:
            p.press("volumeup")
            say("volume up")

        elif "volume down" in t or "volume low" in t:
            p.press("volumedown")
            say("volume down")

        elif "volume mute" in t:
            say("muting the device sir")
            p.press("volumemute")

        elif "volume unmute" in t:
            p.press("volumemute")
            say("The device has been un-muted sir")

        elif "take screenshot" in t or "take a screenshot" in t:
            take_screenshot()

        elif ("find location" in t or "find the location" in t or
              "find a location" in t):
            find_location()

        else:
            prompt = [{"role": "user", "content": t}]
            ai(prompt)


if close == 0:
    try:
        face_auth(main, close)
    except Exception as exc:
        err = exc
        print(f"Have a nice day sir")
