import random
from config import GENE_POOL
from calculations import calculate_slope

def genetic_algorithm(prices):
    population = [
        {'BUY_THRESHOLD': random.choice(GENE_POOL), 'SELL_THRESHOLD': random.choice(GENE_POOL)}
        for _ in range(10)
    ]

    def fitness(genes):
        slope = calculate_slope(prices)
        return abs(genes['BUY_THRESHOLD'] - slope) + abs(genes['SELL_THRESHOLD'] + slope)

    population = sorted(population, key=fitness)
    return population[0]
