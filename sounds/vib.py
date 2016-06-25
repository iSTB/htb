import subprocess 





class vib(object):


    def __init__(self,name):





    def play(self):
        p = subprocess.Popen(['vib','0', '10'], shell=False,
            stdout=subprocess.PIPE, stderr=self.devnull)





