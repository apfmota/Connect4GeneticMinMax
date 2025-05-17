import random
import matplotlib.pyplot as plt
import minMax
import game

POPULATION_SIZE = 20
GENE_COUNT = 4

ELITISM = 2 # Quantos melhores elementos continuam na proxima geracao
TOURNAMENT_SIZE = 4
TOURNAMENTS_PER_GEN = 3
MIN_MAX_DEPTH = 3
RANDOMS_WITH_CROSSOVER = 10
RANDOMS = 2

DEFAULT_JUDGE = [0, 0, 1, 0]

TOTAL_GENERATIONS = 10

MUTATION_RATE = 2 # 2% dos genes irão se alterar

JUDGE_COUNT = 3

avg_score = []
best_score = []

class Chromosome:
    def __init__(self, genes):
        self.genes = genes
        self.total_wins = 0
        self.total_losses = 0
        self.total_draws = 0
        self.score = 0

    def reset_metrics(self):
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

def fitness_population(population, judges, populationNumber):
    score_sum = 0
    for chromosome in population:
        fitness(chromosome, judges)
        print(chromosome)
        score_sum += chromosome.score

    population.sort(key=lambda chr: chr.score)
    avg_score.append(score_sum / POPULATION_SIZE)
    best_score.append(population[-1].score)

    game.Game(population[-1].genes, DEFAULT_JUDGE, MIN_MAX_DEPTH, True, f"output_{populationNumber}.gif").play()

    print(f"\n - Average Score: {score_sum / POPULATION_SIZE}")
    print(f"\n - Highest Score: {population[-1].score}")

def tournament():
    participants = []
    for i in range(TOURNAMENT_SIZE):
        aux = random.randint(0, POPULATION_SIZE - 1)
        if participants.__contains__(aux):
            i -= 1
        else:
            participants.append(aux)

    participants = sorted(participants)
    return participants[-1], participants[-2]

def mutation(chromosome):
    for g in chromosome.genes:
        if random.randint(1, 100) <= MUTATION_RATE:
            op = random.randint(1, 2)
            if op == 1:
                g += 1
            else:
                g -= 1
            g = min(max(g, -10), 10)

def crossover(chromosome1, chromosome2):
    point = GENE_COUNT // 2
    child1 = Chromosome(chromosome1.genes[:point] + chromosome2.genes[point:GENE_COUNT])
    child2 = Chromosome(chromosome2.genes[:point] + chromosome1.genes[point:GENE_COUNT])

    mutation(child1)
    mutation(child2)

    return [child1, child2]

def make_next_generation(population, judges, populationNumber):
    fitness_population(population, judges, populationNumber)

    for p in population:
        p.reset_metrics()

    new_population = []
    for i in range(TOURNAMENTS_PER_GEN):
        c1, c2 = tournament()
        new_population.extend(crossover(population[c1], population[c2]))

    # Adiciona N individuso aleatorios fazendo crossover com os N melhores
    for i in range(RANDOMS_WITH_CROSSOVER):
        new_population.extend(crossover(create_random_chromosome(), population[-i]))

    # Adiciona N individuos aleatorios
    for i in range(RANDOMS):
        new_population.append(create_random_chromosome())

    new_population.extend(population[-ELITISM:])
    return new_population


def plot_chart(data, name, metric_name):
    # Separa os pontos em listas de x e y
    x = list(range(1, len(data) + 1))
    y = data
    
    # Cria o gráfico
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, marker='o', linestyle='-', color='blue')
    plt.title(name)
    plt.xlabel('Geração')
    plt.ylabel(metric_name)
    plt.grid(True)
    plt.show()

population = create_population()
judges = create_judges()

for i in range(TOTAL_GENERATIONS):
    print(f"---------\n{i + 1} Generation\n---------")
    population = make_next_generation(population, judges, i + 1)

plot_chart(avg_score, "Score Médio do fitness por geração", "Score")
plot_chart(best_score, "Melhor score do fitness por geração", "Score")

