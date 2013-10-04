import random
from sebastian.lilypond.interp import parse
from sebastian.core.transforms import reverse
from sebastian.core import OSequence, HSeq, Point, DURATION_64
from sebastian.midi import player
from sebastian.core.transforms import transpose, reverse, add, degree_in_key, midi_pitch #lilypond
print transpose

OFFSET_64 = 'offset_64'
range_of_pitches = range(1,12)
range_of_octaves = range(0,10)
range_of_durations = range(1,100)
range_of_valocities = range(0,100)
rosetta_stone = [5,0,7,2,9,4,11,6,1,8,3,10]


class Keyboard(object):
    notes = HSeq()
    #range(48,12) = middle c
    def __init__(self, hseq=None):
        if hseq == None:

            self.pitches =  rosetta_stone
            #what it should be in reality[5,0,7,2,9,4,11,6,1,8,3,10]
            self.notes = self.get_octaves(range(1,9))
        else:
            self.notes = hseq

    def get_octaves(self, octaves):
        output = HSeq()
        for r in octaves:
            octave = HSeq(Point(pitch=rosetta_stone[pitch], octave=r, velocity=90, duration_64=10) for pitch in self.pitches)
            output = output + octave
        return output

    def get_octaves_as_keyboard(self, octaves):
        hseq = self.get_octaves(octaves)
        return Keyboard(hseq)

    def play(self):
        player.play([OSequence(self.notes | midi_pitch())])



'''
class Keyboard(object):
    notes = []
    #range(48,12) = middle c
    def __init__(self):
        self.notes = HSeq(Point(pitch=pitch) for pitch in range(21,108))
'''

class MinorBluesKeyboard(Keyboard):
    """docstring for BluesKeyboard"""
    def __init__(self):
        super(MinorBluesKeyboard, self).__init__()
        self.pitches = [0, 3, 5, 6, 7, 10]
        #[3,]
        self.notes = self.get_octaves(range(1,9))

class EvenKeyboard(Keyboard):
    """docstring for EvenKeyboard"""
    def __init__(self):
        super(EvenKeyboard, self).__init__()
        self.pitches = [0, 2, 4, 6, 8, 10]
        self.notes = self.get_octaves(range(1,9))

class OddKeyboard(Keyboard):
    """docstring for OddKeyboard"""
    def __init__(self):
        super(OddKeyboard, self).__init__()
        self.pitches = [1,3,5,7,9,11]
        self.notes = self.get_octaves(range(1,9))

class MajorKeyboard(Keyboard):
    """docstring for MajorKeyboard"""
    def __init__(self):
        super(MajorKeyboard, self).__init__()
        self.pitches = [1,3,5,0,2,4,6]
        self.notes = self.get_octaves(range(1,9))

class PentatonicKeyboard(Keyboard):
    """docstring for PentatonicKeyboard"""
    def __init__(self):
        super(PentatonicKeyboard, self).__init__()
        self.pitches = [0,2,3,6,7]
        self.notes = self.get_octaves(self.pitches, range(1,9))

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

    def reset(self):
        pass

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

def metrenome(count, pitch=5, octave=5, rest=64):
    output = []
    total = 0
    duration = 1
    for r in range(0,count):
        beat = Point(pitch=pitch, octave=octave, velocity=90, duration_64=duration, offset_64=total+rest)
        total+=(duration+rest)
        output.append(beat)
    return OSequence(output)


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

def generations(sequence, generations=2, pitch=0, duration=0, velocity=0, offset=0, octave=0):
    last = sequence
    output = sequence
    for l in range(1,generations+1):
        sequence += mutate(last, pitch, duration, velocity, offset, octave)

    return output

def mutate(seq, pitch=0, duration=0, velocity=0, offset=0, octave=0):
    output = []
    octave_delta = random.randint(-1*octave,octave)
    for point in seq:

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

        output.append(new_point)
    return OSequence(output)

def deconstruct(seq, steps=1):
    '''
    gradually remove all notes in a sequence over n steps
    '''
    notes = list(seq)
    for n in range(steps):
      pass  





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

    def __init__(self, length=None, note=None, duration=None, velocity=None, rest=None):
        self.length = length
        self.note = note
        self.duration = duration
        self.velocity = velocity
        print "rest "+str(rest)
        self.rest = rest
        self.last = None

    def next(self, length):
        self.note.reset()
        self.duration.reset()
        self.velocity.reset()
        try:
            self.rest.reset()
        except Exception as e:
            print e
        seq = HSeq()
        total_length = 0
        while total_length < length:
            next = self.note.next() 
            next_duration = self.duration.next()
            next_rest = self.rest.next()
            if total_length+next_duration+next_rest > length:
                #if there isn't time for this note, fill the rest of the time with silence 
                print "fill"
                duration_left = length - total_length
                next.update({DURATION_64: duration_left, OFFSET_64: total_length, "velocity": 0})
            else:
                print "add"
                next.update({DURATION_64: next_duration, OFFSET_64: total_length, "velocity": self.velocity.next()})
            total_length += next_duration+next_rest
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