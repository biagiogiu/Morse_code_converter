import json
import pyaudio
from math import pi
import numpy as np

FREQUENCY = 500
POINT_LENGTH = 0.07
RATE = 44100

with open("morse_code.json", "r") as file:
    morse_dict = json.load(file)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)


class MorseConverter:
    def __init__(self):
        self.text = ""
        self.morse_text = []
        self.morse_audio = []

    def text_to_morse_code(self):
        for char in self.text.upper():
            self.morse_text.append(morse_dict.get(char))
        print(self.morse_text)

    def text_to_morse(self, text):
        self.text = text
        self.text_to_morse_code()
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)

        for letter in self.morse_text:
            morse_letter = []
            for sign in letter:
                if sign == '.':
                    morse_letter.append(self.make_sound())
                    morse_letter.append(self.make_sound(frequency=0))
                elif sign == "-":
                    line_length = POINT_LENGTH * 3
                    morse_letter.append(self.make_sound(length=line_length))
                    morse_letter.append(self.make_sound(frequency=0))
                elif sign == "/":
                    pause_between_signs = POINT_LENGTH * 3
                    morse_letter.append(self.make_sound(frequency=0, length=pause_between_signs))
            self.morse_audio.append(morse_letter)
            pause_between_words = POINT_LENGTH * 7
            self.morse_audio.append(self.make_sound(frequency=0, length=pause_between_words))

        for morse_letter in self.morse_audio:
            for sound in morse_letter:
                stream.write(sound.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()

    def make_sound(self, frequency=FREQUENCY, length=POINT_LENGTH, sample_rate=44100):
        length = int(length * sample_rate)
        factor = float(frequency) * (pi * 2) / sample_rate
        waveform = np.sin(np.arange(length) * factor)
        return waveform
