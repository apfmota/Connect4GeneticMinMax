import random

import minMax

POPULATION_SIZE = 10
GENE_COUNT = 3

def create_random_chromosome():
    chromosome = []

    for i in range(GENE_COUNT):
        chromosome.append(random.uniform(-10, 10))

    return chromosome

def create_population():
    population = []

    for i in range(POPULATION_SIZE):
        population.append(create_random_chromosome())

    return population

def match(chromosome1, chromosome2):
    # Retorna vencedor
    pass

def tournament():
    pass

# population = create_population()
# print(population)

