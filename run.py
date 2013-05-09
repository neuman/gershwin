from sebastian.lilypond.interp import parse
from sebastian.lilypond.write_lilypond import write
from sebastian.midi import write_midi, player
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.core.transforms import stretch, transpose, reverse, add, degree_in_key, midi_pitch, lilypond
from sebastian.core.notes import Key, major_scale
import random
import gershwin.core as gershwin
from gershwin import songs, transforms
from gershwin.core import composition
kb = composition.Keyboard()

d = songs.Omatic()
d.next()
finger1 = d.hand[0]
finger1.last.display()
