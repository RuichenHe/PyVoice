import time
from datetime import date
import speech_recognition as sr

def recognizeSpeechFromMic(recognizer, microphone, recognizerMode):

    print("Ready for input:")
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    print("Recieved signal, recognizing...")
    try:
        if recognizerMode == "VOSK":
            temp = recognizer.recognize_vosk(audio).split(" : ")[1].replace('"', '').replace('}', '').replace('\n', '')
            response["transcription"] = temp
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    return response
if __name__ == "__main__":
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    recognizerMode = "VOSK"
    print("Voice Detection API Start...")
    #### Initlized model here
    ####For VOSK:
    if recognizerMode == "VOSK":
        initAudioFile = sr.AudioFile('init.wav')
        with initAudioFile as source:
            initAudio = recognizer.record(source)
        recognizer.recognize_vosk(initAudio)
    print("Recognizer initialized")
    keepDetection = True
    while keepDetection:
        speakContent = recognizeSpeechFromMic(recognizer, microphone, recognizerMode)
        print("You said: {}".format(speakContent["transcription"]))
        if speakContent["transcription"] == "what is the time now" or speakContent["transcription"] == "what time is it":
            print("Current time: " + time.strftime("%H:%M:%S", time.localtime()))
        elif speakContent["transcription"] == "what is the date today":
            print("Current date: " + str(date.today()))
        elif speakContent["transcription"] == "detection terminate":
            keepDetection = False
    print("Voice Detection API terminated.")