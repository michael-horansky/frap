"""

created on: 2021-11-08
author:     michal horansky
----------------------------
classfile for the FRAP project
waveform: class to synthesize audio segments with arbitrary pitch
----------------------------
This software is distributed under the GNU General Public License (GPL-3.0-or-later).
It may be used, modified, shared, or built upon.
All derivative work must be distributed under the same license.

"""

import pydub
import pydub.generators as pdsynth



class waveform():
    
    # constructors and destructors
    def __init__(self, init_spectrum=[], init_fade_shape=[0, 0]):
        self.spectrum = init_spectrum.copy()
        self.fade_shape = init_fade_shape.copy()
        # spectrum = [[frequency coeff, shape, relative gain in db], ...]
        # shape = ['sine', 'square', 'sawtooth', 'triangle'], default is 'sine'
    
    def get_spectrum(self):
        return(self.spectrum.copy())
    def set_spectrum(self, new_spectrum):
        self.spectrum = new_spectrum.copy()
        return(self)
    def add_overtone(self, append_spectrum):
        self.spectrum.extend(append_spectrum)
        return(self)
    def delete_overtone(self, obsolete_frequency):
        for i in range(len(self.spectrum)):
            if self.spectrum[i][0] == obsolete_frequency:
                self.spectrum.pop(i)
        return(self)
    
    def set_fade_shape(self, new_fade_shape):
        self.fade_shape = new_fade_shape.copy()
        return(self)
    
    def synthesize(self, base_frequency, base_duration, base_gain):
        result = pydub.AudioSegment.silent(duration=base_duration)
        for overtone in self.spectrum:
            if len(overtone) == 2:
                cur_freq  = base_frequency * overtone[0]
                cur_shape = 'sine'
                cur_gain  = overtone[1] + base_gain
            else:
                cur_freq  = base_frequency * overtone[0]
                cur_shape = overtone[1]
                cur_gain  = overtone[2] + base_gain
            if cur_shape == 'sine':
                cur_gen = pdsynth.Sine(cur_freq)
            elif cur_shape == 'square':
                cur_gen = pdsynth.Square(cur_freq)
            elif cur_shape == 'sawtooth':
                cur_gen = pdsynth.Sawtooth(cur_freq)
            elif cur_shape == 'triangle':
                cur_gen = pdsynth.Triangle(cur_freq)
            cur_tone = cur_gen.to_audio_segment(duration = base_duration).apply_gain(cur_gain)
            cur_tone = cur_tone.fade_in(self.fade_shape[0]).fade_out(self.fade_shape[1])
            result = result.overlay(cur_tone)
        return(result)
    
