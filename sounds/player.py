from sound import sample
import time
import random
import numpy as np
import os

class player(object):

    def __init__(self):
        self.outputs = []
        

    def play(self,genome):
        if len(self.outputs) != len(genome):
            raise ValueError('number of outputs does not match the size of the genome')
        
        for i in xrange(len(self.outputs)):
            if genome[i] == '1':
                self.outputs[i].play()

        print genome        
    def add_sound(self,path):
        sound = sample(path)        
        self.outputs.append(sound)
        



if __name__=="__main__":

    p = player()
    '''
    conf_path = './Sounds/DRONE SOUNDS/Confident'
    rel_path = './Sounds/DRONE SOUNDS/Relaxed'
    fear_path = './Sounds/DRONE SOUNDS/Fearful'

    conf_sounds = [conf_path + '/' + x for x in os.listdir(conf_path)]
    rel_sounds = [rel_path + '/' + x for x in os.listdir(rel_path)]
    fear_sounds = [fear_path + '/' + x for x in os.listdir(fear_path)]
    
    all_sounds = conf_sounds + rel_sounds + fear_sounds

    for i,sound in enumerate(all_sounds):
        p.add_sound(i,sound) 

    n_sounds = len(all_sounds)

    print "Number of sounds:", n_sounds    
    '''



    p.add_sound('100.mp3')
    p.play('1')


