import random
from sebastian.lilypond.interp import parse
from sebastian.core.transforms import reverse
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.midi import player
from sebastian.core.transforms import transpose, reverse, add, degree_in_key, midi_pitch, lilypond

OFFSET_64 = 'OFFSET_64'
notes_in_an_octave = 12

class Keyboard(object):
    notes = []
    #range(48,12) = middle c
    def __init__(self):
        self.notes = HSeq(Point(midi_pitch=pitch) for pitch in range(21,108))

class MinorBluesKeyboard(Keyboard):
    """docstring for BluesKeyboard"""
    def __init__(self):
        super(MinorBluesKeyboard, self).__init__()
        bluesminor = HSeq(Point(midi_pitch=pitch) for pitch in [0, 3, 5, 6, 7, 10])
        self.notes = bluesminor
        for t in range(0, 9):
            print bluesminor
            bluesminor = bluesminor | transpose(notes_in_an_octave) #it's 12
            self.notes += bluesminor
        self.notes = self.notes | add({DURATION_64:3})

class NewMinorBluesKeyboard(Keyboard):
    """docstring for BluesKeyboard"""
    def __init__(self):
        super(NewMinorBluesKeyboard, self).__init__()
        bluesminor = HSeq(Point(midi_pitch=pitch) for pitch in [0, 3, 5, 6, 7, 10])
        self.notes = bluesminor | transpose(notes_in_an_octave*2)
        for t in range(4, 11):
            bluesminor = bluesminor | transpose(notes_in_an_octave) #it's 12
            self.notes += bluesminor

class PentatonicKeyboard(Keyboard):
    """docstring for BluesKeyboard"""
    def __init__(self):
        super(PentatonicKeyboard, self).__init__()
        pentatonic = HSeq(Point(midi_pitch=pitch) for pitch in [0,2,3,6,7])
        self.notes = pentatonic
        for t in range(0, 9):
            pentatonic = pentatonic | transpose(notes_in_an_octave) #it's 12
            self.notes += pentatonic

class Randomized(object):
    def __init__(self, population, stickiness=0):
        self.population = population
        self.buffer = []
        self.memory = 5
        self.stickiness = stickiness
        self.reset()

    def reset(self):
        self.max = len(self.population)-1

    def pick(self):
        pick = random.randint(0, self.max)
        next = self.population[pick]
        self.buffer.append(next)
        return next

    def last(self):
        try:
            return self.buffer[len(self.buffer)-1]
        except Exception as e:
            print len(self.buffer)-1
            return 0

    def next(self):
        stick = random.randint(0,self.stickiness)
        if stick == 0:
            return self.pick()
        else:
            self.buffer.append(self.last())
            return self.last()

    def echo(self):
        return Echo(self)

class Echo(object):
    def __init__(self, picker):
        self.picker = picker
        self.last = None
        self.buffer = []

    def reset(self):
        pass

    def next(self):
        next = self.picker.last()
        self.buffer.append(next)
        return next

    def echo(self):
        return Echo(self)

class Wandering(Randomized):
    def __init__(self, population, stickiness=0, step=2):
        super(Wandering, self).__init__(population, stickiness)
        self.step = step
        self.reset()

    def reset(self):
        self.max = len(self.population)-1
        self.highest = random.randint(0,len(self.population)/2)

    def pick(self):
        if self.highest >= self.max:
            pick = random.randint(self.max-self.step, self.max)
        elif self.highest <= 0:
            pick = random.randint(0,0+self.step)
        else:
            pick = random.randint(self.highest-self.step, self.highest+self.step)
            self.highest = pick
        try:
            next = self.population[pick]
        except Exception as e:
            next = self.last()
        self.buffer.append(next)
        return next

class Oscilating(Randomized):
    def __init__(self, population):
        super(Oscilating, self).__init__(population)
        self.reset()

    def reset(self):
        self.increasting = True
        self.max = len(self.population)-1
        self.last_pick = -1

    def pick(self):
        if self.last_pick >= self.max:
            self.increasting = False
        elif self.last_pick <= 0:
            self.increasting = True

        if self.increasting:
            pick = self.last_pick+1
        else:
            pick = self.last_pick-1
        self.last_pick = pick
        next = self.population[pick]
        self.buffer.append(next)
        return next

class Constant(object):
    def __init__(self, population):
        self.population = population
        self.last = None

    def next(self):
        self.last = self.population
        return self.last

class Sticky(Randomized):
    def __init__(self, population, chance, max):
        """
        :param chance: the chance of getting unstuck, always to OSequence
        :param max: most times in a row possible before a change
        """
        super(Sticky, self).__init__()


class Ascending(object):
    def __init__(self, population):
        self.population = population
        self.last = None
        self.reset()
        

    def next(self):
        if self.highest == self.max:
            pick = self.highest
        else:
            pick = random.randint(self.highest, self.highest+1)
            self.highest = pick
            self.last = self.population[pick]
            return self.last


    def reset(self):
        self.max = len(population)-1
        self.highest = random.randint(0,len(self.population)/2)


def mound(seq):
    return seq + (seq | reverse())

def multiply(seq, matrix):
    output = seq
    for m in matrix:
        output = output // (seq | transpose(m))
    return output

def silence(seq):
    return seq | add({'velocity':0})

def loop(loops):
    last = None
    output = None
    for l in loops:
        if last == None:
            last = l
            output = last
        else:
            last = last // l
            output = output + last
    return output



def humanize(seq, pitch=0, duration=0, velocity=0, offset=0):
    output = []
    for point in seq:
        new_pitch = random.randint(point['midi_pitch']-pitch,point['midi_pitch']+pitch)
        new_velocity = random.randint(point['velocity']-velocity,point['velocity']+velocity)
        new_duration = random.randint(point[DURATION_64]-duration,point[DURATION_64]+duration)
        new_offset = random.randint(point[OFFSET_64]-offset,point[OFFSET_64]+offset)
        point.update({
        'midi_pitch':new_pitch,
        DURATION_64:new_duration,
        'velocity':new_velocity,
        OFFSET_64:new_offset
        })
        
        output.append(point)
    return OSequence(output)



class AutoComposer(object):
    notes = ['a','b','c','d','e','f','g']
    octave = parse("c cis d dis e f fis g gis a ais b")
    sharpnesses = [",", "", "'"]
    keyboard = []
    last_sequence = []

    def __init__(self):
        keys = MinorBluesKeyboard()
        self.keyboard = keys.notes

    def gen_rand_snippet(self, counts=None):
        snippet=" "
        tuples = []
        note = Randomized(self.notes)
        sharpness = Randomized(self.sharpnesses)
        duration = Randomized(range(1,30))

        if counts == None:
            counts = random.randint(1,30)
        for i in range(counts):
            tuples.append(note.next()+sharpness.next()+str(duration.next()))

        return snippet.join(tuples)

    def gen_rand_snippet_ascending(self, counts=None):
        snippet=" "
        tuples = []
        note = Ascending(self.notes)
        sharpness = Ascending(self.sharpnesses)
        duration = Ascending(range(1,30))

        if counts == None:
            counts = random.randint(1,30)
        for i in range(counts):
            tuples.append(note.next()+sharpness.next()+str(duration.next()))

        return snippet.join(tuples)

    def gen_rand_seq(self, counts=None):
        snippet=" "
        seq = HSeq()
        note = Wandering(self.keyboard)
        duration = Wandering(range(4,8),3)
        velocity = Wandering(range(40,127),10)

        if counts == None:
            counts = random.randint(1,30)
        for i in range(counts):
            next = note.next()
            next.update({DURATION_64: duration.next(), "velocity": velocity.next()})
            seq.append(next)

        self.last_sequence = seq
        return seq



    def play_rand_song_uno(self, counts=20):
        alpha = parse(self.gen_rand_snippet(counts))
        beta = parse(self.gen_rand_snippet(counts))
        gamma = parse(self.gen_rand_snippet(counts))
        delta = parse(self.gen_rand_snippet(counts))
        player.play([alpha, beta])
        player.play([alpha, gamma])
        player.play([beta, gamma])
        player.play([alpha])


    def play_rand_song_dos(self, counts=20):
        alpha = parse(self.gen_rand_snippet(counts))
        beta = parse(self.gen_rand_snippet(counts))
        gamma = parse(self.gen_rand_snippet(counts))
        delta = parse(self.gen_rand_snippet(counts))
        player.play([alpha+(alpha//beta)+(alpha//beta//gamma)+(alpha//beta//gamma//delta)])


class Finger(object):

    def __init__(self, length, note, duration, velocity):
        self.length = length
        self.note = note
        self.duration = duration
        self.velocity = velocity
        self.last = None

    def next(self, length):
        self.note.reset()
        self.duration.reset()
        self.velocity.reset()
        seq = HSeq()
        total_length = 0
        while total_length < length:
            next = self.note.next() 
            next_duration = self.duration.next()
            total_length += next_duration
            next.update({DURATION_64: next_duration, "velocity": self.velocity.next()})
            seq.append(next)

        self.last = OSequence(seq)
        return self.last

    def next_by_counts(self, count=None):
        self.note.reset()
        self.duration.reset()
        self.velocity.reset()
        seq = HSeq()
        if counts != None:
            counts = random.randint(1,30)
        for i in range(counts):
            next = self.note.next()
            next.update({DURATION_64: self.duration.next(), "velocity": self.velocity.next()})
            seq.append(next)

        self.last = OSequence(seq)
        return self.last



"""
hands for genres, templates for songs
"""