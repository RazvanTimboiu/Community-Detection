import random
from utilitary import normalize


class Chromosome:
    def __init__(self):
        self.__genes = []
        self.__fitness = 0.0

    @property
    def genes(self):
        return self.__genes

    @genes.setter
    def genes(self, genes=None):
        self.__genes = genes

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, fitness=None):
        self.__fitness = fitness

    def get_community_count(self):
        return len(set(self.__genes))

    def initialise(self, size):
        self.__genes = [random.randint(0, size-1) for _ in range(size)]

    def normalize(self):
        self.__genes = normalize(self.__genes)

    def crossover(self, other):
        offspring = Chromosome()
        chosen_community = random.choice(self.__genes)
        offspring.genes = [source if source == chosen_community else destination for source, destination in zip(self.genes, other.genes)]
        offspring.normalize()
        return offspring

    def mutate(self, mutation_rate):
        chance = random.randint(0, 100)
        if chance < mutation_rate:
            first = random.randint(0, len(self.__genes) - 1)
            second = random.randint(0, len(self.__genes) - 1)
            self.__genes[first], self.__genes[second] = self.__genes[second], self.__genes[first]
            self.normalize()

    def add_bias(self, amount, adjacency):
        for _ in range(0, amount):
            chosen = random.randint(0, len(self.__genes) - 1)
            value = self.__genes[chosen]

            for i in range(0, len(self.__genes)):
                if adjacency[i][chosen] == 1:
                    self.__genes[i] = value
        self.normalize()

    def __gt__(self, other):
        if self.fitness > other.fitness:
            return True
        else:
            return False

    def __str__(self):
        return 'Chromosome' + str(set(self.__genes)) + ' has fitness: ' + str(self.__fitness) + '\n'
