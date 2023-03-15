import random
import numpy as np


def create_offspring(parent1, parent2):
    return parent1, parent2

# ------------------- Pseudocode ------------------- #


def fitness_proportionate_selection(population, n):
    new_population = []
    fitness_values = [individual.fitness for individual in population]

    for _ in range(n):
        # choose n individuals with their respective fitness being the probability of being chosen
        new_population.append(random.choice(population, p=fitness_values))

    return new_population


def get_difference(matrix1, matrix2):
    # get how different two matrices are from each other
    return np.sum(np.abs(matrix1 - matrix2))


def tournament(parent1, parent2, offspring1, offspring2):
    population = []
    d1, d2, d3, d4 = get_difference(parent1, offspring1), get_difference(
        parent1, offspring2), get_difference(parent2, offspring1), get_difference(parent2, offspring2)
    if d1 + d2 < d3 + d4:
        if parent1.fitness > offspring1.fitness:
            population.append(parent1)
        else:
            population.append(offspring1)
        if parent2.fitness > offspring2.fitness:
            population.append(parent2)
        else:
            population.append(offspring2)
    else:
        if parent1.fitness > offspring2.fitness:
            population.append(parent1)
        else:
            population.append(offspring2)
        if parent2.fitness > offspring1.fitness:
            population.append(parent2)
        else:
            population.append(offspring1)

    return population


def crowding_selection(parents):
    population = []
    random.shuffle(parents)
    for parent1, parent2 in zip(parents[::2], parents[1::2]):
        offspring1, offspring2 = create_offspring(
            parent1, parent2)
        population += tournament(parent1, parent2,
                                 offspring1, offspring2)
    return population
