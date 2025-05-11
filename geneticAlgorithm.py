import random

import minMax
import game

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
    game = game.Game(chromosome1, chromosome2, 10)
    return game.play() #retorna 1 se o jogador 1 vencer, 2 se o jogador 2 vencer e 0 se empatar

def tournament():
    pass

# population = create_population()
# print(population)

