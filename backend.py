import pyttsx3
import speech_recognition as sr
import datetime
import pyautogui
import requests
import wikipedia
import webbrowser
import os
import smtplib
import psutil


# ---------------------------------------------------------
# Initialize Text-to-Speech Engine
# ---------------------------------------------------------

try:
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")

    if voices:
        engine.setProperty("voice", voices[1].id)

except Exception as e:
    print("SAPI5 driver error:", e)
    engine = None


# ---------------------------------------------------------
# Text-to-Speech Function
# ---------------------------------------------------------

def say(text):
    global engine

    if engine:
        print(f"Saying: {text}")

        engine.say(text)
        engine.runAndWait()

    else:
        print("Text-to-speech engine not initialized. Cannot speak.")


# ---------------------------------------------------------
# Listen Function
# ---------------------------------------------------------

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        recognizer.pause_threshold = 1

        try:
            audio = recognizer.listen(source)

            # Recognize speech using Google Speech Recognition
            command = recognizer.recognize_google(
                audio,
                language="en-in"
            )

            print(f"You said: {command}")

            return command

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""

        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            return ""

        except Exception as e:
            print(f"Error while listening: {e}")
            return ""


# ---------------------------------------------------------
# Wish Me Function
# ---------------------------------------------------------

def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        say("Good Morning!")

    elif hour >= 12 and hour < 18:
        say("Good Afternoon!")

    else:
        say("Good Evening!")


# ---------------------------------------------------------
# Take Command Function
# ---------------------------------------------------------

def takeCommand():
    """
    Takes microphone input from the user
    and returns the recognized speech.
    """

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        r.pause_threshold = 1

        try:
            audio = r.listen(
                source,
                timeout=5
            )

        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return "None"

    try:
        print("Recognizing...")

        query = r.recognize_google(
            audio,
            language="en-in"
        )

        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"

    return query


# ---------------------------------------------------------
# Open Browser Function
# ---------------------------------------------------------

def open_browser(browser_name):
    """Open a browser based on its name."""

    browser_urls = {
        "chrome": "https://www.google.com/chrome/",
        "edge": "https://www.microsoft.com/edge",
        "firefox": "https://www.mozilla.org/firefox/"
    }

    if browser_name in browser_urls:

        try:
            webbrowser.open(
                browser_urls[browser_name]
            )

            say(
                f"Opening {browser_name.capitalize()}."
            )

        except Exception as e:

            say(
                f"Failed to open {browser_name}. "
                f"Error: {str(e)}"
            )

    else:
        say(
            f"I don't know how to open {browser_name}."
        )


# ---------------------------------------------------------
# Close Browser Function
# ---------------------------------------------------------

def close_browser(browser_name):
    """Close browser processes based on their name."""

    browser_processes = {
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
        "firefox": "firefox.exe"
    }

    if browser_name in browser_processes:

        process_name = browser_processes[browser_name]

        try:
            os.system(
                f"taskkill /F /IM {process_name}"
            )

            say(
                f"Closing {browser_name.capitalize()}."
            )

        except Exception as e:

            say(
                f"Failed to close {browser_name}. "
                f"Error: {str(e)}"
            )

    else:

        say(
            f"I don't know how to close {browser_name}."
        )


# ---------------------------------------------------------
# Get Weather Function
# ---------------------------------------------------------

def get_weather(city):

    api_key = "94959dd2a582bb7d0b35b950a464732b"

    base_url = "http://api.weatherstack.com/current"

    params = {
        "access_key": api_key,
        "query": city
    }

    try:
        response = requests.get(
            base_url,
            params=params,
            timeout=10
        )

        data = response.json()

        if "current" in data:

            temperature = data["current"]["temperature"]

            weather_descriptions = ", ".join(
                data["current"]["weather_descriptions"]
            )

            humidity = data["current"]["humidity"]

            return (
                f"The weather in {city} is "
                f"{weather_descriptions} with a temperature "
                f"of {temperature}°C and humidity of "
                f"{humidity}%."
            )

        else:

            return (
                "Sorry, I couldn't find the weather "
                "information for that location."
            )

    except Exception as e:

        print(f"Weather API error: {e}")

        return (
            "Sorry, I was unable to retrieve "
            "the weather information."
        )


# ---------------------------------------------------------
# Say Weather Function
# ---------------------------------------------------------

def say_weather(city):

    weather = get_weather(city)

    say(weather)


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

if __name__ == "__main__":

    print("AURA")

    wishMe()

    say("Hello, how may I help you?")

    failure_count = 0

    # Maximum allowed failures
    max_failures = 2

    while True:

        print("Listening...")

        command = listen()

        # -------------------------------------------------
        # Check if command was empty
        # -------------------------------------------------

        if not command.strip():

            failure_count += 1

            say(
                "I couldn't hear you clearly. "
                "Please try again."
            )

            if failure_count >= max_failures:

                say(
                    "I'm having trouble understanding. "
                    "Exiting now."
                )

                print(
                    "Too many failed attempts. Exiting."
                )

                break

            continue

        # Reset failure count
        failure_count = 0

        # -------------------------------------------------
        # Check for Aura keyword
        # -------------------------------------------------

        if not command.lower().startswith("aura"):

            say(
                "Please start your command with "
                "'Aura' so I can assist you."
            )

            continue

        # Remove "Aura" from command
        command = (
            command
            .lower()
            .replace("aura", "")
            .strip()
        )

        # -------------------------------------------------
        # Websites
        # -------------------------------------------------

        sites = [
            ["youtube", "https://www.youtube.com/"],
            ["google", "https://www.google.com/"],
            ["wikipedia", "https://www.wikipedia.com/"]
        ]

        opened_site = False

        for site in sites:

            if f"open {site[0]}".lower() in command.lower():

                say(
                    f"Opening {site[0]}"
                )

                webbrowser.open(site[1])

                opened_site = True

                break

        if opened_site:
            continue

        # -------------------------------------------------
        # Greeting
        # -------------------------------------------------

        if "hello" in command.lower():

            say(
                "Hello, how may I assist you?"
            )

        # -------------------------------------------------
        # Name
        # -------------------------------------------------

        elif "your name" in command.lower():

            say(
                "My name is AURA."
            )

        # -------------------------------------------------
        # Good Morning / Afternoon / Evening
        # -------------------------------------------------

        elif any(
            greeting in command.lower()
            for greeting in [
                "good morning",
                "good afternoon",
                "good evening"
            ]
        ):

            say(
                f"{command.capitalize()}! "
                "How can I assist you today?"
            )

        # -------------------------------------------------
        # Camera
        # -------------------------------------------------

        elif "open camera" in command.lower():

            os.system(
                "start microsoft.windows.camera:"
            )

            say("Opening camera.")

        elif "close camera" in command.lower():

            os.system(
                "taskkill /F /IM WindowsCamera.exe"
            )

            say("Closing camera.")

        # -------------------------------------------------
        # WhatsApp
        # -------------------------------------------------

        elif "open whatsapp" in command.lower():

            os.system(
                "start whatsapp:"
            )

            say(
                "Aura is opening WhatsApp for you."
            )

        elif "close whatsapp" in command.lower():

            os.system(
                "taskkill /F /IM WhatsApp.exe"
            )

            say(
                "Closing WhatsApp."
            )

        # -------------------------------------------------
        # Calculator
        # -------------------------------------------------

        elif "open calculator" in command.lower():

            os.system(
                "start calculator:"
            )

            say("Opening calculator.")

        elif "close calculator" in command.lower():

            os.system(
                "taskkill /F /IM CalculatorApp.exe"
            )

            say("Closing calculator.")

        # -------------------------------------------------
        # Time
        # -------------------------------------------------

        elif "time" in command.lower():

            strfTime = datetime.datetime.now().strftime(
                "%H:%M:%S"
            )

            say(
                f"The time is {strfTime}"
            )

            print(strfTime)

        # -------------------------------------------------
        # Google Search
        # -------------------------------------------------

        elif "search google" in command.lower():

            say(
                "What should I search for?"
            )

            query = listen()

            if query:

                webbrowser.open(
                    "https://www.google.com/search?q="
                    + query
                )

                say(
                    f"Searching Google for {query}."
                )

        # -------------------------------------------------
        # Refresh
        # -------------------------------------------------

        elif "refresh" in command.lower():

            pyautogui.hotkey(
                "ctrl",
                "r"
            )

            say("Refreshing the screen.")

        # -------------------------------------------------
        # Shutdown
        # -------------------------------------------------

        elif "shutdown" in command.lower():

            say("Shutting down.")

            os.system(
                "shutdown /s /t 0"
            )

        # -------------------------------------------------
        # Exit
        # -------------------------------------------------

        elif "exit" in command.lower() or "quit" in command.lower():

            say("Goodbye!")

            break

        # -------------------------------------------------
        # Chrome
        # -------------------------------------------------

        elif "open chrome" in command.lower():

            open_browser("chrome")

        elif "close chrome" in command.lower():

            close_browser("chrome")

        # -------------------------------------------------
        # Firefox
        # -------------------------------------------------

        elif "open firefox" in command.lower():

            open_browser("firefox")

        elif "close firefox" in command.lower():

            close_browser("firefox")

        # -------------------------------------------------
        # Edge
        # -------------------------------------------------

        elif "open edge" in command.lower():

            open_browser("edge")

        elif "close edge" in command.lower():

            close_browser("edge")

        # -------------------------------------------------
        # Google Classroom
        # -------------------------------------------------

        elif "open classroom" in command.lower():

            webbrowser.open(
                "https://classroom.google.com/h"
            )

            say("Opening Google Classroom.")

        # -------------------------------------------------
        # Weather
        # -------------------------------------------------

        elif "weather" in command.lower():

            say(
                "Please tell me the city name."
            )

            city = listen()

            if city:

                say_weather(city)

            else:

                say(
                    "I couldn't hear the city name."
                )

        # -------------------------------------------------
        # Unknown Command
        # -------------------------------------------------

        else:

            say(
                "I'm not sure what you mean. "
                "Here are some things you can ask me: "
                "open WhatsApp, check the weather, "
                "or tell the time."
            )
