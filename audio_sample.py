"""

created on: 2021-11-08
author:     michal horansky
----------------------------
classfile for the FRAP project
audio_sample: single-sample class
----------------------------
This software is distributed under the GNU General Public License (GPL-3.0-or-later).
It may be used, modified, shared, or built upon.
All derivative work must be distributed under the same license.

"""

import pydub



class audio_sample():
    path_prefix = 'data/samples/'
    # constructors and destructors
    def __init__(self, filename, my_trim=0, my_beat_length = 1):
        
        # my_trim is in milliseconds
        # filename can be an actual filename or a list of form [name, AudioSegment]
        if type(filename) == str:
            self.name = filename
            full_audio = pydub.AudioSegment.from_wav(audio_sample.path_prefix + filename + ".wav")
        else:
            self.name = filename[0]
            full_audio = filename[1]
        self.audio = full_audio[:len(full_audio) - my_trim]
        self.beat_length = my_beat_length
    
    def trim_sample(self, trim_amount):
        self.audio = self.audio[:len(self.audio) - trim_amount]
        return(self)
    
    def stretch_sample(self, stretch_amount, aggressive = False):
        if stretch_amount == 0:
            return(self)
        if stretch_amount < 0:
            if aggressive:
                return(self.trim_sample(-stretch_amount))
            return(self)
        self.audio = self.audio + pydub.AudioSegment.silent(duration=stretch_amount)
        return(self)

