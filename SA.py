import random
import numpy as np
import matplotlib.pyplot as plt
import schematax as sx
import time
from sounds.player import player
from liblo import *
import sys
import os
def all_ones(indv):
    return indv.count('1')

low = "./sounds/HACK THE BRAIN SOUNDS/LOW"
mid = "./sounds/HACK THE BRAIN SOUNDS/MID"
high = "./sounds/HACK THE BRAIN SOUNDS/HIGH"


low_sounds = [low + '/' + x for x in os.listdir(low)]
mid_sounds = [mid + '/' + x for x in os.listdir(mid)]
high_sounds = [high + '/' + x for x in os.listdir(high)]

all_sounds = low_sounds + mid_sounds + high_sounds




class SA(object):

    def __init__(self,func = all_ones,n=10,p=16,mu=0.1,s=0,e=False):
        """
        n: number of indvs
        p: number of bits for each indv
        mu: mutation rate
        s: selction type: 0 = roullete whel
        e: eleitism.
        """ 
        self.n = n
        self.p = p
        self.mu = mu
        self.s = s
        self.e = e
        self.schemata =[]

        self.pop = [] #current pop go here
        self.best = '' #stores best overall indivdual
        self.bests = [] #stores best individual from each gen
        self.best_f = -float('inf') #the fittness of the best overal indivdual

        self.av_f = [] #stores the average fitness of each population

        self.func = func
        self.player = player()
        #self.player.add_sound('./sounds/100.mp3')
        for sound in all_sounds:
            self.player.add_sound(sound)


    def init_pop(self):
        self.pop = [''.join(str(random.choice(['1','0'])) for _ in xrange(self.p)) for _ in xrange(self.p) ]
    
    def mutate(self,indv):
        return ''.join(str(int(not(int(x)))) if random.random() <= self.mu else x for x in indv)

    def crossover(self,ma,da):
        pivot = random.randint(0,self.p)

        son = ma[:pivot] + da[pivot:]
        daught = da[:pivot] + ma[pivot:]

        return [son,daught]
    
    def eval_pop(self):
        import time
        import numpy
        self.fs = {}
        bestp = ''
        bestpf = -float('inf')
        for indv in self.pop:
            self.player.play(indv)
            mel_old = server.signal['mel']
            first = len(mel_old)
            time.sleep(25)
            mel_new = server.signal['mel']
            f = numpy.mean(mel_new[first:])
            print "calmness readings: " + str(mel_new[first:])
            print "Fitness of genome, " + indv + " is: " + str(f)
            self.fs[indv] = f

            if f > self.best_f:
                self.best = indv
                self.best_f = f

            if  f > bestpf:
                bestp = indv
                bestpf = f

        self.bests.append(bestp)
        self.av_f.append(np.mean(self.fs.values()))

    def roulette_wheel(self):
        max = sum(self.fs.values())

        pick = random.uniform(0,max)

        current = 0

        for indv in self.fs.keys():
            current += self.fs[indv]
            if current > pick:
                return indv


    def select(self):
        if self.s == 0:
            return self.roulette_wheel()

            


    def make_next_gen(self):
        self.eval_pop()
        new = []
        if self.e:
            new.append(self.bests[-1])
        while len(new) <= self.n:
            mum = self.select()
            dad = self.select()

            new +=  [self.mutate(x) for x in self.crossover(mum,dad)]
        self.pop = new

    def run(self,steps=100):
        self.init_pop()
        for i in range(steps):
            print "gen: ",i
            self.make_next_gen()
            print self.bests
            print self.best



class MuseServer(ServerThread):
    def __init__(self, port=4444):
        self.signal = {}
        self.signal['eeg'] = []
        self.signal['alpha_rel'] = []
        self.signal['conc'] = []
        self.signal['mel'] = []
        ServerThread.__init__(self, port)

    # receive accelrometer data
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):
        acc_x, acc_y, acc_z = args
        # print "%s %f %f %f" % (path, acc_x, acc_y, acc_z)

    # receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        self.signal['eeg'].append(args)

        # receive alpha relative data
    @make_method('/muse/elements/alpha_relative', 'ffff')
    def alpha_callback(self, path, args):
        self.signal['alpha_rel'].append(args)

    # receive alpha relative data
    @make_method('/muse/elements/experimental/concentration', 'f')
    def concentration_callback(self, path, args):
        self.signal['conc'].append(args[0])


    # receive mellow data - viewer is the same as concentration
    @make_method('/muse/elements/experimental/mellow', 'f')
    def mellow_callback(self, path, args):
        self.signal['mel'].append(args[0])
    # handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        test = args
        # print "Unknown message \n\t Source: '%s' \n\t Address: '%s' \n\t Types: '%s ' \n\t Payload: '%s'" %
        # (src.url, path, types, args)




#######Starting Server ################
try:
    server = MuseServer()
except ServerError, err:
    print str(err)
    sys.exit()
server.start()
print "MuseServer started on port 4444"


if __name__ == "__main__":
    bits = len(all_sounds)
    g = SA(n=14,p=bits) 
    g.run()
    plt.plot(g.av_f)
    plt.show()

