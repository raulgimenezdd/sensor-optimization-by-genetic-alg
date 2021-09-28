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

def evaluate_population(population):
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





if __name__ == '__main__':
    n_individuals = 20
    initial_pop = create_population(n_individuals)
    evaluate_population(initial_pop)