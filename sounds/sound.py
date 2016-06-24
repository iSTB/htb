import subprocess
import os
import time
class sample(object):
    
    def __init__(self,path,buffer_size=1024):
        self.path = path
        
        self.devnull = open(os.devnull, 'wb') 
        """
        #Loading sounds
        #print "Loading sound: " + path + "..."
        
        #self.f = waveOpen(self.path,'rb') 
        #self.frame_rate = self.f.getframerate()
        #self.frames = self.f.getnframes()
        #self.channels = self.f.getnchannels()      
        print "Frame rate=" + str(self.frame_rate)
        print "Number of channels = " + str(self.channels) 

        self.width = self.f.getsampwidth()

        #Loading player
        print "Making player..."

        p = pyaudio.PyAudio()

        self.stream = p.open(format=p.get_format_from_width(self.width),
        channels=self.channels,
        rate=self.frame_rate,
        output=True,
        stream_callback=self.callback,
        start =False)

        #self.sound_out = alsaaudio.PCM() 
        #self.sound_out.setchannels(self.channels)
        #self.sound_out.setrate(self.frame_rate)
        #self.sound_out.setperiodsize(buffer_size) 
    

        #if self.width == 1:
        #   self.sound_out.setformat(alsaaudio.PCM_FORMAT_U8)
        # Otherwise we assume signed data, little endian
        #elif self.width == 2:
        #   self.sound_out.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        #elif self.width == 3:
        #   self.sound_out.setformat(alsaaudio.PCM_FORMAT_S24_LE)
        #elif self.width == 4:
        #   self.sound_out.setformat(alsaaudio.PCM_FORMAT_S32_LE)
        #else:
        #   raise ValueError('Unsupported format')

        self.sound = self.f.readframes(self.frames)
        #self.f.close()

    def callback(self, in_data, frame_count, time_info, status):
        data = self.f.readframes(frame_count)
        return (data, pyaudio.paContinue)
    """ 
    def play(self):
        # print self.path
       # p = subprocess.Popen(['mpg123','-q',self.path])     
        time.sleep(0.05)
        p = subprocess.Popen(['mpg123','-q',self.path], shell=False,
              stdout=subprocess.PIPE, stderr=self.devnull)



if __name__ == "__main__":
    s = sample('100.mp3')
    s.play()

