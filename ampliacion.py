import random

import requests
import numpy as np

n_genes = 384  # number of genes of the individual


def http_requests_fitness(chromosome):  # this function makes an http request in order to obtain the fitness value of an indivdual
    # funciones: test, alfa, easydc, pilar, alfa2
    real_url = "http://memento.evannai.inf.uc3m.es/age/alfa2?c="
    r = requests.get(real_url + chromosome)
    return float(r.text)


def create_individual():  # this function creates a random individual as a binary list with length of n_genes
    possibilities = ['0', 'H', 'F']
    individual = [random.choice(possibilities) for i in range(n_genes)]
    return individual


def create_population(n_individuals):  # this function create a random population with a total of n_individuals
    print("Creating population...")
    population = [create_individual() for i in range(n_individuals)]
    return population


def evaluate_population(population):
    print("Evaluating population...")
    fitness_list = []
    for i in range(len(population)):
        str_individual = "".join([str(_) for _ in population[i]])  # we transform the list that represents an individual into a string
        fitness_individual = http_requests_fitness(str_individual)
        fitness_list.append(fitness_individual)
    return fitness_list


def selection_tournaments(evaluated_population, fitness_list, n_participants):  # this funtion selects the best individuals through tournaments
    print("Selecting population...")
    selected_population = []
    for i in range(len(fitness_list)):  # as many iterations (tournaments) as individuals to create a new population of the same size
        selected_individual = -1
        fitness_selected = 100000
        for j in range(n_participants):
            participant = np.random.randint(0,len(fitness_list))  # random selection of an individual from the whole population
            fitness_participant = fitness_list[
                participant]  # fitness value of the selected individual for the tournament
            if (fitness_participant < fitness_selected):
                selected_individual = participant
                fitness_selected = fitness_participant
        selected_population.append(evaluated_population[selected_individual])
    return selected_population


def individuals_simple_crossing(selected_population):  # this function mix the genes of the individuals simulating the reproduction
    # print("Crossing population...")
    cross_population = []
    for i in range(0, n_individuals, 2):
        crossed_individual1 = selected_population[i][:192] + selected_population[i + 1][192:]  # first_part_ind1 + second_part_ind2
        crossed_individual2 = selected_population[i + 1][:192] + selected_population[i][192:]  # first_part_ind2 + second_part_ind1
        cross_population.append(crossed_individual1)
        cross_population.append(crossed_individual2)
    # selected_population = cross_population.copy()
    return cross_population


def individuals_uniform_crossing(selected_population):
    print("Crossing population...")
    cross_population = []
    for i in range(0, n_individuals, 2):
        new_individual1 = []
        new_individual2 = []
        for j in range(n_genes):
            gen_of_ind1 = np.random.choice([True, False], size=1, p=[0.5, 0.5])[0]
            if (gen_of_ind1):
                new_individual1.append(selected_population[i][j])
                new_individual2.append(selected_population[i + 1][j])
            else:
                new_individual1.append(selected_population[i + 1][j])
                new_individual2.append(selected_population[i][j])
        cross_population.append(new_individual1)
        cross_population.append(new_individual2)
    return cross_population


def mutation(mutation_rate, population):
    print("Mutating population...")
    for i in range(len(population)):
        for j in range(len(population[i])):
            gonna_mutate = np.random.choice([True, False], size=1, p=[mutation_rate, 1 - mutation_rate])[0]
            if gonna_mutate:
                if population[i][j] == '0':
                    population[i][j] = random.choice(['F','H'])
                elif population[i][j] == 'F':
                    population[i][j] = random.choice(['0','H'])
                else:
                    population[i][j] = random.choice(['0','F'])


if __name__ == '__main__':

    # setting the parameters
    n_individuals = 200
    current_generation = 0
    max_generations = 125
    n_participants = 20
    mutation_rate = 0.005

    # random inicialization of the population
    population = create_population(n_individuals)

    # buffers to store best individuals and fitness of the generation
    best_fitness = []
    best_individuals = []

    print("------------PARAMETROS-------------\n" +
          "individuos: " + str(n_individuals) + "\n" +
          "generaciones: " + str(max_generations) + "\n" +
          "participantes torneos: " + str(n_participants) + "\n" +
          "ratio de mutacion: " + str(mutation_rate) + "\n" +
          "-------------------------------------\n")

    while (current_generation < max_generations):
        print("----------------------------------------------\n" + "GENERATION Nº " + str(current_generation))

        # evaluation of the population
        fitness_list = evaluate_population(population).copy()

        # store of the best fitness of the generation
        best_fitness_generation = min(fitness_list)
        best_fitness.append(best_fitness_generation)

        # store of the best individual of the generation
        best_individual_index = fitness_list.index(best_fitness_generation)
        best_individual = population[best_individual_index]
        best_individuals.append(best_individual)

        # selection of the best individuals
        population = selection_tournaments(population, fitness_list, n_participants).copy()

        # crossing of the selected individuals
        population = individuals_uniform_crossing(population).copy()

        # mutation of the population
        mutation(mutation_rate, population)

        print("Best fitness: " + str(best_fitness_generation))
        best_individual_str = "".join([str(_) for _ in best_individual])
        print("Best individual: " + best_individual_str)

        current_generation = current_generation + 1

    print("\n----------------------------------------------\nBest value achieved: " + str(min(best_fitness)))
    the_best = best_individuals[best_fitness.index(min(best_fitness))]
    the_best_str = "".join([str(_) for _ in the_best])
    print("Best individual achieved: " + the_best_str +
          "\n----------------------------------------------\n" +
          "Analyzing stations...")

    stations_to_delete = []
    allGood = True
    counter = 0
    for i in range(24):
        allZero = True
        for j in range(16):
            if the_best[counter] != '0':
                allZero = False
            counter = counter+1
        if allZero == True:
            allGood = False
            print("Deleting station nº " + str(i) + "... (UNNECESSARY)")
            stations_to_delete.append(i)
    if allGood == True:
        print("EVERY STATION IS NECESSARY")
    else:
        print("UNNECESSARY STATIONS HAVE BEEN DELETED")
