import requests
import numpy as np
import random

n_genes = 64 # number of genes of the individual

def http_requests_fitness(chromosome): # this function makes an http request in order to obtain the fitness value of an indivdual
    # funcion real: alfa?c=
    url = "http://memento.evannai.inf.uc3m.es/age/test?c="
    r = requests.get(url + chromosome)
    return float(r.text)

def create_individual(): # this function creates a random individual as a binary list with length of n_genes
    individual = [np.random.randint(0,2) for i in range(n_genes)]
    str_individual = "".join([str(_) for _ in individual])
    return individual

def create_population(n_individuals): # this function create a random population with a total of n_individuals
    population = [create_individual() for i in range(n_individuals)]
    return population

def evaluate_population(population): # this function gives a fitness value to each individual
    min_fitness = 100000
    for i in range(len(population)):
        str_individual = "".join([str(_) for _ in population[i]])  # we transform the list that represents an individual into a string
        fitness = http_requests_fitness(str_individual)
        population[i].append(fitness)
        if fitness < min_fitness: # we store the minimum fitness value obtained
            min_fitness = fitness
        # condicion de parada aqui

def selection_tournaments(evaluated_population, n_participants): # this funtion selects the best individuals through tournaments
    selected_population = []
    for j in range (len(evaluated_population)): # as many iterations (tournaments) as individuals to create a new population of the same size
        selected_individual = -1
        fitness_selected = 100000
        for i in range (n_participants):
            participant = np.random.randint(0, len(evaluated_population))  # random selection of an individual from the whole population
            fitness_participant = evaluated_population[participant][-1]  # fitness value of the selected individual for the tournament
            if fitness_participant < fitness_selected:
                selected_individual = participant
                fitness_selected = fitness_participant
        selected_population.append(evaluated_population[selected_individual])
        '''
        AQUI HAY ERRORES 
        '''
        cleaned_population = []
        a = len(selected_population)
        for x in range(len(selected_population)):  # elimination of the fitness value of each individual from his corresponding list
            # evaluated_population[x].pop()
            cleaned_population.append(selected_population[x][:65])
        evaluated_population = cleaned_population.copy()


def individuals_crossing(selected_population): # this function mix the genes of the individuals simulating the reproduction
    cross_population = []
    for i in range (0, n_genes, 2):
        crossed_individual1 = selected_population[i][:32] + selected_population[i+1][32:] # first_part_ind1 + second_part_ind2
        crossed_individual2 = selected_population[i+1][:32] + selected_population[i][32:] # first_part_ind2 + second_part_ind1
        cross_population.append(crossed_individual1)
        cross_population.append(crossed_individual2)
    selected_population = cross_population.copy()

def mutation(mutation_rate, population):
    for i in range(len(population)):
        for j in range(len(population[i])):
            gonna_mutate = np.random.choice([True, False], size=1, p=[mutation_rate, mutation_rate - 1])[0]
            if gonna_mutate:
                if population[i][j] == 1:
                    population[i][j] = 0
                else:
                    population[i][j] = 1

if __name__ == '__main__':

    # random inicialization of the population
    n_individuals = 5
    population = create_population(n_individuals)

    n_iterations = 0
    max_iterations = 100
    while (n_iterations < max_iterations):
        # evaluation of the population
        evaluate_population(population) # esto lo hace bien

        # selection of the best individuals
        n_participants = 2
        selection_tournaments(population, n_participants)

        # crossing of the selected individuals
        individuals_crossing(population)

        # mutation of the population
        mutation_rate = 0.02
        mutation(mutation_rate, population)

        n_iterations = n_iterations + 1