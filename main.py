import requests
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt

n_genes = 384 # number of genes of the individual

def http_requests_fitness(chromosome): # this function makes an http request in order to obtain the fitness value of an indivdual
    # funcion real: alfa?c=
    url = "http://memento.evannai.inf.uc3m.es/age/test?c="
    real_url = "http://memento.evannai.inf.uc3m.es/age/alfa?c="
    r = requests.get(real_url + chromosome)
    return float(r.text)


def create_individual(): # this function creates a random individual as a binary list with length of n_genes
    individual = [np.random.randint(0,2) for i in range(n_genes)]
    str_individual = "".join([str(_) for _ in individual])
    return individual

def create_population(n_individuals): # this function create a random population with a total of n_individuals
    # print("Creating population...")
    population = [create_individual() for i in range(n_individuals)]
    return population


def evaluate_population(population):
   # print("Evaluating population...")
    fitness_list = []
    for i in range(len(population)):
        str_individual = "".join([str(_) for _ in population[i]])  # we transform the list that represents an individual into a string
        fitness_individual = http_requests_fitness(str_individual)
        fitness_list.append(fitness_individual)
    return fitness_list



def selection_tournaments(evaluated_population, fitness_list, n_participants): # this funtion selects the best individuals through tournaments
   # print("Selecting population...")
    selected_population = []
    for i in range (len(fitness_list)): # as many iterations (tournaments) as individuals to create a new population of the same size
        selected_individual = -1
        fitness_selected = 100000
        for j in range (n_participants):
            participant = np.random.randint(0,len(fitness_list))  # random selection of an individual from the whole population
            fitness_participant = fitness_list[participant]  # fitness value of the selected individual for the tournament
            if (fitness_participant < fitness_selected):
                selected_individual = participant
                fitness_selected = fitness_participant
        selected_population.append(evaluated_population[selected_individual])
    # evaluated_population = selected_population.copy()
    return selected_population

def individuals_simple_crossing(selected_population): # this function mix the genes of the individuals simulating the reproduction
   # print("Crossing population...")
    cross_population = []
    for i in range (0, n_individuals, 2):
        crossed_individual1 = selected_population[i][:192] + selected_population[i+1][192:] # first_part_ind1 + second_part_ind2
        crossed_individual2 = selected_population[i+1][:192] + selected_population[i][192:] # first_part_ind2 + second_part_ind1
        cross_population.append(crossed_individual1)
        cross_population.append(crossed_individual2)
    # selected_population = cross_population.copy()
    return cross_population

def individuals_uniform_crossing(selected_population):
    cross_population = []
    for i in range(0, n_individuals, 2):
        new_individual1 = []
        new_individual2 = []
        for j in range (n_genes):
            gen_of_ind1 = np.random.choice([True, False], size=1, p=[0.5, 0.5])[0]
            if (gen_of_ind1):
                new_individual1.append(selected_population[i][j])
                new_individual2.append(selected_population[i+1][j])
            else:
                new_individual1.append(selected_population[i+1][j])
                new_individual2.append(selected_population[i][j])
        cross_population.append(new_individual1)
        cross_population.append(new_individual2)
    return cross_population



def mutation(mutation_rate, population):
   # print("Mutating population...")
    for i in range(len(population)):
        for j in range(len(population[i])):
            gonna_mutate = np.random.choice([True, False], size=1, p=[mutation_rate, 1 - mutation_rate])[0]
            if gonna_mutate:
                if population[i][j] == 1:
                    population[i][j] = 0
                else:
                    population[i][j] = 1



if __name__ == '__main__':

    # random inicialization of the population
    n_individuals = 200
    current_generation = 0
    max_generations = 125
    n_participants = 20
    mutation_rate = 0.005
    population = create_population(n_individuals)
    best_fitness = []
    print("------------PARAMETROS-------------\n" +
          "individuos: " + str(n_individuals) + "\n" +
          "generaciones: " + str(max_generations) + "\n" +
          "participantes torneos: " + str(n_participants) + "\n" +
          "ratio de mutacion: " + str(mutation_rate) + "\n" +
          "-------------------------------------\n")

    while (current_generation < max_generations):
       # print("----------------------------------------------\n" + "GENERATION Nº " + str(current_generation))

        # evaluation of the population
        fitness_list = evaluate_population(population).copy()
        best_fitness_generation = min(fitness_list)
        best_fitness.append(best_fitness_generation)
        print(str(best_fitness_generation))

        # selection of the best individuals

        population = selection_tournaments(population, fitness_list, n_participants).copy()

        # crossing of the selected individuals
        population = individuals_uniform_crossing(population).copy()

        # mutation of the population

        mutation(mutation_rate, population)

        current_generation = current_generation + 1
    print("Best value achieved: " + str(min(best_fitness)))