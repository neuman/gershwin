from sebastian.lilypond.interp import parse
from sebastian.midi import write_midi, player
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.core.transforms import transform_sequence, transpose, reverse, add, degree_in_key, midi_pitch
from sebastian.core.notes import Key, major_scale
import sebastian.core.transforms as transforms
from core.composition import OFFSET_64
import random

@transform_sequence
def delay(interval, point):
    """
    Transpose a point by an interval, using the Sebastian interval system
    """
    if "offset" in point:
        point["offset"] = point["offset"] + interval
    if OFFSET_64 in point:
        point[OFFSET_64] = point[OFFSET_64] + interval
    return point

@transform_sequence
def mutate(octave, pitch, velocity, duration, offset, point):
	#def mutate(seq, pitch=0, duration=0, velocity=0, offset=0, octave=0):
    """
    Transpose a point by an interval, using the Sebastian interval system
    """
    octave_delta = random.randint(-1*octave,octave)
    rna = {
    'midi_pitch':pitch, 
    'pitch':pitch, 
    'octave':octave,
    'velocity':velocity, 
    DURATION_64:duration, 
    OFFSET_64:offset
    }
    new_point = Point()
    for key in rna:
        if key in point:
            if key == "octave":
                new_value = random.randint(point[key]-rna[key],point[key]+rna[key])+octave_delta
            else:
                new_value = random.randint(point[key]-rna[key],point[key]+rna[key])
            new_point.__setitem__(key, new_value)

    return new_point