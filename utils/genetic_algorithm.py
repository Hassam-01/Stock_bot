import random
from config import GENE_POOL
from calculations import calculate_slope

def genetic_algorithm(prices, generations=50, population_size=20, mutation_rate=0.1):
    if not GENE_POOL:
        raise ValueError("GENE_POOL cannot be empty.")
    if len(prices) < 2:
        raise ValueError("Prices must have at least two data points to calculate slope.")

    # Initialize population
    population = [
        {'BUY_THRESHOLD': random.choice(GENE_POOL), 'SELL_THRESHOLD': random.choice(GENE_POOL)}
        for _ in range(population_size)
    ]

    def fitness(genes):
        # Evaluate genes based on trading profit
        profit = 0
        for i in range(len(prices) - 1):
            if prices[i + 1] > prices[i] + genes['BUY_THRESHOLD']:
                profit += prices[i + 1] - prices[i]
            elif prices[i + 1] < prices[i] - genes['SELL_THRESHOLD']:
                profit -= prices[i + 1] - prices[i]
        return -profit  # Minimize negative profit (maximize actual profit)

    best_fitness = []

    for generation in range(generations):
        # Sort the population by fitness (ascending order, as lower fitness is better)
        population = sorted(population, key=fitness)
        best_fitness.append(fitness(population[0]))
        print(f"Generation {generation}: Best fitness = {-best_fitness[-1]}")  # Report positive profit

        # Select the top 50% of individuals for breeding
        top_individuals = population[:len(population) // 2]

        # Create next generation (offspring)
        offspring = []
        for _ in range(len(population) - len(top_individuals)):
            parent1, parent2 = random.sample(top_individuals, 2)
            child = {
                'BUY_THRESHOLD': random.choice([parent1['BUY_THRESHOLD'], parent2['BUY_THRESHOLD']]),
                'SELL_THRESHOLD': random.choice([parent1['SELL_THRESHOLD'], parent2['SELL_THRESHOLD']])
            }

            # Apply adaptive mutation
            adaptive_mutation_rate = mutation_rate * (1 - generation / generations)
            if random.random() < adaptive_mutation_rate:
                child['BUY_THRESHOLD'] = random.choice(GENE_POOL)
            if random.random() < adaptive_mutation_rate:
                child['SELL_THRESHOLD'] = random.choice(GENE_POOL)

            offspring.append(child)

        # Combine top individuals and offspring to form new population
        population = top_individuals + offspring

    # Return the best individual and their fitness score
    best_individual = population[0]
    return best_individual, -fitness(best_individual)
