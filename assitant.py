import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import requests

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

def open_website(url):
    webbrowser.open(url)
    return f"Opening {url}"

def get_weather(city):
    api_key = "your_openweathermap_api_key"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_description = data["weather"][0]["description"]
        return f"The temperature in {city} is {temperature - 273.15:.2f}°C with {weather_description}."
    else:
        return "City not found."

def main():
    speak("Hello, I am your virtual assistant. How can I help you today?")
    while True:
        command = listen()

        if "time" in command:
            current_time = get_time()
            speak(f"The current time is {current_time}")
        elif "open" in command and "website" in command:
            speak("Which website would you like to open?")
            site = listen()
            response = open_website(site)
            speak(response)
        elif "weather" in command:
            speak("Which city's weather would you like to know?")
            city = listen()
            weather_info = get_weather(city)
            speak(weather_info)
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I can only tell the time, open websites, and fetch weather information. Please try again.")

if __name__ == "__main__":
    main()
