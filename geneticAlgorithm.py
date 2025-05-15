import random

import minMax
import game

POPULATION_SIZE = 10
GENE_COUNT = 4
MIN_MAX_DEPTH = 4

JUDGE_COUNT = 10

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

def create_judges():
    judges = []

    for i in range(JUDGE_COUNT):
        judges.append(create_random_chromosome())

    return judges

def match(chromosome1, chromosome2):
    """
        Retorna 1 se o jogador 1 vencer, 2 se o jogador 2 vencer e 0 se empatar
    """
    g = game.Game(chromosome1, chromosome2, MIN_MAX_DEPTH)
    return g.play()

def fitness(chromosome, judges):
    victory_count = 0

    for judge in judges:
        # Inicia o jogo
        if match(chromosome, judge) == 1:
            print(f"venceu {judge} de brancas")
            victory_count += 1

        # Deixa o juiz comecar o jogo
        if match(judge, chromosome) == 2:
            print(f"venceu {judge} de pretas")
            victory_count += 1

    print(f"Total de vitórias: {victory_count}")

def tournament():
    pass

population = create_population()
judges = create_judges()
fitness(population[0], judges)

# print(match(population[0], judges[0]))

