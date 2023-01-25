import time
from datetime import date
import speech_recognition as sr

def recognizeSpeechFromMic(recognizer, microphone, recognizerMode):
    """_summary_

    Args:
        recognizer (sr.Recognizer): voice recognizer from speech_recognition package
        microphone (sr.Microphone): microphone handler from speech_recognition package
        recognizerMode (string): mode to decide which API to use during operation, currently support: VOSK
    Returns:
        response: a dict, contains success flag, error message, and transcription result 
    """
    print("Ready for input:")
    #Check if the input parameter fullfills the requirement
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    if not isinstance(recognizerMode, str):
        raise TypeError("`recognizerMode` must be `string` instance")
    #Handle the Audio I/O input
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
            #Segment the returned string value to obtain final voice recognition result
            temp = recognizer.recognize_vosk(audio).split(" : ")[1].replace('"', '').replace('}', '').replace('\n', '')
            response["transcription"] = temp
        elif recognizerMode == "Sphinx":
            temp = recognizer.recognize_sphinx(audio)
            response["transcription"] = temp
        elif recognizerMode == "Whisper":
            ####Currently not supported: will have a permission denied error
            temp = recognizer.recognize_whisper(audio)
            response["transcription"] = temp
        elif recognizerMode == "Tensorflow":
            ####Currently not supported: cannot detect anything
            temp = recognizer.recognize_tensorflow(audio, 'C:/Users/RuichenHe/source/Python/PyVoice/tensorflow-data/conv_actions_frozen.pb', 'C:/Users/RuichenHe/source/Python/PyVoice/tensorflow-data/conv_actions_labels.txt')
            response["transcription"] = temp
        elif recognizerMode == "Google":
            ####Currently not supported: cannot detect anything
            temp = recognizer.recognize_google(audio)
            response["transcription"] = temp
    #Handle potential errors
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
    recognizerMode = "Google"
    print("Voice Detection API Start...")
    #Initlized model here
    #For VOSK:
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
        #Different operations based on the voice command
        if speakContent["transcription"] == "what is the time now" or speakContent["transcription"] == "what time is it":
            print("Current time: " + time.strftime("%H:%M:%S", time.localtime()))
        elif speakContent["transcription"] == "what is the date today":
            print("Current date: " + str(date.today()))
        elif speakContent["transcription"] == "detection terminate":
            keepDetection = False
    print("Voice Detection API terminated.")