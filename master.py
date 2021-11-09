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
import pydub.playback as pdplayback


from lsg import *
from soundfont import *
from frap_functions import *

def set_to_target_level(sound, target_level):
    difference = target_level - sound.dBFS
    return sound.apply_gain(difference)

class master():
    
    # initializers and destructors
    def __init__(self):
        self.tracks     = {}
        self.lsgs       = {}
        self.soundfonts = {}
    
    # methods
    def add_lsg(self, lsg_name, new_lsg):
        # if name already exists, it will be overwritten
        self.lsgs[lsg_name] = new_lsg
        return(self)
    def delete_lsg(self, obsolete_name):
        self.lsgs.pop(obsolete_key, None)
        return(self)
    def add_soundfont(self, soundfont_name, new_soundfont):
        # if name already exists, it will be overwritten
        self.soundfonts[soundfont_name] = new_soundfont
        return(self)
    def delete_soundfont(self, obsolete_name):
        self.soundfonts.pop(obsolete_key, None)
        return(self)
    
    def generate_track(self, track_name, soundfont_name, lsg_name, lsg_depth, lsg_axiom="__UNDEFINED__"):
        lstring = self.lsgs[lsg_name].iterate(lsg_depth, lsg_axiom)
        #new_track = pydub.AudioSegment.silent(duration=0)
        
        self.tracks[track_name] = self.soundfonts[soundfont_name].sf_play(lstring) #new_track
    
    def trim_track(self, track_name, trim_amount):
        if trim_amount > 0:
            self.tracks[track_name] = self.tracks[track_name][:len(self.tracks[track_name]) - trim_amount]
        return(self)
    def set_track_length(self, track_name, target_length):
        if len(self.tracks[track_name]) > target_length:
            self.tracks[track_name] = self.tracks[track_name][:target_length]
        return(self)
    def set_mix_length(self, mix_length):
        for my_track_name, my_track in self.tracks.items():
            self.set_track_length(my_track_name, mix_length)
        return(self)
    def track_fade_in(self, track_name, fade_in_duration):
        self.tracks[track_name] = self.tracks[track_name].fade_in(fade_in_duration)
        return(self)
    def track_fade_out(self, track_name, fade_out_duration):
        self.tracks[track_name] = self.tracks[track_name].fade_out(fade_out_duration)
        return(self)
    def track_sine_pan(self, track_name, period, amplitude = 1.0, start_duration = 0, end_duration = -1):
        self.tracks[track_name] = sine_panning(self.tracks[track_name], period, amplitude, start_duration, end_duration)
    def mix_fade_in(self, fade_in_duration):
        for my_track_name, my_track in self.tracks.items():
            self.track_fade_in(my_track_name, fade_in_duration)
        return(self)
    def mix_fade_out(self, fade_out_duration):
        for my_track_name, my_track in self.tracks.items():
            self.track_fade_out(my_track_name, fade_out_duration)
        return(self)
    
    def mix_audio(self, target_level = -12):
        # find the longest track and center everything around it
        max_length = 0
        longest_track_name = "_none"
        for name, track in self.tracks.items():
            if len(track) > max_length:
                max_length = len(track)
                longest_track_name = name
        final_mix = self.tracks[longest_track_name]
        for name, track in self.tracks.items():
            if name == longest_track_name:
                continue
            final_mix = final_mix.overlay(track) #TODO:add equalization here
        return(set_to_target_level(final_mix, target_level))
    
    def export_mix(self, filename):
        my_mix = self.mix_audio()
        my_mix.export("outputs/" + filename + ".wav", format='wav')
    
    def play_mix(self):
        pdplayback.play(self.mix_audio())
        
    





