from sebastian.lilypond.interp import parse
from sebastian.midi import write_midi, player
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.core.transforms import transpose, reverse, add, degree_in_key, midi_pitch
from sebastian.core.notes import Key, major_scale
import random

from core.composition import *
from core.transforms import *
import sebastian.core.transforms as transforms
from transforms import delay

class Dramatic(object):
        def __init__(self):
                self.hand = []

        def next(self):
                keys = Keyboard().notes
                self.keys = keys
                stretch_length = random.randint(2,5)
                left_low = random.randint(40,70)
                left_range = random.randint(1,2)
                left = HSeq(list(keys).__getslice__(left_low,left_low+left_range))
                right = HSeq(list(keys).__getslice__(20,50))

                note1 = Wandering(keys)
                duration1 = Oscilating(range(2,8))
                velocity1 = Randomized(range(20,127))

                note2 = Wandering(left)
                duration2 = Randomized(range(0,len(left)))
                velocity2 = Wandering(range(70,90))

                note3 = note2.echo()
                duration3 = Randomized(range(2,12))
                velocity3 = Wandering(range(20,127))

                finger1 = Finger(
                length = 16,
                note = note1,
                duration = duration1,
                velocity = velocity1
                )

                finger2 = Finger(
                        length = 160,
                        note = note2,
                        duration = duration2,
                        velocity = velocity2
                        )

                finger3 = Finger(
                        length = 16,
                        note = note2,
                        duration = duration3,
                        velocity = velocity3
                        )

                finger4 = Finger(
                        length = 16,
                        note = Wandering([1,2,3]),
                        duration = Randomized([4,6]),
                        velocity = Wandering(range(40,50))
                        )
                x=800
                
                drone = (finger1.next(50) | transforms.stretch(1))*3
                solo1 = finger1.next(x)
                #solo2 = mutate(finger1.last,1,1,1,1)
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
                keys = PentatonicKeyboard().notes
                stretch_length = random.randint(2,5)
                left_low = random.randint(40,70)
                left_range = random.randint(1,2)
                left = HSeq(list(keys).__getslice__(left_low,left_low+left_range))
                right = HSeq(list(keys).__getslice__(20,50))

                note1 = Wandering(keys)
                duration1 = Wandering(range(2,8))
                velocity1 = Randomized(range(20,127))

                note2 = Wandering(left)
                duration2 = Randomized(range(0,len(left)))
                velocity2 = Wandering(range(70,90))

                note3 = note2.echo()
                duration3 = Randomized(range(2,12))
                velocity3 = Wandering(range(20,127))

                finger1 = Finger(
                length = 1160,
                note = note1,
                duration = duration1,
                velocity = velocity1
                )
                self.hand = [finger1]
                x = 160
                #player.play([loop([finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x),finger1.next(x)])])
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
        keyboards = [Keyboard(), MinorBluesKeyboard(), EvenKeyboard(), OddKeyboard(), PentatonicKeyboard()]
        pickers = [
        Randomized(),
        Wandering(), 
        Oscilating(), 
        Ascending(), 
        Constant()
        ]
        '''

        def next(self):
                keys = EvenKeyboard().notes
                self.keys = list(keys)
                keycount = len(self.keys)
                stretch_length = random.randint(2,5)
                left_low = random.randint(keycount/4,(keycount/2))
                left_range = random.randint(1,2)
                mids = HSeq(self.keys.__getslice__(left_low,left_low+left_range))
                right = HSeq(self.keys.__getslice__(keycount-(keycount/4), keycount-1))

                finger1 = Finger(
                length = 16,
                note = Wandering(mids),
                duration = Wandering(range(2,4)),
                velocity = Wandering(range(20,127)),
                rest = Randomized(range(0,4))
                )

                finger2 = Finger(
                        length = 160,
                        note = Wandering(right),
                        duration = Randomized(range(2,80)),
                        velocity = Wandering(range(50,90)),
                        rest = Randomized([1,2,3,4,5])
                        )

                finger3 = Finger(
                length = 16,
                note = Wandering(mids),
                duration = Oscilating(range(2,8)),
                velocity = Randomized(range(20,127)),
                rest = Randomized([10,20,40])
                )


                x=800
                
                drone = (finger1.next(90) | transforms.stretch(1))*2
                #drone = multiply(drone,[-3])
                measure = drone.next_offset()-1
                #metrenome 
                alpha = (drone*2)+(mutate(drone,1,2,1,2,0))+(drone*2)+(mutate(drone,1,2,1,0,1))+(drone*2)+(mutate(drone,1,2,1,0,1))+(drone*2)
                drone2 = (finger1.next(90) | transforms.stretch(1))*2
                mutated_drone2 = (mutate(drone2,1,2,1,0,1))
                beta = (drone*2)+(mutated_drone2)+(drone2*2)+(mutated_drone2)+(drone2*2)+(mutated_drone2)+(drone2*2)
                solo1 = finger2.next(measure)+(mutate(finger2.next(measure),octave=1) | delay(measure))+(finger2.next(measure) | delay(measure))
                output = alpha//(beta | delay(measure*2))
                self.hand = [finger1,finger2]
                self.last = output | transforms.stretch(.25)
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
        keyboards = [Keyboard(), MinorBluesKeyboard(), EvenKeyboard(), OddKeyboard(), PentatonicKeyboard()]
        pickers = [
        Randomized(),
        Wandering(), 
        Oscilating(), 
        Ascending(), 
        Constant()
        ]
        '''

        def next(self):
                keys = PentatonicKeyboard().notes
                self.keys = list(keys)
                keycount = len(self.keys)
                stretch_length = random.randint(2,5)
                left_low = random.randint(keycount/4,(keycount/2))
                left_range = random.randint(1,2)
                mids = HSeq(self.keys.__getslice__(left_low,left_low+left_range))
                right = HSeq(self.keys.__getslice__(keycount-(keycount/4), keycount-1))

                finger1 = Finger(
                length = 16,
                note = Wandering(mids),
                duration = Oscilating([16, 32]),
                velocity = Randomized(range(20,127)),
                rest = Randomized([16, 32])
                )

                finger2 = Finger(
                        length = 160,
                        note = Wandering(right),
                        duration = Randomized([8,16,24,32]),
                        velocity = Wandering(range(50,90)),
                        rest = Randomized([8,16,24,32])
                        )

                finger3 = Finger(
                length = 16,
                note = Wandering(mids),
                duration = Oscilating(range(2,8)),
                velocity = Randomized(range(20,127)),
                rest = Randomized([10,20,40])
                )


                x=800
                
                drone = (finger1.next(80))*2
                #drone = multiply(drone,[-3])
                measure = drone.next_offset()-1
                #metrenome 
                alpha = (drone*2)+(mutate(drone,1,2,1,2,0))+(drone*2)+(mutate(drone,1,2,1,0,1))+(drone*2)+(mutate(drone,1,2,1,0,1))+(drone*2)
                drone2 = (finger1.next(90) | transforms.stretch(.5))*2
                mutated_drone2 = (mutate(drone2,1,2,1,0,1))
                beta = (drone*2)+(mutated_drone2)+(drone2*2)+(mutated_drone2)+(drone2*2)+(mutated_drone2)+(drone2*2)
                solo1 = finger2.next(measure)+(mutate(finger2.next(measure),octave=1) | delay(measure))+(finger2.next(measure) | delay(measure))
                output = alpha//(beta | delay(measure*2))
                self.hand = [finger1,finger2]
                self.last = output | transforms.stretch(.5)
                try:
                        player.play([self.last | midi_pitch()])
                except Exception as e:
                        print e


        def last(self):
                return self.last



class Omatic(object):
        def __init__(self):
                self.hand = []
        '''
        keyboards = [Keyboard(), MinorBluesKeyboard(), EvenKeyboard(), OddKeyboard(), PentatonicKeyboard()]
        pickers = [
        Randomized(),
        Wandering(), 
        Oscilating(), 
        Ascending(), 
        Constant()
        ]
        '''

        def next(self):
                keys = PentatonicKeyboard().notes
                self.keys = list(keys)
                keycount = len(self.keys)
                stretch_length = random.randint(2,5)
                left_low = random.randint(keycount/4,(keycount/2))
                left_range = random.randint(1,8)
                mids = HSeq(self.keys.__getslice__(left_low,left_low+left_range))
                right = HSeq(self.keys.__getslice__(keycount-(keycount/4), keycount-1))

                finger1 = Finger(
                length = 16,
                note = Wandering(mids),
                duration = Oscilating([2,4,8,16,32]),
                velocity = Randomized(range(20,127)),
                rest = Randomized([2,4,8,16,32])
                )

                finger2 = Finger(
                        length = 160,
                        note = Wandering(right),
                        duration = Randomized(range(2,80)),
                        velocity = Wandering(range(50,90)),
                        rest = Randomized([1,2,3,4,5])
                        )

                finger3 = Finger(
                length = 16,
                note = Wandering(mids),
                duration = Randomized([2,4,8,16,32]),
                velocity = Randomized(range(20,127)),
                rest = Oscilating([2,4,8,16,32])
                )


                x=800
                
                drone = (finger1.next(256) | transforms.stretch(.5))*2
                #drone = multiply(drone,[-3])
                measure = drone.next_offset()
                #metrenome 
                alpha = (drone*2)+(mutate(drone,1,2,1,2,0))+(drone*2)+(mutate(drone,1,2,1,0,1))+(drone*2)+(mutate(drone,1,2,1,0,1))+(drone*2)
                drone2 = (finger3.next(256) | transforms.stretch(1))*2
                mutated_drone2 = (mutate(drone2,1,2,1,0,1))
                beta = (drone*2)+(mutated_drone2)+(drone2*2)+(mutated_drone2)+(drone2*2)+(mutated_drone2)+(drone2*2)
                solo1 = finger2.next(measure)+(mutate(finger2.next(measure),octave=1) | delay(measure))+(finger2.next(measure) | delay(measure))
                output = alpha//(beta | delay(measure*2))
                self.hand = [finger1,finger2]
                self.last = output | transforms.stretch(1)
                try:
                        player.play([self.last | midi_pitch()])
                except Exception as e:
                        print e


        def last(self):
                return self.last

class Mutational(object):
        def __init__(self):
                self.hand = []
        '''
        keyboards = [Keyboard(), MinorBluesKeyboard(), EvenKeyboard(), OddKeyboard(), PentatonicKeyboard()]
        pickers = [
        Randomized(),
        Wandering(), 
        Oscilating(), 
        Ascending(), 
        Constant()
        ]
        '''

        def next(self):
                keys = PentatonicKeyboard().notes
                self.keys = list(keys)
                keycount = len(self.keys)
                stretch_length = random.randint(2,5)
                left_low = random.randint(keycount/4,(keycount/2))
                left_range = random.randint(1,8)
                mids = self.keys.__getslice__(left_low,left_low+left_range)
                right = HSeq(self.keys.__getslice__(keycount-(keycount/4), keycount-1))
                print mids

                finger1 = Finger(
                length = 16,
                note = Wandering(mids),
                duration = Oscilating([2,4,8,16,32]),
                velocity = Randomized(range(20,127)),
                rest = Randomized([2,4,8,16,32])
                )

                finger2 = Finger(
                        length = 160,
                        note = Wandering(right),
                        duration = Randomized(range(2,80)),
                        velocity = Wandering(range(50,90)),
                        rest = Randomized([5])
                        )

                finger1_shifted = Finger(
                length = 16,
                note = Wandering(keys),
                duration = Oscilating([10]),
                velocity = Randomized(range(20,127)),
                rest = Randomized([1])
                )


                x=800
                
                drone = (finger1.next(856*2) | transforms.stretch(.5))*2
                self.drone = drone
                self.phrase1 = (drone*2)+(mutate(drone,1,2,1,2,1))+(drone*2)+(mutate(drone,1,2,1,0,1))+(drone*2)+(mutate(drone,1,2,1,0,1))+(drone*2)
                measure = drone.next_offset()-1
                #metrenome 
                #alpha = generations(phrase1,5,1,2,1,2,0)
                output = self.phrase1
                self.hand = [finger1,finger2]
                self.last = output | transforms.stretch(.5) 
                try:
                        player.play([self.last | midi_pitch()])
                except Exception as e:
                        print e

                #new_variable = sequence | transform_function(paramaters) | transform_function(paramaters)  |transform_function(paramaters) 

                #newer_variable = new_variable | transform_function(paramaters) | transform_function(paramaters)  |transform_function(paramaters)          

        def last(self):
                return self.last


class BeatBased(object):
        def __init__(self):
                self.hand = []
        '''
        keyboards = [Keyboard(), MinorBluesKeyboard(), EvenKeyboard(), OddKeyboard(), PentatonicKeyboard()]
        pickers = [
        Randomized(),
        Wandering(), 
        Oscilating(), 
        Ascending(), 
        Constant()
        ]
        '''

        def next(self):
                keys = EvenKeyboard().notes
                self.keys = list(keys)
                keycount = len(self.keys)
                right = HSeq(self.keys.__getslice__(keycount-(keycount/2), keycount-(keycount/4)))
                whole = 64
                seed_pitch = random.randint(1,12)
                seed_unit = random.choice([1,2,4,8,16])
                seed_duration = whole/seed_unit
                measure_length = 4*whole
                phrase_lengths = range(50,90)
                phrase_length = Randomized(phrase_lengths)
                reaches = range(-1,1)
                reach = Wandering(reaches)

                finger1 = Finger(
                length = 16,
                note = Wandering(right),
                duration = Randomized([2,4,4,4,4,4,4,4,4,4,5,6,9,8,8,8,8,16,32,32,32]),
                velocity = Randomized(range(20,127)),
                rest = Randomized([2,4,8,16,32,32,32,32,32,32,32,32])
                )

                finger2 = Finger(
                        length = 160,
                        note = Wandering(keys),
                        duration = Randomized(range(2,80)),
                        velocity = Wandering(range(50,90)),
                        rest = Randomized([1,2,3,4,5])
                        )

                finger3 = Finger(
                length = 16,
                note = Wandering(keys),
                duration = Randomized([2,4,8,16,32]),
                velocity = Randomized(range(20,127)),
                rest = Oscilating([2,4,8,16,32])
                )


                beat = metrenome(seed_unit,seed_pitch,5,seed_duration)
                measure_length = beat.next_offset()
                phrase_length_new = phrase_length.next()
                phrase1 = finger1.next(phrase_length_new)
                phrase1_b = mutate(phrase1,1,2,1,0,0)
                phrase2 = finger2.next(phrase_length_new*2)
                phrase2_b = mutate(phrase2,1,2,1,0,0)
                phrase3 = finger1.next(phrase_length_new*3)
                phrase1_3 = mutate(phrase3,1,2,1,0,0)
                #metrenome 
                left_seq = (phrase1*3)+phrase1_b+(phrase3*3)+phrase1_b
                right_seq = (phrase2*3)+phrase2_b+(phrase2*3)+phrase2_b
                left_composition = (left_seq*2)+((left_seq*2) | transpose(reach.next()) )+(left_seq*2)
                self.output = left_composition#//(right_seq | delay(phrase1.next_offset()*2))
                self.hand = [finger1,finger2]
                self.last = self.output | transforms.stretch(.25)
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



class Jeff_old(object):
        def __init__(self):
                self.hand = []

        def next(self):
                keys = MajorKeyboard().notes
                self.keys = list(keys)
                keys = HSeq(self.keys.__getslice__(40,50))

                keycount = len(self.keys)

                stretch_length = ()

                finger1 = Finger(
                length = 160,
                note = Wandering(keys),
                duration = Wandering([2]),
                velocity = Wandering(range(50,51)),
                rest = Randomized([2])
                )
                
                finger2 = Finger(
                length = 160,
                note = Wandering(keys),
                duration = Wandering([2]),
                velocity = Wandering(range(50,51)),
                rest = Randomized([2])
                )

                alpha = finger1.next(100) 
                beta = finger2.next(100)
                gamma = finger1.next(70)
                self.hand = [finger1]
                self.last = alpha // beta


                try:
                        player.play([self.last | midi_pitch()])
                except Exception as e:
                        print e


        def last(self):
                return self.last

class JeffBLUES_SUCESS(object):
        def __init__(self):
                self.hand = []

        def next(self):
                keys = MinorBluesKeyboard().notes
                self.keys = list(keys)

                keycount = len(self.keys)

                stretch_length = ()

                finger1 = Finger(
                length = 300,
                note = Wandering(HSeq(self.keys.__getslice__(20,40))),
                duration = Wandering([8]),
                velocity = Wandering(range(50,51)),
                rest = Randomized([8])
                )
                
                finger2 = Finger(
                length = 300,
                note = Oscilating(HSeq(self.keys.__getslice__(10,20))),
                duration = Oscilating([32]),
                velocity = Oscilating(range(50,51)),
                rest = Randomized([0])
                )

                alpha = finger1.next(60)
                beta = finger2.next(60)
                gamma = finger1.next(70)
                self.hand = [finger1]
                sequence_1 = (alpha//beta) | transforms.stretch(.5)
                #sequence_2 = sequence_1 | transforms.stretch(.5)
                sequence_2 = sequence_1 | transpose(11)
                sequence_3 = sequence_1 | transpose(1)
                self.last = sequence_1+sequence_2+sequence_3+sequence_1

                try:
                        player.play([self.last | midi_pitch()])
                except Exception as e:
                        print e


        def last(self):
                return self.last




class Transposify(object):
        def __init__(self):
                self.hand = []

        def next(self):
                keys = MajorKeyboard().notes
                self.keys = list(keys)
                keys = HSeq(self.keys.__getslice__(40,80))


                keycount = len(self.keys)

                stretch_length = (80)

                finger1 = Finger(
                length = 16,
                note = Wandering(keys),
                duration = Wandering([2,4,8]),
                velocity = Wandering(range(50,100)),
                rest = Randomized([2,4])
                )
                x=200
                
                drone = (finger1.next(90) | transforms.stretch(1))*2
                #drone = multiply(drone,[-3])
                measure = drone.next_offset()-1
                #metrenome 
                alpha = finger1.next(200)
                self.hand = [finger1]
                self.last = alpha


                try:
                        player.play([self.last | midi_pitch()])
                except Exception as e:
                        print e


        def last(self):
                return self.last


class JazzBot(object):
        def __init__(self):
                self.hand = []

        def next(self):
                keys = MinorKeyboard().notes
                self.keys = list(keys)
                keycount = len(self.keys)
                base = Randomized([40,80,120,240]).next()
                measure = metrenome(base/2,octave=5, bpm=base)
                #two sequences that make different audible metrenomes
                tick = metrenome(base/2,octave=10, bpm=base)
                tock = metrenome(base/2,octave=10, bpm=base, velocity=Randomized([0,20,40,60,80,90]).next()) | mutate(0,0,30,0,0)


                finger1 = Finger(
                length = measure.next_offset(),
                note = Wandering(HSeq(self.keys.__getslice__(20,23))),
                duration = Wandering([4,8,16,32,64]),
                velocity = Wandering(range(50,51)),
                rest = Randomized([8])
                )

                finger2 = Finger(
                length = measure.next_offset(),
                note = Wandering(HSeq(self.keys.__getslice__(23,24))),
                duration = Wandering([4,8,16,32,64]),
                velocity = Wandering(range(30,41)),
                rest = Randomized([8])
                )

                finger3 = Finger(
                length = measure.next_offset(),
                note = Wandering(HSeq(self.keys.__getslice__(26,27))),
                duration = Wandering([4,8,16,32,64]),
                velocity = Wandering(range(30,41)),
                rest = Randomized([8])
                )

                transpositions = Randomized([-2,2,4,6,8])

                def fade_mutate(incoming, count, mutation_matrix=[0,2,30,0,0]):
                        output = OSequence()
                        last = incoming
                        for r in xrange(16):
                                current = last | mutate(mutation_matrix[0], mutation_matrix[1], mutation_matrix[2], mutation_matrix[3], mutation_matrix[4])
                                output += (tock//incoming // current) | transpose(transpositions.next())
                                last = current
                        return output

                def generate_jazz():
                        seq_1 = fade_mutate(finger1.next(measure.next_offset()),4)
                        seq_2 = fade_mutate(finger1.next(measure.next_offset()),4)
                        output = seq_1 // seq_2
                        return output

                output = generate_jazz()//(generate_jazz() | delay(measure.next_offset()*1))//(generate_jazz() | delay(measure.next_offset()*2))
                

                self.hand = [finger1]
                sequence_1 = (output)

                self.last = sequence_1
                #print self.last | midi_pitch()
                try:
                        player.play([self.last | midi_pitch()])
                except Exception as e:
                        print e


        def last(self):
                return self.last


class Neustar(object):
        def __init__(self):
                self.hand = []

        def next(self):
                keys = MajorKeyboard().notes
                self.keys = list(keys)

                keycount = len(self.keys)

                stretch_length = ()

                finger1 = Finger(
                length = 300,
                note = Wandering(HSeq(self.keys.__getslice__(20,80))),
                duration = Wandering([8,4]),
                velocity = Wandering(range(50,51)),
                rest = Randomized([8])
                )
                
                finger2 = Finger(
                length = 300,
                note = Oscilating(HSeq(self.keys.__getslice__(10,20))),
                duration = Oscilating([32]),
                velocity = Oscilating(range(50,51)),
                rest = Randomized([0])
                )

                finger3 = Finger(
                length = 300,
                note = Wandering(self.keys),
                duration = Wandering([2,4,6,8,16]),
                velocity = Wandering(range(50,80)),
                rest = Wandering([2,4,6,8,16])
                )

                g = 50
                self.hand = [finger1]
                sequence_1 = (finger1.next(g)//finger2.next(g))
                sequence_1_a = sequence_1 | transpose(11)
                sequence_1_b = sequence_1 | transpose(1) 

                sequence_2 = (finger2.next(g)//finger2.next(g))
                sequence_2_a = sequence_1 | transpose(11)
                sequence_2_b = sequence_1 | transpose(1) 

                sequence_3 = (finger1.next(g)//finger1.next(g))
                sequence_3_a = sequence_1 | transpose(11)
                sequence_3_b = sequence_1 | transpose(1) 

                solo = finger3.next(g*6)
                self.last = sequence_1+sequence_1_a+((sequence_2_b+sequence_2+sequence_1+sequence_3_a+sequence_3_b+sequence_1_a))+sequence_2

                try:
                        player.play([sequence_1 | midi_pitch()])
                except Exception as e:
                        print e


        def last(self):
                return self.last


class TimeBot(object):
        def __init__(self):
                self.hand = []

        def next(self, mutation_matrix=[0,0,0,0,0]):
                measure = metrenome(120,octave=5, bpm=120)
                voice1 = measure |mutate(1,2,0,0,0)
                half_measure = metrenome(120,octave=5, bpm=240)
                delay = metrenome(10,octave=5, bpm=120)
                new = half_measure | delay(delay.next_offset())

                self.last = measure // voice1

                try:
                        player.play([self.last | midi_pitch()])
                except Exception as e:
                        print e


        def last(self):
                return self.last



