from random import randint, shuffle
from time import time
import pandas as pd
AND = 0
OR = 1
XOR = 2
NAND = 3
NOR = 4
XNOR = 5
PM = 0.9
PC = 0.94

def prob(p):
    r = randint(1,10000)
    r = r / 10000
    if r<p:
        return True
    return False

class Chromosome():
    fitness_table = {}
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0
        self.key = ''
        for it in self.genes:
            self.key = self.key + str(it)
    def calc_fitness(self, data):
        if self.key in self.fitness_table.keys() :
            self.fitness = self.fitness_table[self.key]
            return
        fitness = 0
        for index, row in data.iterrows():
            output = row["Input1"]
            for i in range(len(self.genes)):
                input = row["Input"+str(i+2)]
                if self.genes[i] == AND:
                    output = input & output
                elif self.genes[i] == OR:
                    output = input | output                    
                elif self.genes[i] == XOR:
                    output = input ^ output
                elif self.genes[i] == NAND:
                    output = not(input & output)
                elif self.genes[i] == NOR:
                    output = not(input | output)
                elif self.genes[i] == XNOR:
                    output = not(input ^ output)
            if output == row["Output"]:
                fitness+=1
        self.fitness = fitness
        self.fitness_table[self.key] = self.fitness

    def mutation(self):
        g = randint(0, len(self.genes) - 1)
        self.genes[g] = randint(0, 5)
    
    def crossover(self, p1, p2):
        for i in range(len(self.genes)):
            if prob(.5):
                self.genes[i] = p1.genes[i]
            else:
                self.genes[i] = p2.genes[i]

    def write(self):
        for i in range(len(self.genes)):
            print(str(i+1)+" gate --> ", end='')
            if self.genes[i] == AND:
                print("AND")
            elif self.genes[i] == OR:
                 print("OR")                    
            elif self.genes[i] == XOR:
                 print("XOR")
            elif self.genes[i] == NAND:
                 print("NAND")
            elif self.genes[i] == NOR:
                 print("NOR")
            elif self.genes[i] == XNOR:
                 print("XNOR")
            print()
            

def initial(length):
    p = []
    for i in range(2*(length**2)):
        new = []
        for j in range(length-1):
            new.append(randint(0, 5))
        p.append(Chromosome(new))
    return p

def crossover(generation, pc):
    p = []
    for i in range(len(generation) - 1):
        if(prob(pc)):
            new = Chromosome(len(generation[i].genes)*[-1])
            new.crossover(generation[i], generation[i - 1])
            p.append(new)
        else:
            p.append(Chromosome(generation[i].genes[:]))
            p.append(Chromosome(generation[i - 1].genes[:]))
    return p

def select(population, length):
    return population[:length**2]
    l = []
    p = []
    le = len(population)
    for i in range(le):
        l += (le- i) * [i]
    for i in range(length ** 2):
        index = randint(0, le-1)
        p.append(population[index])
    return p

def mutation(population, pm):
    p = []
    for it in population:
        if(prob(pm)):
            new = Chromosome(it.genes)
            new.mutation()
            p.append(new)
    return p

def calc_population_fitness(population, data):
    for it in population:
        it.calc_fitness(data)

def copy(c1, c2):
    c1.genes = c2.genes[:]
    c1.fitness = c2.fitness
    c1.key = c2.key
s = time()
file_name = input("Enter file name: ")
data = pd.read_csv(file_name)
s = time()
length = len(data.columns)-1

population = initial(length)
pm = 0.62
pc = 0.94
result = Chromosome((length-1) * [0])
k = 0
for i in range(length**2):
    generation = select(population, length)
    population = []
    shuffle(generation)
    population += crossover(generation, pc)
    population += mutation(population, 1 - pm)
    pm = pm * PM
    pc = pc * PC
    calc_population_fitness(population, data)
    population.sort(key=lambda x: x.fitness, reverse=True)
    k = i + 1
    if(population[0].fitness > result.fitness):
        copy(result, population[0])
    if(result.fitness == 2**length):
        break
result.write()
print(k)
print(result.fitness)
print(time() - s)