#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
import os
import torch
import speech_recognition # для работы требуется установить pyaudio
from playsound import playsound #pip install playsound==1.2.2
from IPython.display import Audio
from googletrans import Translator # pip install googletrans==3.1.0a0

class Voice:
    def __init__(self):
        if not os.path.isdir("TTS results"):
            os.mkdir("TTS results")
            print("Was created folder TTS results")

        for file in os.listdir("./TTS results/"):
            if file.endswith(".wav"):
                os.remove(f"TTS results/{file}")

    answer_number = 0
    resultSTT = ""
    resultGPT = ""

    recognizer = speech_recognition.Recognizer()
    translator = Translator(service_urls=['translate.googleapis.com'])

    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                        model='silero_tts',
                                        language= 'ru',
                                        speaker= 'v3_1_ru')
    model.to(torch.device('cpu'))

    def textToSpeech(self, text):
        print("Ответ на фразу: " + text)

        audio = self.model.apply_tts(text=text,
                            speaker= 'xenia',
                            sample_rate= 48000,
                            put_accent= True,
                            put_yo= True)

        with open(f'TTS results/voiceAnswer{self.answer_number}.wav', 'wb') as file:
            file.write(Audio(audio, rate= 48000).data)

        playsound(f'TTS results/voiceAnswer{self.answer_number}.wav')
        self.answer_number += 1
        print(f"Озвучен results/voiceAnswer{self.answer_number}")

    def speechToText(self, deviceIndex: int = 1):
        while True:
                print("button is pressed")
                try:
                    with speech_recognition.Microphone(device_index = deviceIndex) as sourse:
                        audio = self.recognizer.listen(sourse)
                except:
                    print("Ошибка инициализации микрофона")
                try:
                    self.resultSTT = self.recognizer.recognize_google(audio, language = "ru-RU").lower()
                except:
                    print("Ошибка распознования аудио")
                
                print("Распознаная фраза: " + self.resultSTT)
                return self.resultSTT