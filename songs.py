from sebastian.lilypond.interp import parse
from sebastian.midi import write_midi, player
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.core.transforms import transpose, reverse, add, degree_in_key, midi_pitch
from sebastian.core.notes import Key, major_scale
import random

from gershwin.core import composition as gershwin
from gershwin.transforms import delay
import sebastian.core.transforms as transforms

class Dramatic(object):
        def __init__(self):
                self.hand = []

        def next(self):
                keys = gershwin.Keyboard().notes
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
                x=800
                
                drone = (finger1.next(50) | transforms.stretch(1))*3
                solo1 = finger1.next(x)
                #solo2 = gershwin.humanize(finger1.last,1,1,1,1)
                solo2 = finger1.next(x)
                output = drone+(solo1//solo2//(drone*10)//finger3.next(x) | transforms.stretch(5))+(drone*3)
                self.hand = [finger1,finger2,finger3,finger4]
                self.last = output
                try:
                        player.play([output | midi_pitch()])
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
                #player.play([gershwin.loop([finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x)])])
                try:
                        player.play([output])
                except Exception as e:
                        print e

        def last(self):
                return self.last



class Omatic(object):
        def __init__(self):
                self.hand = []
        '''
        keyboards = [gershwin.Keyboard(), gershwin.MinorBluesKeyboard(), gershwin.EvenKeyboard(), gershwin.OddKeyboard(), gershwin.PentatonicKeyboard()]
        pickers = [
        gershwin.Randomized(),
        gershwin.Wandering(), 
        gershwin.Oscilating(), 
        gershwin.Ascending(), 
        gershwin.Constant()
        ]
        '''

        def next(self):
                keys = gershwin.PentatonicKeyboard().notes
                self.keys = list(keys)
                keycount = len(self.keys)
                stretch_length = random.randint(2,5)
                left_low = random.randint(keycount/4,(keycount/2))
                left_range = random.randint(1,2)
                mids = HSeq(self.keys.__getslice__(left_low,left_low+left_range))
                right = HSeq(self.keys.__getslice__(keycount-(keycount/4), keycount-1))

                finger1 = gershwin.Finger(
                length = 16,
                note = gershwin.Wandering(mids),
                duration = gershwin.Oscilating(range(2,8)),
                velocity = gershwin.Randomized(range(20,127)),
                rest = gershwin.Randomized([10,20,40])
                )

                finger2 = gershwin.Finger(
                        length = 160,
                        note = gershwin.Wandering(right),
                        duration = gershwin.Randomized(range(2,80)),
                        velocity = gershwin.Wandering(range(50,90)),
                        rest = gershwin.Randomized([1,2,3,4,5])
                        )

                finger3 = gershwin.Finger(
                length = 16,
                note = gershwin.Wandering(mids),
                duration = gershwin.Oscilating(range(2,8)),
                velocity = gershwin.Randomized(range(20,127)),
                rest = gershwin.Randomized([10,20,40])
                )


                x=800
                
                drone = (finger1.next(90) | transforms.stretch(1))*2
                #drone = gershwin.multiply(drone,[-3])
                measure = drone.next_offset()-1
                #metrenome 
                alpha = (drone*2)+(gershwin.humanize(drone,1,2,1,2,0))+(drone*2)+(gershwin.humanize(drone,1,2,1,0,1))+(drone*2)+(gershwin.humanize(drone,1,2,1,0,1))+(drone*2)
                drone2 = (finger1.next(90) | transforms.stretch(1))*2
                humanized_drone2 = (gershwin.humanize(drone2,1,2,1,0,1))
                beta = (drone*2)+(humanized_drone2)+(drone2*2)+(humanized_drone2)+(drone2*2)+(humanized_drone2)+(drone2*2)
                solo1 = finger2.next(measure)+(gershwin.humanize(finger2.next(measure),octave=1) | delay(measure))+(finger2.next(measure) | delay(measure))
                output = alpha//(beta | delay(measure*2))
                self.hand = [finger1,finger2]
                self.last = output | transforms.stretch(1)
                try:
                        player.play([self.last | midi_pitch()])
                except Exception as e:
                        print e


        def last(self):
                return self.last



class BenSong(object):
        def __init__(self):
                self.hand = []
        '''
        keyboards = [gershwin.Keyboard(), gershwin.MinorBluesKeyboard(), gershwin.EvenKeyboard(), gershwin.OddKeyboard(), gershwin.PentatonicKeyboard()]
        pickers = [
        gershwin.Randomized(),
        gershwin.Wandering(), 
        gershwin.Oscilating(), 
        gershwin.Ascending(), 
        gershwin.Constant()
        ]
        '''

        def next(self):
                keys = gershwin.MinorBluesKeyboard().notes
                self.keys = list(keys)
                keycount = len(self.keys)
                stretch_length = random.randint(2,5)
                left_low = random.randint(keycount/4,(keycount/2))
                left_range = random.randint(1,2)
                mids = HSeq(self.keys.__getslice__(left_low,left_low+left_range))
                right = HSeq(self.keys.__getslice__(keycount-(keycount/4), keycount-1))

                finger1 = gershwin.Finger(
                length = 16,
                note = gershwin.Wandering(mids),
                duration = gershwin.Oscilating([16, 32]),
                velocity = gershwin.Randomized(range(20,127)),
                rest = gershwin.Randomized([16, 32])
                )

                finger2 = gershwin.Finger(
                        length = 160,
                        note = gershwin.Wandering(right),
                        duration = gershwin.Randomized([8,16,24,32]),
                        velocity = gershwin.Wandering(range(50,90)),
                        rest = gershwin.Randomized([8,16,24,32])
                        )

                finger3 = gershwin.Finger(
                length = 16,
                note = gershwin.Wandering(mids),
                duration = gershwin.Oscilating(range(2,8)),
                velocity = gershwin.Randomized(range(20,127)),
                rest = gershwin.Randomized([10,20,40])
                )


                x=800
                
                drone = (finger1.next(80))*2
                #drone = gershwin.multiply(drone,[-3])
                measure = drone.next_offset()-1
                #metrenome 
                alpha = (drone*2)+(gershwin.humanize(drone,1,2,1,2,0))+(drone*2)+(gershwin.humanize(drone,1,2,1,0,1))+(drone*2)+(gershwin.humanize(drone,1,2,1,0,1))+(drone*2)
                drone2 = (finger1.next(90) | transforms.stretch(1))*2
                humanized_drone2 = (gershwin.humanize(drone2,1,2,1,0,1))
                beta = (drone*2)+(humanized_drone2)+(drone2*2)+(humanized_drone2)+(drone2*2)+(humanized_drone2)+(drone2*2)
                solo1 = finger2.next(measure)+(gershwin.humanize(finger2.next(measure),octave=1) | delay(measure))+(finger2.next(measure) | delay(measure))
                output = alpha//(beta | delay(measure*2))
                self.hand = [finger1,finger2]
                self.last = output | transforms.stretch(.5)
                try:
                        player.play([self.last | midi_pitch()])
                except Exception as e:
                        print e


        def last(self):
                return self.last






'''
when picking a next note, choose to modify the previous somehow
perhaps augmenting it or making it sharp or flat
the picker's stickiness could be adjusted for different genres
'''