import speech_recognition as sr
def input_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        recognizer.non_speaking_duration = 2
        recognizer.pause_threshold = 2
        try:
            audio = recognizer.listen(mic, phrase_time_limit = 15)
            query = recognizer.recognize_google(audio, language="en-in")
            print(f'You said: {query}')
            return query
        except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError, TimeoutError):
            return "Couldn't hear you, please try again sir."