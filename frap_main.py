"""

created on: 2021-11-08
author:     michal horansky
----------------------------
main file for the FRAP project
a sample use of the library, to be modified, copied, or changed
----------------------------
This software is distributed under the GNU General Public License (GPL-3.0-or-later).
It may be used, modified, shared, or built upon.
All derivative work must be distributed under the same license.

"""

import pydub.playback as pdplayback

from lsg import *
from master import *
from soundfont import *
from waveform import *

from frap_functions import *

abba_lsg = lsg({'a' : 'ab', 'b' : 'a', 'ab' : 'ba'})
kanye_lsg = lsg({'a' : 'ba', 'b' : 'ca', 'c' : 'b'})
jaco_lsg = lsg({'a' : 'cab', 'c' : 'db', 'b' : 'a', 'd' : 'ac'})
print(len(jaco_lsg.iterate(7, 'a')))
print(len(abba_lsg.iterate(21, 'a')))

main_master = master()

main_master.add_lsg("abba" , abba_lsg )
main_master.add_lsg("kanye", kanye_lsg)
main_master.add_lsg("jaco", jaco_lsg)
#main_master.add_soundfont("drumfont", samplefont(['snicker', 'snack'], [3, 2]))

main_master.add_soundfont("snickersnack", samplefont(["trap_kickdrum", "trap_snare"], [4, 4]))
main_master.add_soundfont("scoopitypoop", samplefont([espeak_sample("poopity"), espeak_sample("scoopity"), espeak_sample("poop")], [4, 4, 2]))
#main_master.add_soundfont("scoopitypoop", samplefont(["trap_kickdrum", "trap_snare", "trap_break"], [2, 2, 2]))


main_master.soundfonts['snickersnack'].set_symbol_map({'a' : 'trap_kickdrum', 'b' : 'trap_snare'})
main_master.soundfonts['snickersnack'].trim_samples(200)
main_master.soundfonts['snickersnack'].normalize_samples()

main_master.soundfonts['scoopitypoop'].set_symbol_map({'a' : 'poopity', 'b' : 'scoopity', 'c' : 'poop'})
main_master.soundfonts['scoopitypoop'].trim_samples(200)
main_master.soundfonts['scoopitypoop'].normalize_samples(main_master.soundfonts['snickersnack'].time_per_beat)

bass_waveform = waveform([[1.0, 'sine', 0], [3.0/2.0, 'triangle', -10]], [10, 150])
main_master.add_soundfont("bass_font", pitchfont(bass_waveform, main_master.soundfonts['snickersnack'].time_per_beat))

main_master.soundfonts['bass_font'].set_symbol_map({'a' : [200.0, 4], 'b' : [200.0 * hs * hs * hs, 2, -5], 'c' : [200.0 * hs * hs * hs * hs * hs, 4, -5], 'd' : [200.0 * hs * hs * hs * hs * hs * hs, 2, -5]})

main_master.generate_track('jaco'       , 'bass_font'   , 'jaco' , 7 , 'a')
main_master.generate_track('jabberwocky', 'snickersnack', 'abba' , 21, 'a')
main_master.generate_track('donda'      , 'scoopitypoop', 'kanye', 10, 'a')

min_length = len(main_master.tracks['jaco'])
main_master.set_mix_length(min_length)
main_master.track_sine_pan('jaco', 1500, 0.9, int(min_length / 3), int(min_length * 2 / 3))
main_master.mix_fade_in(1500)
main_master.mix_fade_out(5000)

main_master.export_mix("NANDa")
main_master.play_mix()


