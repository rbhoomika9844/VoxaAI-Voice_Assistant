import speech_recognition as sr 
import pyttsx3 
import pywhatkit 
import wikipedia 
import datetime 
import pyjokes 
import webbrowser 
import googlesearch
def speak(text): 
    engine = pyttsx3.init() 
    voices = engine.getProperty('voices')  # Get available voices 
# Set female voice (index 1 or 2 depending on your system) 
    engine.setProperty('voice', voices[1].id) 
    engine.say(text) 
    engine.runAndWait() 
def recognize_speech(): 
    recognizer = sr.Recognizer() 
    with sr.Microphone() as source: 
        print("Listening...") 
        recognizer.adjust_for_ambient_noise(source) 
        audio = recognizer.listen(source) 
        try: 
            print("Recognizing...") 
            text = recognizer.recognize_google(audio) 
            print("You said:", text) 
            return text.lower() 
        except sr.UnknownValueError: 
            print("Sorry, I couldn't understand what you said.") 
            return None 
        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service;{0}".format(e)) 
    return None 
def get_weather_google(city): 
    try: 
        query = f"Weather in {city}" 
        search_results = googlesearch.search(query, num=1, stop=1, pause=2) 
        for result in search_results: 
            if "°C" in result: 
                return result 
        return "Sorry, I couldn't fetch the weather information for that city." 
    except Exception as e: 
        return f"An error occurred: {e}" 
def search_images(query): 
    try: 
        url = f"https://www.google.com/search?tbm=isch&q={query}" 
        webbrowser.open(url) 
    except Exception as e: 
        print("An error occurred while searching for images:", e) 
def main(): 
    print("Waiting for 'Alexa' wake word...") 
    while True: 
        user_input = recognize_speech() 
        if user_input and "alexa" in user_input: 
            speak("Hello! How can I assist you today?") 
            break 
    while True: 
        user_input = recognize_speech() 
        if user_input: 
            if "play" in user_input: 
                song = user_input.split("play")[-1].strip() 
                speak(f"Playing {song} on YouTube.") 
                pywhatkit.playonyt(song) 
            elif any(word in user_input for word in ["time", "date"]): 
                # Get the current time and date 
                now = datetime.datetime.now() 
                response = f"Today is {now.strftime('%A, %B %d, %Y')}. The time is {now.strftime('%I:%M %p')}." 
                speak(response) 
            elif "joke" in user_input: 
                # Fetch and speak a joke 
                joke = pyjokes.get_joke() 
                speak(joke) 
            elif "weather in" in user_input: 
                city = user_input.split("weather in")[-1].strip() 
                response = get_weather_google(city) 
                speak(response)    
            elif "what is" in user_input: 
                # Get information from Wikipedia 
                query = user_input.replace("what is", "").strip() 
                try: 
                    info = wikipedia.summary(query, sentences=2) 
                    speak(info) 
                except wikipedia.exceptions.DisambiguationError as e: 
                    options = e.options[:3]   
                    speak(f"Multiple results found. Did you mean {', '.join(options)}?") 
                except wikipedia.exceptions.PageError: 
                    speak("Sorry, I couldn't find information on that topic.") 
            elif "when is" in user_input: 
                # Extract the query from user input 
                query = user_input.split("when is")[-1].strip() 
                # Get information from Wikipedia about the query 
                try: 
                    info = wikipedia.summary(query, sentences=2) 
                    speak(info) 
                except wikipedia.exceptions.DisambiguationError as e: 
                    options = e.options[:3]   
                    speak(f"Multiple results found. Did you mean {', '.join(options)}?") 
                except wikipedia.exceptions.PageError: 
                    speak("Sorry, I couldn't find information on that topic.") 
            elif "image of" in user_input or "picture of" in user_input: 
                thing = user_input.split("image of")[-1].strip() if "image of" in user_input else user_input.split("picture of")[-1].strip() 
                search_images(thing) 
            elif any(word in user_input for word in ["goodnight", "goodbye", "bye"]): 
                speak("Goodbye! Have a great day.") 
                break 
            else: 
                speak("Sorry, I didn't understand that.") 
if __name__ == "__main__": 
    main()