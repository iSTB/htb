from sound import sample
import time
import random
import numpy as np
import os

import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

def convert(touch):
    to_send = []
    if len(touch) != 14:
        raise ValueError('touch not the right length. ' + str(len(touch)) +'instead of 8' ) 
    to_send.append(int(touch[0:2],2)) #left start
    to_send.append(int(touch[2:4],2)) #left stop
    to_send.append(int(touch[4:7],2)) #left freq 

    to_send.append(int(touch[7:9],2)) #right start
    to_send.append(int(touch[9:11],2)) #right stop
    to_send.append(int(touch[11:],2)) #right start
    

    return to_send



class player(object):

    def __init__(self):
        self.outputs = []
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default="127.0.0.1",
          help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=8000,
          help="The port the OSC server is listening on")
        args = parser.parse_args()
        self.client = udp_client.UDPClient(args.ip, args.port)        

    def play(self,genome):
        if len(self.outputs) > len(genome):
            raise ValueError('number of sound outputs does not match the size of the genome')


        ####play sound part of genome        
        for i in xrange(len(self.outputs)):
            if genome[i] == '1':
                self.outputs[i].play()
        
        ##### send touch########
        #touch = genome[len(self.outputs):]
        #self.send_message(convert(touch))
        
    def send_message(self,to_send):
        msg = osc_message_builder.OscMessageBuilder(address = "/filter")
        msg.add_arg(to_send)
        msg = msg.build()
        self.client.send(msg)
        time.sleep(1)        


    def add_sound(self,path):
        sound = sample(path)        
        self.outputs.append(sound)
        
    def add_vib(self,number):
        pass

if __name__=="__main__":

    print convert('11111111111111')
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
    p.play('111111111111111')


