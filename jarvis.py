import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import os
import random
import tkinter as tk
import threading
import math
from PIL import Image, ImageTk, ImageEnhance
from itertools import cycle
import requests
import wikipedia

# Initialize recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Jokes for fun
jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "I'm on a seafood diet. I see food and I eat it.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "I would tell you a construction joke, but I'm still working on it."
]

# Global color state
arc_color = None

# Speak function
def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Listen function
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"API request error: {e}")
        return ""

# Get Weather Info
def get_weather():
    api_key = "your_openweather_api_key"
    city = "YourCityName"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            main = data["main"]
            temp = main["temp"]
            weather = data["weather"][0]["description"]
            speak(f"The current temperature in {city} is {temp} degrees Celsius with {weather}.")
        else:
            speak("Sorry, I couldn't fetch the weather information.")
    except:
        speak("Weather service is currently unavailable.")

# Wikipedia Search
def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError:
        speak("Can you be more specific?")
    except Exception:
        speak("I couldn't find that information.")

# Take Note
def take_note():
    speak("What would you like me to write?")
    note = listen()
    with open("notes.txt", "a") as f:
        f.write(f"{note}\n")
    speak("Note saved.")

# Respond to commands
def handle_command(command):
    global arc_color

    if "hello" in command:
        speak("Hello! How can I help you?")
    elif "time" in command:
        current_time = time.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "play music" in command:
        speak("Playing music on YouTube.")
        webbrowser.open("https://music.youtube.com")
    elif "open google" in command:
        speak("Open Google.")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        speak("Open YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in command:
        speak("Open Facebook.")
        webbrowser.open("https://www.facebook.com")
    elif "open instagram" in command:
        speak("Open Instagram.")
        webbrowser.open("https://www.instagram.com")
    elif "open notepad" in command:
        speak("Open Notepad.")
        os.system("notepad.exe")
    elif "open chrome" in command or "open google chrome" in command:
        speak("Opening Google Chrome.")
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        os.startfile(chrome_path)
    elif "joke" in command:
        speak(random.choice(jokes))
    elif "weather" in command:
        get_weather()
    elif "note" in command:
        take_note()
    elif "search" in command:
        query = command.replace("search", "")
        search_wikipedia(query)
    elif "exit" in command or "khuda hafiz" in command or "shutdown" in command:
        speak("Shutting down. Goodbye!")
        os._exit(0)
    elif "color" in command or "colour" in command:
        if "red" in command:
            arc_color = "red"
            speak("Changing color to red")
        elif "blue" in command:
            arc_color = "blue"
            speak("Changing color to blue")
        elif "green" in command:
            arc_color = "green"
            speak("Changing color to green")
        elif "yellow" in command:
            arc_color = "yellow"
            speak("Changing color to yellow")
        elif "white" in command:
            arc_color = "white"
            speak("Changing color to white")
        elif "cyan" in command:
            arc_color = "cyan"
            speak("Changing color to cyan")
        else:
            speak("Sorry, I don't recognize that color")
    else:
        speak("Sorry, I didn't understand that. Try again.")

# Display Iron Man animated face (not fullscreen)
def display_face():
    canvas.delete("all")
    gif_path = "man.gif"
    ironman_gif = Image.open(gif_path)
    frames = []

    try:
        while True:
            frame = ironman_gif.copy()
            frame = frame.resize((800, 600), Image.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame))
            ironman_gif.seek(len(frames))
    except EOFError:
        pass

    frame_cycle = cycle(frames)

    def animate():
        frame = next(frame_cycle)
        canvas.delete("all")
        canvas.create_image(screen_width // 2, screen_height // 2, anchor="center", image=frame)
        canvas.image = frame
        canvas.after(100, animate)

    animate()

# Back button functionality
def go_back():
    app.destroy()
    os.system("python your_main_menu_script.py")  # Replace with your actual main menu script

# Jarvis activation loop
def run_jarvis():
    speak("Hello Hasin, I am Jarvis. your voice assistant.")
    while True:
        command = listen()
        if "hey jarvis" in command:
            status_label.config(text="Listening...")
            speak("Hii Hasin, how can I help you.")
            command = listen()
            if command:
                handle_command(command)
            status_label.config(text="Say 'Hey Jarvis' to activate")

# GUI setup
app = tk.Tk()
app.title("Jarvis AI")
app.configure(bg="black")
# Removed fullscreen
# app.attributes("-fullscreen", True)

screen_width = 1024
screen_height = 768

canvas = tk.Canvas(app, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
canvas.pack()

status_label = tk.Label(app, text="Say 'Hey Jarvis' to activate", fg="cyan", bg="black", font=("Segoe UI", 16))
status_label.place(x=20, y=20)

# Back Button
back_button = tk.Button(app, text="Back", command=go_back, font=("Segoe UI", 12), bg="gray", fg="white")
back_button.place(x=20, y=60)

# Start threads
threading.Thread(target=display_face, daemon=True).start()
threading.Thread(target=run_jarvis, daemon=True).start()

app.mainloop()
