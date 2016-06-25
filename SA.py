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

low = "./sounds/LOW FREQ"
mid = "./sounds/MID FREQ"
high = "./sounds/HIGH FREQ"


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
        self.fs = {}
        bestp = ''
        bestpf = -float('inf')
        for indv in self.pop:
            server.singal['mel']
            self.player.play(indv)
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


    def get_good_schemata(self):
        meanf = np.mean([s.fit for s in self.schemata])
        meano = np.mean([s.get_order() for s in selfschemata])

        self.good = [s for s in self.schemata if s.get_order() >= meano and s.fit >= meanfit]
    
            


    def make_next_gen(self):
        self.eval_pop()
        self.schemata = sx.complete(self.pop)
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












try:
    server = MuseServer()
except ServerError, err:
    print str(err)
    sys.exit()
server.start()

import time
if __name__ == "__main__":
   # io_udp = MuseIOOSC()
   # io_udp.starit()
    while True:
        time.sleep(5)
        print server.signal['conc']



'''
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server


def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    print("EEG (uV) per channel: ", ch1, ch2, ch3, ch4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=4444,
                        help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    #dispatcher.map("/debug", print)
    dispatcher.map("/muse/eeg", eeg_handler, "EEG")

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
'''

#if __name__ == "__main__":
#    g = SA(e=True) 
#    g.run()
#    plt.plot(g.av_f)
#    plt.show()

