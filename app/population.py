from app.chromosome import *


class Population:
    def __init__(self):
        self.__population = []

    @property
    def population(self):
        return self.__population

    def initialize(self, options, network):
        for _ in range(0, options['population_size']):
            c = Chromosome()
            c.initialise(network['number_of_nodes'])
            c.add_bias(options['number_of_biased_nodes'], network['adjacency_matrix'])
            self.__population.append(c)

    def evaluate(self, fitness_function, network):
        for c in self.__population:
            c.fitness = fitness_function(c.genes, network)

    def get_fittest_chromosome(self):
        fittest = self.__population[0]
        for current in self.__population:
            if current > fittest:
                fittest = current
        return fittest

    def select(self):
        population_size = len(self.__population)

        one = random.randint(0, population_size - 1)
        two = random.randint(0, population_size - 1)
        if self.__population[one].fitness > self.__population[two].fitness:
            return one
        else:
            return two

    def iterate_one_generation_standard(self, cost_function, network, options):
        new_population = []

        for _ in range(len(self.__population)):
            src = self.__population[self.select()]
            dest = self.__population[self.select()]
            off = src.crossover(dest)
            off.mutate(options['mutation_rate'])
            new_population.append(off)
        self.__population = new_population

        self.evaluate(cost_function, network)

    def iterate_one_generation_elitism(self, cost_function, network, options):
        new_population = [self.get_fittest_chromosome()]

        for _ in range(len(self.__population) - 1):
            src = self.__population[self.select()]
            dest = self.__population[self.select()]
            off = src.crossover(dest)
            off.mutate(options['mutation_rate'])
            new_population.append(off)
        self.__population = new_population

        self.evaluate(cost_function, network)

    def iterate_one_generation_steady_state(self, cost_function, network, options):
        self.__population = sorted(self.__population, key=lambda x: x.fitness, reverse=True)

        for _ in range(len(self.__population)):
            src = self.__population[self.select()]
            dest = self.__population[self.select()]
            off = src.crossover(dest)
            off.mutate(options['mutation_rate'])

            off.fitness = cost_function(off.genes, network)
            if off.fitness > self.__population[-1].fitness:
                self.__population[-1] = off

        self.evaluate(cost_function, network)
