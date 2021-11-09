"""

created on: 2021-11-08
author:     michal horansky
----------------------------
supplementary module for the FRAP project
general functions to be used by all files
----------------------------
This software is distributed under the GNU General Public License (GPL-3.0-or-later).
It may be used, modified, shared, or built upon.
All derivative work must be distributed under the same license.

"""

import gtts
import pyttsx3
import pydub
import pydub.playback as pdplayback
import io
import os
import numpy as np

# ---------------- USEFUL CONSTANTS ------------

#halfstep
hs = np.power(2.0, 1.0/12.0)


#from playsound import playsound

def max_property(my_list, func = len):
    my_max_property = 0
    for element in my_list:
        cur_val = func(element)
        if cur_val > my_max_property:
            my_max_property = cur_val
    return(my_max_property)

# ---------- AUDIO FUNCTIONS -------------

def sine_panning(my_audio, period, amplitude = 1.0, start_duration = 0, end_duration = -1):
    if end_duration == -1:
        end_duration = len(my_audio)
    audio_before = my_audio[:start_duration]
    audio_to_pan = my_audio[start_duration:end_duration]
    audio_after  = my_audio[end_duration:]
    
    step_size = int(period / 50) # 50 steps during one period
    for timestamp in range(0, end_duration - start_duration, step_size):
        maxbit = timestamp + step_size
        if maxbit > len(audio_to_pan):
            maxbit = len(audio_to_pan)
        audio_bit = audio_to_pan[timestamp : maxbit]
        audio_before += audio_bit.pan(amplitude * np.sin(2.0 * np.pi * (float(timestamp) / float(period))))
    return(audio_before + audio_after)


# ---------- TEXT TO SPEECH --------------

def gtts_sample(text):
    tts_audio = gtts.gTTS(text)
    #print(tts_audio)
    mp3_fp = io.BytesIO()
    #wav_fp = io.BytesIO()
    tts_audio.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    mp3_as = pydub.AudioSegment.from_mp3(mp3_fp)
    return(mp3_as)
    #mp3_as.export(wav_fp, format="wav")
    #wav_as = pydub.AudioSegment.from_wav(wav_fp)
    #pdplayback.play(wav_as)

my_engine = pyttsx3.init()

def espeak_sample(text, name = "__UNDEFINED__"):
    if name == "__UNDEFINED__":
        name = text
    filepath = "data/samples/" + name + ".wav"
    if not os.path.exists(filepath):
        my_engine.save_to_file(text, filepath)
        my_engine.runAndWait()
        while(my_engine.isBusy()):
            pass
    #my_engine.say(text)
    #wav_fp = io.BytesIO()
    #wav_fp.seek(0)
    audio_output = pydub.AudioSegment.from_wav(filepath)
    #os.remove("data/samples/__TEMPORARY_SAMPLE_FILE__.wav")
    return([name, audio_output])
