import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pyaudio

# Initialize the TTS Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Choose a female voice

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am JARVIS, your assistant. How can I help you?")

def take_command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            speak("Listening...")
            r.adjust_for_ambient_noise(source, duration=1)

            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                speak("I didn't hear anything. Please try again.")
                return ""

    except OSError:
        speak("Microphone not detected. Please check your audio input device.")
        return ""

    try:
        command = r.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please say it again.")
        return ""
    except sr.RequestError:
        speak("Sorry, I'm unable to reach the speech service.")
        return ""

def run_jarvis():
    greet()
    while True:
        command = take_command()

        if 'time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        elif 'open youtube' in command:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif 'open google' in command:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif 'your name' in command:
            speak("I am JARVIS, your AI assistant.")

        elif 'exit' in command or 'stop' in command or 'quit' in command:
            speak("Goodbye! Have a great day.")
            break

        elif command.strip() == "":
            continue

        else:
            speak("Sorry, I didn't get that. Please try again.")

# Run the assistant
if __name__ == "__main__":
    run_jarvis()
