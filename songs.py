from sebastian.lilypond.interp import parse
from sebastian.midi import write_midi, player
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.core.transforms import transpose, reverse, add, degree_in_key, midi_pitch
from sebastian.core.notes import Key, major_scale
import random

from gershwin.core import composition as gershwin
import sebastian.core.transforms as transforms

class Dramatic(object):
        def __init__(self):
                self.hand = []

        def next(self):
                keys = gershwin.MinorBluesKeyboard().notes
                self.keys = keys
                stretch_length = random.randint(2,5)
                left_low = random.randint(40,70)
                left_range = random.randint(1,2)
                left = HSeq(list(keys).__getslice__(left_low,left_low+left_range))
                right = HSeq(list(keys).__getslice__(20,50))

                note1 = gershwin.Wandering(keys)
                duration1 = gershwin.Oscilating(range(2,8))
                velocity1 = gershwin.Randomized(range(20,127))

                note2 = gershwin.Wandering(left)
                duration2 = gershwin.Randomized(range(0,len(left)))
                velocity2 = gershwin.Wandering(range(70,90))

                note3 = note2.echo()
                duration3 = gershwin.Randomized(range(2,12))
                velocity3 = gershwin.Wandering(range(20,127))

                finger1 = gershwin.Finger(
                length = 16,
                note = note1,
                duration = duration1,
                velocity = velocity1
                )

                finger2 = gershwin.Finger(
                        length = 160,
                        note = note2,
                        duration = duration2,
                        velocity = velocity2
                        )

                finger3 = gershwin.Finger(
                        length = 16,
                        note = note2,
                        duration = duration3,
                        velocity = velocity3
                        )

                finger4 = gershwin.Finger(
                        length = 16,
                        note = gershwin.Wandering([1,2,3]),
                        duration = gershwin.Randomized([4,6]),
                        velocity = gershwin.Wandering(range(40,50))
                        )
                x=500
                
                drone = (finger1.next(5) | transforms.stretch(1))*3
                solo1 = finger1.next(x)
                #solo2 = gershwin.humanize(finger1.last,1,1,1,1)
                solo2 = finger1.next(x)
                output = drone+(solo1//solo2//(drone*10)//finger3.next(x) | transforms.stretch(4))+(drone*3)
                self.hand = [finger1,finger2,finger3,finger4]
                self.last = output
                try:
                        player.play([output])
                except Exception as e:
                        print e


        def last(self):
                return self.last

class Loopy(object):
        def __init__(self):
                self.hand = []
                
        def next(self):
                keys = gershwin.PentatonicKeyboard().notes
                stretch_length = random.randint(2,5)
                left_low = random.randint(40,70)
                left_range = random.randint(1,2)
                left = HSeq(list(keys).__getslice__(left_low,left_low+left_range))
                right = HSeq(list(keys).__getslice__(20,50))

                note1 = gershwin.Wandering(keys)
                duration1 = gershwin.Wandering(range(2,8))
                velocity1 = gershwin.Randomized(range(20,127))

                note2 = gershwin.Wandering(left)
                duration2 = gershwin.Randomized(range(0,len(left)))
                velocity2 = gershwin.Wandering(range(70,90))

                note3 = note2.echo()
                duration3 = gershwin.Randomized(range(2,12))
                velocity3 = gershwin.Wandering(range(20,127))

                finger1 = gershwin.Finger(
                length = 1160,
                note = note1,
                duration = duration1,
                velocity = velocity1
                )
                self.hand = [finger1]
                x = 160
                player.play([gershwin.loop([finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x)])])
                try:
                        player.play([output])
                except Exception as e:
                        print e

        def last(self):
                return self.last



