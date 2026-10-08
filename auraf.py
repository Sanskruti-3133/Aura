import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import os
import webbrowser
import pyautogui

from backend import (
    takeCommand,
    open_browser,
    close_browser,
    say_weather,
    listen
)

from datetime import datetime


# Initialize TTS Engine
def init_tts():
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        return engine

    except Exception as e:
        print("TTS Engine Initialization Error:", e)
        return None


# Custom say() function
def say(text):
    # Always display the text in the output area,
    # even if TTS fails
    output_area.insert(tk.END, f"Aura: {text}\n")
    output_area.see(tk.END)

    if engine:
        engine.say(text)
        engine.runAndWait()
    else:
        print("TTS Engine not initialized. Text displayed in GUI.")


# Process Commands
def process_command(command):

    # Display the user's command in the output area
    output_area.insert(tk.END, f"You: {command}\n")
    output_area.see(tk.END)

    command = command.lower()

    if "aura" in command:

        command = command.replace("aura", "").strip()

        # Handle opening browsers
        if "open chrome" in command:
            open_browser("chrome")

        elif "open firefox" in command:
            open_browser("firefox")

        elif "open edge" in command:
            open_browser("edge")

        # Handle closing browsers
        elif "close chrome" in command:
            close_browser("chrome")

        elif "close firefox" in command:
            close_browser("firefox")

        elif "close edge" in command:
            close_browser("edge")

        # Handle weather command
        elif "weather" in command:

            city = command.split("weather in")[-1].strip()

            if city:
                say_weather(city)
            else:
                say("Please specify the city.")

        # Handle time command
        elif "time" in command:

            current_time = datetime.now().strftime("%H:%M:%S")
            say(f"The current time is {current_time}")

        # Handle opening WhatsApp
        elif "open whatsapp" in command:

            os.system("start whatsapp:")
            say("Aura is opening WhatsApp for you.")

        # Handle closing WhatsApp
        elif "close whatsapp" in command:

            os.system("taskkill /F /IM WhatsApp.exe")
            say("Closing WhatsApp...")

        # Handle opening YouTube
        elif "open youtube" in command:

            webbrowser.open("https://www.youtube.com/")
            say("Opening YouTube.")

        # Handle opening Google
        elif "open google" in command:

            webbrowser.open("https://www.google.com/")
            say("Opening Google.")

        # Handle opening Wikipedia
        elif "open wikipedia" in command:

            webbrowser.open("https://www.wikipedia.com/")
            say("Opening Wikipedia.")

        # Handle opening Google Classroom
        elif "open classroom" in command:

            webbrowser.open("https://classroom.google.com/h")
            say("Opening Google Classroom.")

        # Handle opening camera
        elif "open camera" in command:

            os.system("start microsoft.windows.camera:")
            say("Opening camera.")

        # Handle closing camera
        elif "close camera" in command:

            os.system("taskkill /F /IM WindowsCamera.exe")
            say("Closing camera.")

        # Handle opening calculator
        elif "open calculator" in command:

            os.system("start calculator:")
            say("Opening calculator.")

        # Handle closing calculator
        elif "close calculator" in command:

            os.system("taskkill /F /IM CalculatorApp.exe")
            say("Closing calculator.")

        # Handle refreshing the screen
        elif "refresh" in command:

            pyautogui.hotkey("ctrl", "r")
            say("Refreshing the screen.")

        # Handle shutdown command
        elif "shutdown" in command:

            os.system("shutdown /s /t 0")
            say("Shutting down...")

        # Handle exit command
        elif "exit" in command or "quit" in command:

            say("Goodbye!")
            app.quit()

        # Handle greeting commands
        elif any(
            greeting in command
            for greeting in ["hello", "hi", "hey"]
        ):

            say("Hello! How can I assist you?")

        # Handle name command
        elif "your name" in command:

            say("My name is Aura.")

        # Handle unrecognized commands
        else:

            say(
                "I'm not sure what you mean. "
                "Here are some things you can ask me: "
                "open WhatsApp, check the weather, or tell the time."
            )

    else:

        say(
            "Please start your command with 'Aura' "
            "so I can assist you."
        )


# Continuous Listening Function
def start_listening():

    listen_button.config(bg="#34A853")

    say("I'm listening...")

    while True:

        command = listen()

        entry.delete(0, tk.END)
        entry.insert(0, command)

        process_command(command)

        # Exit the loop if the user says
        # "Aura exit" or "Aura quit"
        if (
            "exit" in command.lower()
            or "quit" in command.lower()
        ):
            break

    listen_button.config(bg="#4285F4")


# Tkinter GUI Setup
def setup_gui():

    app = tk.Tk()

    app.title("Aura - Your Voice Assistant")
    app.geometry("600x500")
    app.configure(bg="#FFFFFF")

    # Header
    header_frame = tk.Frame(
        app,
        bg="#FFFFFF"
    )

    header_frame.pack(pady=10)

    left_label = tk.Label(
        header_frame,
        text="Call me Aura",
        font=("Arial", 18, "bold"),
        bg="#FFFFFF",
        fg="#34A853"
    )

    left_label.pack()

    # Output area
    global output_area

    output_area = scrolledtext.ScrolledText(
        app,
        wrap=tk.WORD,
        font=("Arial", 12),
        height=15,
        width=60,
        bg="#F1F3F4"
    )

    output_area.pack(pady=10)

    # Text entry
    global entry

    entry = tk.Entry(
        app,
        font=("Arial", 14),
        width=50,
        bg="#E8F0FE"
    )

    entry.pack(pady=5)

    # Button frame
    button_frame = tk.Frame(
        app,
        bg="#FFFFFF"
    )

    button_frame.pack(pady=10)

    # Listen button
    global listen_button

    listen_button = tk.Button(
        button_frame,
        text=" 🎙 ",
        font=("Arial", 18),
        command=start_listening,
        bg="#4285F4",
        fg="#FFFFFF",
        width=4,
        height=2,
        bd=0,
        relief=tk.FLAT
    )

    listen_button.pack(
        side=tk.LEFT,
        padx=20
    )

    listen_button.config(
        highlightbackground="#FFFFFF"
    )

    # Quit button
    quit_button = tk.Button(
        app,
        text="Quit",
        font=("Arial", 12),
        command=app.quit,
        bg="#EA4335",
        fg="#FFFFFF",
        width=10
    )

    quit_button.pack(pady=5)

    return app


# Define wishMe()
def wishMe():

    hour = int(datetime.now().hour)

    if hour >= 0 and hour < 12:

        say("Good Morning!")

    elif hour >= 12 and hour < 18:

        say("Good Afternoon!")

    else:

        say("Good Evening!")

    say("Hello, how may I help you?")


# Main Program
if __name__ == "__main__":

    engine = init_tts()

    app = setup_gui()

    # Greet the user as soon as the app starts
    wishMe()

    app.mainloop()
