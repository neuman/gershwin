from sebastian.lilypond.interp import parse
from sebastian.midi import write_midi, player
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.core.transforms import transform_sequence, transpose, reverse, add, degree_in_key, midi_pitch
from sebastian.core.notes import Key, major_scale
import sebastian.core.transforms as transforms
from core.composition import OFFSET_64

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