import random
import numpy as np
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import pairwise_distances


class Polynomial:
    def __init__(self, parameters):
        self.params = parameters

    def get_value(self, x):
        return np.add(
            np.add(pow(x, 3)*self.params[0], pow(x, 2)*self.params[1]),
            np.add(x*self.params[2], self.params[3]))

    def change_param(self, position, value):
        self.params[position] += value


class Individual:
    def __init__(self, params=None):
        if params is not None:
            self.polynomial = Polynomial(params)
        else:
            self.polynomial = Polynomial(np.array([random.uniform(-10.0, 10.0), random.uniform(-10.0, 10.0),
                                                   random.uniform(-10.0, 10.0), random.uniform(-10.0, 10.0)]))

    def calc_fitness(self, points):
        flat_distances = (points[:, 1] - self.polynomial.get_value(points[:, 0]))
        classification_distances = flat_distances * points[:, 2].transpose()
        fitness = 0
        for i in range(0, classification_distances.shape[0]):
            if classification_distances[i] > 0:
                fitness += 1
        return fitness/points.shape[0]


class Population:
    def __init__(self, pop):
        """create population of polynomials

        :param pop: (int)Number of individuals in population

        """
        self.generation = 0
        self.population = []
        for i in range(0, pop):
            new_individual = Individual()
            self.population.append(new_individual)

    def get_pop(self):
        return len(self.population)

    def get_generation(self):
        return self.generation

    def get_bestfit(self, points):
        best_fit = 0.0
        for individual in self.population:
            fit = individual.calc_fitness(points)
            if fit > best_fit:
                best_fit = fit
        return best_fit

    def get_avgfit(self, points):
        fitness_sum = 0.0
        for individual in self.population:
            fitness_sum += individual.calc_fitness(points)
        return fitness_sum/len(self.population)

    def get_fitness_vector(self, points):
        fitness_list = []
        for individual in self.population:
            fitness_list.append(individual.calc_fitness(points))
        return np.asarray(fitness_list)

    def poly_params_vector(self):
        poly_vector = []
        for individual in self.population:
            poly_vector.append(individual.polynomial.params)
        return poly_vector

    def calc_probabilities(self, points):
        """ calculates list of probabilities depending on the fitness

        :param points: (x, y, class) Numpy matrix of points belonging to two classes {-1, 1}
        :return list of probabilities (sums to 1) of choosing individual for crossover
        """
        probability_list = []
        fitness_sum = 0
        # calculate fitnesses for individuals
        for individual in self.population:
            probability_list.append(individual.calc_fitness(points))
            fitness_sum += individual.calc_fitness(points)
        # transpose fitness value into probability (fitness/sum of fitnesses)
        return [fitness_value / fitness_sum for fitness_value in probability_list]

    def crossover(self, probability_list):
        parents_first = random.choices(self.population, weights=probability_list, k=int(len(self.population)/2))
        # TODO change simple probability calculated with fitness to use polynomial distance metric
        # simple parent choose
        parents_second = random.choices(self.population, weights=probability_list, k=int(len(self.population)/2))
        parents = zip(parents_first, parents_second)
        children = []
        for pair in parents:
            crossover_position = random.randrange(0, 4)
            first_child = Individual(params=np.append(pair[0].polynomial.params[0:crossover_position],
                                                      pair[1].polynomial.params[crossover_position:]))
            second_child = Individual(params=np.append(pair[1].polynomial.params[0:crossover_position],
                                                       pair[0].polynomial.params[crossover_position:]))
            children.append(first_child)
            children.append(second_child)
        self.population = children

    def mutation(self, mutation_probability, mutation_value):
        for individual in self.population:
            for i in range(0, 4):
                if random.randrange(0, 100) < mutation_probability*100:
                    if random.randrange(0, 2) == 0:
                        individual.polynomial.change_param(i, mutation_value)
                    else:
                        individual.polynomial.change_param(i, -1*mutation_value)

    def evolve_generation(self, points, mutation_probability, mutation_value):
        self.crossover(self.calc_probabilities(points))
        self.mutation(mutation_probability, mutation_value)
        print("Generation no. ", self.get_generation(), " successfully evolved")
        print("Pop: ", self.get_pop(), ", Best fitness: ", self.get_bestfit(points),
              ", Avg Fitness: ", self.get_avgfit(points))
        self.generation += 1

    def run(self, points, mutation_probability=0.1, mutation_value=1):
        while self.get_bestfit(points) != 1.0:
            self.evolve_generation(points, mutation_probability, mutation_value)


def points_generator(clusters, _range=0.1, quantity=100):
    '''

    :param clusters: numpy matrix [[x, y]...] of clusters origins
    :param _range: (dx, dy) max range in both directions from the cluster origin
    :param quantity: number of points in each cluster
    :return: numpy matrix [[x, y, class]...] of generated points belonging to class {-1, 1}
    '''

    points = []
    for i in range(0, clusters.shape[0]):
        for j in range(0, quantity):
            x = random.uniform(clusters[i, 0]-_range, clusters[i, 0]+_range)
            y = random.uniform(clusters[i, 1]-_range, clusters[i, 1]+_range)
            _class = pow(-1, i)
            point = (x, y, _class)
            points.append(point)
    return np.asarray(points)


if __name__ == "__main__":
    clusters = np.array([[0.1, 0.1], [0.5, 0.2], [0.8, 0.5]])
    fdc = np.array([[1, 2, 3]])
    test = np.array([[1, 2, 3], [1, 2, 3], [2, 2, 2]])

    population = Population(200)
    population.run(points_generator(clusters))



