import speech_recognition as sr
import pyttsx3
import time

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 180)

WAKE_WORD = "hey jarvis"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤 Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("🗣️ You said:", command)
            return command
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Network error.")
            return ""

def activate_assistant():
    speak("Yes? How can I help?")
    command = listen()

    if "time" in command:
        import datetime
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "your name" in command:
        speak("I am Jarvis, your voice assistant.")

    elif "stop" in command or "goodbye" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("Sorry, I didn't understand that.")

# 🔄 Main loop
while True:
    print("Waiting for wake word...")
    command = listen()
    if WAKE_WORD in command:
        activate_assistant()
    time.sleep(1)
