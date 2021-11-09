"""

created on: 2021-11-08
author:     michal horansky
----------------------------
classfile for the FRAP project
master: to contain, handle, process and mix all audiotracks
----------------------------
This software is distributed under the GNU General Public License (GPL-3.0-or-later).
It may be used, modified, shared, or built upon.
All derivative work must be distributed under the same license.

"""

import pydub

from audio_sample import *
from waveform import *


class soundfont():
    
    # constructors and destructors
    def __init__(self):
        self.symbol_map = {}
        self.normalize_beats = True
        self.time_per_beat = 0
    
    # methods
    def get_symbol_map(self):
        return(self.symbol_map.copy())
    def set_symbol_map(self, new_symbol_map):
        self.symbol_map = new_symbol_map.copy()
        return(self)
    def add_symbols(self, append_symbol_map):
        for s_0, s_1 in append_symbol_map.items():
            # if rule already exists, it will merely be updated
            self.symbol_map[s_0] = s_1
        return(self)
    def delete_symbol(self, obsolete_key):
        self.symbol_map.pop(obsolete_key, None)
        return(self)
    
    
    
    def sf_play(self, lstring):
        return(pydub.AudioSegment.silent(duration=0))


class samplefont(soundfont):
    
    # constructors and destructors
    def __init__(self, sample_names=[], sample_beat_lengths = []):
        soundfont.__init__(self)
        self.samples = {}
        if len(sample_beat_lengths) == 0:
            self.normalize_beats = False
        else:
            self.normalize_beats = True
        for i in range(len(sample_names)):
            sample_filename = sample_names[i]
            if type(sample_filename) == str:
                sample_name = sample_filename
            else:
                sample_name = sample_filename[0]
            cur_beat_length = 1
            if self.normalize_beats > 0:
                cur_beat_length = sample_beat_lengths[i]
            self.samples[sample_name] = audio_sample(sample_filename, 0, cur_beat_length)#pydub.AudioSegment.from_wav("data/samples/" + sample_filename + ".wav")
    
    def add_sample(self, sample_name, sample_beat_length = 1):
        self.samples[sample_name] = audio_sample(sample_name, 0, sample_beat_length)#pydub.AudioSegment.from_wav("data/samples/" + sample_name + ".wav")
    def trim_samples(self, trim_amount):
        for name, sample in self.samples.items():
            sample.trim_sample(trim_amount)
        return(self)
    
    def normalize_samples(self, demanded_time_per_beat = -1):
        
        if demanded_time_per_beat == -1:
            # find the sample with the longest time per beat, then add corresponding amount of silence to all others
            max_time_per_beat = 0
            for name, sample in self.samples.items():
                cur_time_per_beat = int(len(sample.audio) / sample.beat_length)
                if cur_time_per_beat > max_time_per_beat:
                    max_time_per_beat = cur_time_per_beat
            self.time_per_beat = max_time_per_beat
            for name, sample in self.samples.items():
                target_time = sample.beat_length * self.time_per_beat
                sample.stretch_sample(target_time - len(sample.audio))
        else:
            # aggressively trim and stretch all samples so that the beat lengths are aligned with the demanded time per beat
            self.time_per_beat = demanded_time_per_beat
            for name, sample in self.samples.items():
                target_time = sample.beat_length * self.time_per_beat
                sample.stretch_sample(target_time - len(sample.audio), aggressive=True)
    
    def sf_play(self, lstring):
        result = pydub.AudioSegment.silent(duration=0)
        for char in lstring:
            if char in self.symbol_map.keys():
                result += self.samples[self.symbol_map[char]].audio
        return(result)


class pitchfont(soundfont):
    
    # constructors and destructors
    def __init__(self, init_waveform, init_time_per_beat):
        # symbol map here is { rule : [pitch, beat length, gain=0] }
        soundfont.__init__(self)
        self.my_waveform = init_waveform
        self.time_per_beat = init_time_per_beat
    
    def sf_play(self, lstring):
        result = pydub.AudioSegment.silent(duration=0)
        for char in lstring:
            if char in self.symbol_map.keys():
                if len(self.symbol_map[char]) == 2:
                    cur_pitch = self.symbol_map[char][0]
                    cur_beat_length = self.symbol_map[char][1]
                    cur_gain = 0
                else:
                    cur_pitch = self.symbol_map[char][0]
                    cur_beat_length = self.symbol_map[char][1]
                    cur_gain = self.symbol_map[char][2]
                result += self.my_waveform.synthesize(cur_pitch, cur_beat_length * self.time_per_beat, cur_gain)
        return(result)



