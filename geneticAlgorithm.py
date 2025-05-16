import random

import minMax
import game

POPULATION_SIZE = 10
GENE_COUNT = 4
MIN_MAX_DEPTH = 4

JUDGE_COUNT = 3

class Chromosome:
    def __init__(self, genes):
        self.genes = genes
        self.total_wins = 0
        self.total_losses = 0
        self.total_draws = 0
        self.score = 0

    def __str__(self):
        return f"{self.genes}:\
               \n\tScore: {self.score}\
               \n\t{self.total_wins} Wins | {self.total_losses} Losses | {self.total_draws} Draws"

def create_random_chromosome():
    genes = []

    for i in range(GENE_COUNT):
        genes.append(random.uniform(-10, 10))

    return Chromosome(genes)

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
        Retorna: (vencedor, total de jogadas)

        vencedor: 1 se o jogador 1 vencer, 2 se o jogador 2 vencer e 0 se empatar
    """
    g = game.Game(chromosome1.genes, chromosome2.genes, MIN_MAX_DEPTH)
    return g.play()

def set_score(chromosome, winner, total_moves, player_number):
    if winner == 0:
        chromosome.total_draws += 1 # Empate
        return
    
    match_result = (25 - total_moves + 1) # adiciona 1 caso o jogador ganhe/perca no ultimo lance
    
    if winner == player_number:
        chromosome.total_wins += 1
        chromosome.score += match_result
    else:
        chromosome.total_losses += 1
        chromosome.score -= match_result

def fitness(chromosome, judges):
    for judge in judges:

        # Jogador inicia o jogo
        winner, total_moves = match(chromosome, judge)
        set_score(chromosome, winner, total_moves, 1)

        # Juiz inicia o jogo
        winner, total_moves = match(judge, chromosome)
        set_score(chromosome, winner, total_moves, 2)

def fitness_population(population, judges):
    for chromosome in population:
        fitness(chromosome, judges)
        print(chromosome)

def tournament():
    pass

def crossover(chromosome1, chromosome2):
    point = GENE_COUNT // 2
    child1 = Chromosome(chromosome1.genes[:point] + chromosome2.genes[point:GENE_COUNT])
    child2 = Chromosome(chromosome2.genes[:point] + chromosome1.genes[point:GENE_COUNT])

    return child1, child2

population = create_population()
judges = create_judges()

fitness_population(population, judges)

# score_sum = 0
# for i, subject in enumerate(population):
#     score = fitness(subject, judges)
#     print(f"score of {i}: {score}")
#     score_sum += score

# score_sum /= POPULATION_SIZE
# print(f"Average Score: {score_sum}")

# print(match(population[0], judges[0]))

