from sebastian.lilypond.interp import parse
#from sebastian.lilypond.write_lilypond import write
from sebastian.midi import write_midi, player
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.core.transforms import stretch, transpose, reverse, add, degree_in_key, midi_pitch, midi_to_pitch, delay #, lilypond
from sebastian.core.notes import Key, major_scale
from sebastian.core import OSequence, HSeq, Point, DURATION_64
import random
import metatracks, transforms
from core.composition import *
from core.transforms import *
d = metatracks.JazzBot()
#finger1 = d.hand[0]
d.next()
#finger1.last

