import speech_recognition as sr
import matplotlib.pyplot as plt
import numpy as np

from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "ENG_F.wav")
AUDIO_FILE_fr = path.join(path.dirname(path.realpath(__file__)), "f_m3.wav")


def histogram(data, n_bins, cumulative=False, x_label="", y_label="", title=""):
    fig = plt.figure()
    s = fig.add_subplot(111)
    amplitude = np.fromstring(data, np.int16)
    s.plot(amplitude)
    fig.savefig('plot.png')


r = sr.Recognizer()
print("Speak now!")

with sr.Microphone() as source:
    audio = r.listen(source)
# write audio to a RAW file
with open("microphone-results.raw", "wb") as f:
    raw_data = audio.get_raw_data()
    f.write(raw_data)
    histogram(raw_data, 2, False, "Frequency", "Hz", "sound")

with sr.AudioFile(AUDIO_FILE) as source:
    audio_en = r.record(source)  # read the entire audio file

with sr.AudioFile(AUDIO_FILE_fr) as source:
    audio_fr = r.record(source)  # read the entire audio file

try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said in eng" + r.recognize_google(audio_en))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

try:
    print("Google Speech Recognition thinks you said in fr " + r.recognize_google(audio_fr, language='fr-FR'))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# write audio to a WAV file
with open("microphone-results.wav", "wb") as f:
    f.write(audio.get_wav_data())

try:
    text = r.recognize_google(audio)
    print("You said: {}".format(text))
except sr.UnknownValueError:
    print("Cannot recognize what you said")