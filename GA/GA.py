iimport random
import numpy as np
import matplotlib.pyplot as plt


def all_ones(indv):
    return indv.count('1')



class GA(object):

    def __init__(self,func = all_ones,n=10,p=16,mu=0.1,s=0,e=False):
        """
        n: number of indvs
        p: number of bits for each indv
        mu: mutation rate
        s: selction type: 0 = roullete whel
        e: eleitism.
        """ 

        self.func = func
        self.n = n
        self.p = p
        self.mu = mu
        self.s = s
        self.e = e


        self.pop = [] #current pop go here
        self.best = '' #stores best overall indivdual
        self.bests = [] #stores best individual from each gen
        self.best_f = -float('inf') #the fittness of the best overal indivdual

        self.av_f = [] #stores the average fitness of each population


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
            f = self.func(indv)
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


if __name__ == "__main__":
    g = GA(e=True) 
    g.run()
    plt.plot(g.av_f)
    plt.show()

