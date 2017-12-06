import numpy
import os
import random
import matplotlib.pyplot as plt
import copy

class Guess(object):
	def __init__(self, gene):
		"""
		:param genes: list 
		"""
		self.gene = gene
		self.fitness = None
		self.MSE = None


def my_function(gene, x, y):
	"""
	:param gene: numpy array 
	:param x: float
	:param y: float
	:return: function output
	"""
	b0, b1, b2, b3, b4 = gene
	return numpy.sin(b0 + b1*x)+b2*numpy.cos(x*(b3+y))*(1/(1+numpy.exp((numpy.square(x-b4)))))


def parse_data(path_to_file):
	"""
	:param path_to_file: str (path to data) 
	"""
	final = numpy.array([0, 0, 0])
	with open(path_to_file, 'r') as data:
		for line in data:
			x = float(line.split("\t", 1)[0])
			line = line.split("\t", 1)[1]
			y = float(line.split("\t", 1)[0])
			f = float(line.split("\t", 1)[1])
			line_array = numpy.array([x, y, f])
			final = numpy.vstack((final, line_array))
	final = numpy.delete(final, (0), axis=0)
	return final


def get_fitness(guess):
	"""
	:param guess: Guess instance
	:return: float (MQE - mean quadratic error)
	"""
	dataset1 = os.path.join(os.path.dirname(__file__), "zad4-dataset1.txt")
	dataset2 = os.path.join(os.path.dirname(__file__), "zad4-dataset2.txt")
	dataset = parse_data(dataset1)
	sum_of_diffs = 0
	number_of_samples = 0
	for row in dataset:
		f_real = row[2]
		x = row[0]
		y = row[1]
		f_system = my_function(guess.gene, x, y)
		sum_of_diffs += numpy.square(f_system-f_real)
		number_of_samples += 1
	MSE = sum_of_diffs/number_of_samples
	fitness = 1/MSE
	return (fitness, MSE)

def mutation(guess, mutation_probability=0.01):
	gene = guess.gene
	for index, num in enumerate(gene):
		if numpy.random.uniform(low=0, high=1) <= mutation_probability:
			gene[index] = numpy.random.uniform(low=-4, high=4)
	return guess.gene


def crossover(guess1, guess2, mut_prob):
	"""
	This crossover implements discreete recombination
	of genes.
	:param guess1: Guess class instance 
	:param guess2: Guess class instance
	:return: Guess class instance
	"""
	gene1 = guess1.gene
	gene2 = guess2.gene
	new_gene = numpy.array([numpy.random.choice([item1, item2]) for (item1, item2) in zip(gene1, gene2)])
	new_gene_instance = Guess(new_gene)
	mutation(new_gene_instance, mut_prob)
	return new_gene_instance


def generate_population(n):
	"""
	Generating first population. Genes are random (float) 
	numbers in interval	[-4, 4]. For every guess in population
	fitness is calculated and added in its instance. In the end 
	function returns first population.
	:param n: number of guesses in population
	:return: list of Guess instances
	"""
	population = []
	for guess in range(n):
		genes = numpy.random.uniform(low=-4, high=4, size=(5,))
		guess_instance = Guess(genes)
		fitness, MSE = get_fitness(guess_instance)
		guess_instance.fitness = fitness
		guess_instance.MSE = MSE
		population.append(guess_instance)
		#print(fitness)
	return population


def kanonski_generacijski(n):
	first_population = generate_population(n)

def tri_turnirska_eliminacijska(n, iterations, mut_prob, mse_exit_criteria=0.01):
	population = generate_population(n)
	i = iterations
	while i:
		i -= 1
		[first_guess, second_guess, third_guess] = random.sample(population, 3)
		elim_MSE = max(first_guess.MSE, second_guess.MSE, third_guess.MSE)
		elim_choice = [item for item in [first_guess, second_guess, third_guess] if item.MSE == elim_MSE][0]
		parents = [item for item in [first_guess, second_guess, third_guess] if item != elim_choice]
		child = crossover(parents[0], parents[1], mut_prob)
		fitness, MSE = get_fitness(child)
		child.fitness = fitness
		child.MSE = MSE
		population = [guess for guess in population if guess != elim_choice]
		population.append(child)
		min_MSE = min([item.MSE for item in population])
		if min_MSE < mse_exit_criteria:
			break
		if i%1000 == 0:
			print(min_MSE)
		best_of = [item for item in population if item.MSE == min_MSE][0]
	return best_of

def plot(final, best):
	"""
	:param final: array of inputs and output (data that we have from dataset) 
	:param best: best genes found (Guess instance)
	"""
	inputs = []
	corr_outputs = []
	my_outputs = []
	my_final = copy.deepcopy(final)
	my_final = my_final[200:]
	for i, item in enumerate(my_final):
		corr_output = item[2]
		x, y = item[0], item[1]
		my_output = my_function(best.gene, x, y)
		inputs.append(i)
		corr_outputs.append(corr_output)
		my_outputs.append(my_output)
	plt.figure(1)
	plt.plot(inputs, corr_outputs, label="Correct outputs")
	plt.plot(inputs, my_outputs, 'r', label="Outputs calculated by best result of EA")
	plt.legend()
	plt.title("MSE: {}".format(best.MSE))
	plt.show()


def main():
	n = 25  # POPULATION SIZE
	mut_prob = 0.01  # MUTATION PROBABILITY
	number_of_iterations = 25000  # NUMBER OF ITERATIONS

	dataset1 = os.path.join(os.path.dirname(__file__), "zad4-dataset1.txt")
	final = parse_data(dataset1)
	# kanonski_generacijski(n)
	best = tri_turnirska_eliminacijska(n, number_of_iterations, mut_prob, mse_exit_criteria=0.01)
	plot(final, best)

if __name__ == "__main__":
	main()
