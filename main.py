import requests
import numpy as np
import random

n_genes = 64

def http_requests_fitness(chromosome):
    # funcion real: alfa?c=
    url = "http://memento.evannai.inf.uc3m.es/age/test?c="
    r = requests.get(url + chromosome)
    return float(r.text)

def create_individual(): # this function creates a random individual as a binary list with length of 384
    individual = [np.random.randint(0,2) for i in range(n_genes)]
    str_individual = "".join([str(_) for _ in individual])
    return individual

def create_population(n_individuals): # this function create a random population with a total of n_individuals
    population = [create_individual() for i in range(n_individuals)]
    return population

def evaluate_population(population): # this function gives a fitness value to each individual
    for i in range(len(population)):
        str_individual = "".join([str(_) for _ in population[i]])  # we transform the list that represents an individual into a string
        fitness = http_requests_fitness(str_individual)
        population[i].append(fitness)
        # condicion de parada aqui



def selection_tournaments(evaluated_population, n_participants):
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
    evaluated_population = selected_population.copy()
    for i in range (len(evaluated_population)): # elimination of the fitness value of each individual from his corresponding list
        evaluated_population[i].pop()
    print(evaluated_population)

def individuals_crossing(selected_population):
    cross_population = []



if __name__ == '__main__':

    # random inicialization of the population
    n_individuals = 5
    population = create_population(n_individuals)

    # evaluation of the population
    evaluate_population(population)

    # selection of the best individuals
    n_participants = 5
    selection_tournaments(population, n_participants)