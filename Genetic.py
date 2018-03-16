import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import time


class Polynomial:
    def __init__(self, parameters):
        self.params = parameters
        self.degree = self.params.shape[0] - 1

    def get_value(self, x):
        ret_val = self.params[self.degree]
        for i in range(1, self.degree+1):
            ret_val = np.add(ret_val, pow(x, i)*self.params[self.degree-i])
        return ret_val

    def get_degree(self):
        return self.degree

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
        self.best_individual = Individual()
        self.generation = 0
        self.best_fit = 0.0
        self.population = []
        for i in range(0, pop):
            new_individual = Individual()
            self.population.append(new_individual)

    def get_pop(self):
        return len(self.population)

    def get_generation(self):
        return self.generation

    def get_bestfit(self, points):
        for individual in self.population:
            fit = individual.calc_fitness(points)
            if fit > self.best_fit:
                self.best_fit = fit
                self.best_individual = individual

    def get_avgfit(self, points):
        fitness_sum = 0.0
        for individual in self.population:
            fitness_sum += individual.calc_fitness(points)
        return fitness_sum/len(self.population)

    def get_fitness_list(self, points):
        fitness_list = []
        for individual in self.population:
            fitness_list.append(individual.calc_fitness(points))
        return fitness_list

    def calc_spatial_distances(self, individual_params):
        poly_vector = []
        for individual in self.population:
            poly_vector.append(individual.polynomial.params)
        poly_vector = np.asarray(poly_vector)
        distances = cdist(poly_vector, individual_params, 'euclidean')
        return distances/sum(distances)

    @staticmethod
    def calc_probabilities(fitness_list):
        fitness_sum = 0.0
        probability_list = []
        for fitness_value in fitness_list:
            probability_list.append(fitness_value)
            fitness_sum += fitness_value
        # transpose fitness value into probability (fitness/sum of finesses)
        return [fitness_value / fitness_sum for fitness_value in probability_list]

    def crossover(self, points, fitness_list):
        parents_first = []
        for i in range(0, int(len(self.population)/2)):
            tournament = random.choices(self.population, weights=self.calc_probabilities(fitness_list),
                                        k=5)
            best_fit = 0.0
            best_parent = Individual()
            for parent in tournament:
                if parent.calc_fitness(points) > best_fit:
                    best_fit = parent.calc_fitness(points)
                    best_parent = parent
            parents_first.append(best_parent)
        fitness_vector = np.asarray(fitness_list)
        parents = []
        for first_parent in parents_first:
            second_parent = random.choices(
                self.population,
                weights=(fitness_vector * self.calc_spatial_distances(
                    first_parent.polynomial.params[:, np.newaxis].transpose()).transpose()).transpose(), k=1)
            parents.append((first_parent, second_parent[0]))
        children = []
        for pair in parents:
            crossover_position = random.randrange(0, pair[0].polynomial.degree+1)
            first_child = Individual(params=np.append(pair[0].polynomial.params[0:crossover_position],
                                                      pair[1].polynomial.params[crossover_position:]))
            second_child = Individual(params=np.append(pair[1].polynomial.params[0:crossover_position],
                                                       pair[0].polynomial.params[crossover_position:]))
            children.append(first_child)
            children.append(second_child)
        self.population = children

    def mutation(self, mutation_probability):
        for individual in self.population:
            if random.randrange(0, 100) < mutation_probability*100:
                for i in range(0, individual.polynomial.degree+1):
                    individual.polynomial.change_param(i, random.uniform(-10.0, 10.0))

    def evolve_generation(self, points, _avg_fit, _best_fit, mutation_probability):
        # perform crossover operation over population
        self.crossover(points, self.get_fitness_list(points))
        self.generation += 1
        # perform mutation operation over newly created generation
        self.mutation(mutation_probability)
        print("Generation no. ", self.get_generation(), " successfully evolved")
        print("Pop: ", self.get_pop(), ", Best fitness: ", self.best_fit,
              ", Avg Fitness: ", self.get_avgfit(points))
        self.get_bestfit(points)
        _avg_fit.append(self.get_avgfit(points))
        _best_fit.append(self.best_fit)

    def run(self, points, generation_number, mutation_probability=0.1):
        '''
        This method runs genetic algorithm over population

        :param points: matrix nx3 (x, y, class) && class = {-1, 1}
        :param generation_number: number of generations which will be generated during run
        :param mutation_probability: probability of individual mutation <0, 1>
        :return: (value of fitness of the best individual in whole run <0, 1>,
        best individual in whole run, [] of average fitness over generations,
        [] of best fitness over generations
        '''

        _best_fit = []
        _avg_fit = []
        while self.generation < generation_number:
            self.evolve_generation(points, _avg_fit, _best_fit, mutation_probability)

        return _avg_fit, _best_fit


def points_generator(clusters, _range=0.1, quantity=20):
    points = []
    for i in range(0, clusters.shape[0]):
        for j in range(0, quantity):
            x = random.uniform(clusters[i, 0]-_range, clusters[i, 0]+_range)
            y = random.uniform(clusters[i, 1]-_range, clusters[i, 1]+_range)
            _class = pow(-1, i)
            point = (x, y, _class)
            points.append(point)
    return np.asarray(points)


def brute_force(points):
    individual = Individual()
    while individual.calc_fitness(points) != 1.0:
        individual = Individual()
    return individual

if __name__ == "__main__":
    clusters = np.array([[0.4, 0.5], [0.4, 0.42]])
    population = Population(100)
    data_set = points_generator(clusters)

    start = time.time()
    # BRUTAL
    # best_poly = brute_force(data_set)
    # polynomial = np.poly1d(best_poly.polynomial.params.transpose())
    avg_fit, best_fit = population.run(data_set, 100, mutation_probability=0.2)
    stop = time.time()
    print("Time elapsed: ", stop - start, "s")

    # plot best individual and points
    polynomial = np.poly1d(population.best_individual.polynomial.params.transpose())
    x = np.linspace(0.28, 0.52, 100)
    y = polynomial(x)
    my_colors = np.array(['tab:blue', 'tab:orange'])
    for i in range(0, data_set[:, :].shape[0]):
        if data_set[i, 2] == -1:
            data_set[i, 2] = 0
    plt.scatter(x=data_set[:, 0], y=data_set[:, 1], c=my_colors[data_set[:, 2].astype(int)])
    plt.plot(x, y)
    plt.show()

    # plot graph of best fitness over generation distribution
    fig, ax = plt.subplots()
    idx = np.arange(1, len(best_fit)+1)
    ax.set_xticks(idx)
    ax.set_ylim([0, 1])
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.bar(idx, best_fit)
    plt.show()

    # plot graph of average fitness over generation distribution
    fig, ax = plt.subplots()
    idx = np.arange(1, len(avg_fit)+1)
    ax.set_xticks(idx)
    ax.set_ylim([0, 1])
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.bar(idx, avg_fit)
    plt.show()



