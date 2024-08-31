import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import openai
import pywhatkit


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "enter your news api"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    openai.api_key = "Enter your openai api"  

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Cloud. Speak in Hindi, Englis and Bengali most you try hindi"},
                {"role": "user", "content": command}
            ]
        )

        # Extract the assistant's response
        answer = response['choices'][0]['message']['content']
        return answer

    except Exception as e:
        return f"An error occurred: {e}"
    
    return(completion.choices[0].message.content)
    
def play_youtube_video(command):
    if command:
        print(f"Playing on YouTube: {command}")
        pywhatkit.playonyt(command)

def search_on_google(command):
    if command:
        print(f"Searching on Google: {command}")
        pywhatkit.search(command)


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif c.startswith("play"):
        play_youtube_video(c[5:])
    elif c.startswith("search"):
        search_on_google(c[7:])
 
    elif "tell me news" in c.lower():
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])
                
                if not articles:
                    speak("Sorry, I couldn't find any news articles.")
                else:
                    for article in articles:
                        speak(article["title"])
            else:
                speak("Sorry, I couldn't retrieve the news right now. Please try again later.")


    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)
        

if __name__ == "__main__":
    speak("Initializing jarvis......")

    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))
