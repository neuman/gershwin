from sebastian.lilypond.interp import parse
#from sebastian.lilypond.write_lilypond import write
from sebastian.midi import write_midi, player
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.core.transforms import stretch, transpose, reverse, add, degree_in_key, midi_pitch, midi_to_pitch, delay #, lilypond
from sebastian.core.notes import Key, major_scale
from sebastian.core import OSequence, HSeq, Point, DURATION_64
import random
import core as gershwin
import metatracks, transforms
from core import composition
kb = composition.Keyboard()
kb.play()

#d = metatracks.Redux()
#finger1 = d.hand[0]
#d.next([3,1,0,0,0])
#finger1.last


{'octave': 1, 'pitch': 1, 'velocity': 90, 'midi_pitch': 21, 'offset_64': 0, 'duration_64': 10}, 
{'octave': 1, 'pitch': 2, 'velocity': 90, 'midi_pitch': 16, 'offset_64': 10, 'duration_64': 10}, 
{'octave': 1, 'pitch': 3, 'velocity': 90, 'midi_pitch': 23, 'offset_64': 20, 'duration_64': 10}, 
{'octave': 1, 'pitch': 4, 'velocity': 90, 'midi_pitch': 18, 'offset_64': 30, 'duration_64': 10}, 
{'octave': 1, 'pitch': 5, 'velocity': 90, 'midi_pitch': 13, 'offset_64': 40, 'duration_64': 10}, 
{'octave': 1, 'pitch': 6, 'velocity': 90, 'midi_pitch': 20, 'offset_64': 50, 'duration_64': 10}, 
{'octave': 1, 'pitch': 7, 'velocity': 90, 'midi_pitch': 15, 'offset_64': 60, 'duration_64': 10}, 
{'octave': 1, 'pitch': 8, 'velocity': 90, 'midi_pitch': 22, 'offset_64': 70, 'duration_64': 10}, 
{'octave': 1, 'pitch': 9, 'velocity': 90, 'midi_pitch': 17, 'offset_64': 80, 'duration_64': 10}, 
{'octave': 1, 'pitch': 10, 'velocity': 90, 'midi_pitch': 24, 'offset_64': 90, 'duration_64': 10}, 
{'octave': 1, 'pitch': 11, 'velocity': 90, 'midi_pitch': 19, 'offset_64': 100, 'duration_64': 10}
