import time

import speech_recognition as sr

def RecognizeSpeechFromMic(recognizer, microphone):
    
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
        response["transcription"] = recognizer.recognize_vosk(audio)
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
    print("Voice Detection API Start...")
    time.sleep(3)

    while True:
        speakContent = RecognizeSpeechFromMic(recognizer, microphone)
        print("You said: {}".format(speakContent["transcription"]))