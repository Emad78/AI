from random import randint, shuffle
import pandas as pd
AND = 0
OR = 1
XOR = 2
NAND = 3
NOR = 4
XNOR = 5
class Chromosome():
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0
    def calc_fitness(self, data):
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
def initial(length):
    p = []
    for i in range(length**2):
        new = []
        for j in range(length-1):
            new.append(randint(1, 6))
        p.append(Chromosome(new))
    return p

def crossover(generation):
    ## write code
    pass

def select(population):
    ## write code
    pass

def mutation(generation):
    ## write code
    pass

def calc_population_fitness(population, data):
    for it in population:
        it.calc_fitness(data)

file_name = input("Enter file name: ")
data = pd.read_csv(file_name)
length = len(data.columns)-1
population = initial(length)

for i in range(2**length):
    generation = select(population)
    population = []
    population += crossover(generation)
    population += mutation(generation)
    calc_population_fitness(population, data)
    population.sort(key=lambda x: x.fitness)

    if(population[-1].fitness == 2**length):
        print(population[0].genes)
        break