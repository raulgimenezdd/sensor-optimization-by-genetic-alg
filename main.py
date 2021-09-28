import requests
import numpy as np
import random

def http_requests_fitness(self, chromosome):
    url = "http://memento.evannai.inf.uc3m.es/age/test?c="
    r = requests.get(url + chromosome)
    print("Valor de adecuacion: " + r.text)
    return r

def create_individual(): # this function creates a random individual as a binary list with length of 384
    individual = [np.random.randint(0,2) for i in range(384)]
    str_individual = "".join([str(_) for _ in individual])
    return individual

def create_population(n_individuals): # this function create a random population with a total of n_individuals
    population = [create_individual() for i in range(n_individuals)]
    return population

def evaluate_population(population): # this function gives a fitness value to each individual
    for i in range (len(population)):
        str_individual = "".join([str(_) for _ in population[i]]) # we transform the list that represents an individual into a string
        fitness_part1 = http_requests_fitness(str_individual[0:63]) # we divided the string into 6 parts of 64 genes in order to use the function http_requests_fitness
        fitness_part2 = http_requests_fitness(str_individual[64:127])
        fitness_part3 = http_requests_fitness(str_individual[128:191])
        fitness_part4 = http_requests_fitness(str_individual[192:255])
        fitness_part5 = http_requests_fitness(str_individual[256:319])
        fitness_part6 = http_requests_fitness(str_individual[320:383])
        real_fitness = fitness_part1 + fitness_part2 + fitness_part3 + fitness_part4 + fitness_part5 + fitness_part6 # the real value of fitness is the sum of the parts
        population[i].append(real_fitness)
        '''
        implementar aqui la condicion de parada 
        '''

def selection_tournaments(evaluated_population, n_participants):
    selected_population = []
    for j in range (len(evaluated_population)): # as many iterations (tournaments) as individuals to create a new population of the same size
        selected_individual = -1
        fitness_selected = -1
        for i in range (n_participants):
            participant = np.random.randint(0, len(evaluated_population))  # random selection of an individual from the whole population
            fitness_participant = evaluated_population[participant][-1]  # fitness value of the selected individual for the tournament
            if fitness_participant > fitness_selected:
                selected_individual = participant
                fitness_selected = fitness_participant
        selected_population.append(evaluated_population[selected_individual])
    evaluated_population = selected_population.copy()
    for i in range (len(evaluated_population)): # elimination of the fitness value of each individual from his corresponding list
        evaluated_population[i].pop()

'''
def individuals_crossing(selected_population):
'''


if __name__ == '__main__':

    # random inicialization of the population
    n_individuals = 20
    population = create_population(n_individuals)

    # evaluation of the population
    evaluate_population(population)

    # selection of the best individuals
    n_participants = 4
    selection_tournaments(population, n_participants)