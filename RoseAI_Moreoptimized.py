import pyttsx3 as p
import datetime as d
import random
import webbrowser as wb
from search_website import search_website
from speech import input_speech
from fuzzywuzzy import fuzz
from open_app import open_app
from close_app import close_app
from hugchat import hugchat

# Initialize text-to-speech engine

# At top of RoseAI_Moreoptimized.py
ui_callback = None

def set_ui_callback(callback):
    """Set the UI callback for sending text to the GUI."""
    global ui_callback
    ui_callback = callback

def send_to_ui(text, msg_type="status"):
    """Send messages to UI if available, else print to console."""
    if ui_callback:
        ui_callback(text, msg_type)
    else:
        print(text)

v = p.init('sapi5')
v.setProperty("voice", v.getProperty("voices")[2].id)

WEBSITES = {
    "facebook": "https://www.facebook.com",
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "amazon": "https://www.amazon.in",
    "wikipedia": "https://www.wikipedia.com",
}

APP_COMMANDS = {
    "chrome": "chrome.exe",
    "calculator": "calc",
    "clock": "ms-clock",
    "brave": "brave.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "word": r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
    "powerpoint": r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
    "photos": "ms-photos",
    "file explorer": "explorer.exe",
    "paint": "mspaint.exe"
}

EXIT_PHRASES = ["rose shut down", "rose shutdown", "rose exit", "rose quit", "rose goodbye", "rose bye",
                "shut down", "shutdown", "exit", "quit", "goodbye", "bye", "Rose stop", "stop"]

FAREWELL_MESSAGES = [
    "Goodbye! Have a great day!",
    "Shutting down now. Take care!",
    "It was a pleasure assisting you. Take care!",
    "I'm signing off now. See you next time!"
]

REPORTING_MESSAGES = [
    "How may I assist you?",
    "I'm here to assist you.",
    "What may I assist you with?",
    "Your wish is my command!"
]

def speak(speech):
    send_to_ui(speech, "rose")  # Show in UI
    v.say(speech)
    v.runAndWait()

def greet():
    hour = d.datetime.now().hour
    period = "morning" if hour < 12 else "afternoon" if hour < 18 else "evening"
    speak(f"Good {period} sir")

def parse_intent(query):
    words = query.lower().split()
    intents = {"open", "launch", "start", "search", "search for", "run", "close", "shut", "exit"}
    intent = next((w for w in words if w in intents), None)
    target = next((w for w in words if w in WEBSITES or w in APP_COMMANDS), None)

    if "on" in words and any(site in words for site in WEBSITES):
        site = next(site for site in WEBSITES if site in words)
        search_term = " ".join(words[words.index("on") + 1:words.index(site)] + words[words.index(intent) + 1:words.index("on")])
        return "specific_search", (site, search_term)

    if intent and target:
        return intent, ("website" if target in WEBSITES else "app", target)
    if intent in {"open", "search", "search for"}:
        return intent, ("search", " ".join(w for w in words if words.index(w) > words.index(intent)))
    return "unknown", None

def chatBot(query):
    cookie_path = r"E:\ROSE AI\huggingface.co.json"
    
    try:
        chatbot = hugchat.ChatBot(cookie_path=cookie_path)
        chatbot.switch_llm(2)
        conversation_id = chatbot.new_conversation()
        chatbot.change_conversation(conversation_id)
        response = chatbot.chat(query.lower())

        if response:
            print(response)
            speak(response)
            return response
        else:
            speak("I'm sorry, I didn't get a valid response from the chatbot.")
            print("Error: No response received from the chatbot.")
            return None

    except FileNotFoundError:
        speak("The required authentication file is missing. Please check the path and try again.")
        print("Error: The authentication cookie file is missing.")

    except Exception as e:
        speak("There was an unexpected error communicating with the chatbot. Please try again later.")
        print(f"Error: {str(e)}")

    return None
def take_input():
    while True:
        speech_text = input_speech()
        if not speech_text:
            speak("I didn't catch that. Could you please repeat?")
            continue
        send_to_ui(speech_text, "user")

        if any(phrase in speech_text.lower() for phrase in EXIT_PHRASES):
            speak(random.choice(FAREWELL_MESSAGES))
            return

        intent, target = parse_intent(speech_text)
        if "the time" in speech_text.lower():
            speak(d.datetime.now().strftime("The time right now is %I:%M"))
            continue

        if intent in {"open", "search", "search for", "specific_search"}:
            handle_intent(intent, target)
        elif intent == "close":
            handle_close(target)
        else:
            chatBot(speech_text)

def handle_intent(intent, target):
    if intent == "specific_search":
        site, search_term = target
        perform_search(search_term, site)

    elif target[0] == "website":
        url = WEBSITES.get(target[1]) or search_website(target[1])
        open_url_or_app(url, target[1], "Opening")
        speak(f"opening {target[1]}")
    elif target[0] == "app":
        app_command = open_app(target[1])
        if isinstance(app_command, str):
            open_url_or_app(app_command, target[1], "Opening")
            speak(f"opening {target[1]}")
        else:
            print(f"Error: App '{target[1]}' could not be opened.")
            speak(f"Sorry, I couldn't open the app {target[1]}.")
    elif target[0] == "search":
        url = search_website(target[1])
        open_url_or_app(url, target[1], "Searching")
        speak(f"searching {target[1]}")


def handle_close(target):
    if target and target[0] == "app" and close_app(target[1]):
        speak(f"Closing {target[1]}")
    else:
        speak(f"I'm not sure how to close '{target[1] if target else 'unknown'}'. Could you be more specific?")

def perform_search(search_term, site):
    url = search_website(search_term, site)
    open_url_or_app(url, f"{search_term} on {site}", "Searching")

def open_url_or_app(action_result, target, action_message):
    if isinstance(action_result, str):
        if "http" in action_result:   
            wb.open(action_result)
        send_to_ui(f"{action_message} the app: {target}", "status")
    else:
        send_to_ui(f"Invalid action_result type: {type(action_result)}", "status")

def listen_for_wakeword():
    send_to_ui("Listening for wake word 'Hello Rose'...", "status")
    while True:
        wake_word_text = input_speech().lower()
        if fuzz.ratio(wake_word_text, "hello rose") > 70:
            send_to_ui("Wake word 'Hello Rose' detected!", "status")
            speak(f"Yes, {random.choice(REPORTING_MESSAGES)}?")
            take_input()

def main():
    listen_for_wakeword()

if __name__ == "__main__":
    main()
