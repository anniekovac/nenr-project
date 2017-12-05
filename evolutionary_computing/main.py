import numpy
import os


class Guess(object):
	def __init__(self, gene):
		"""
		:param genes: list 
		"""
		self.gene = gene
		self.fitness = None


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
	fitness = sum_of_diffs/number_of_samples
	return fitness


def crossover(guess1, guess2):
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
	return new_gene_instance

def generate_population(n):
	population = []
	for guess in range(n):
		genes = numpy.random.uniform(low=-4, high=4, size=(5,))
		guess_instance = Guess(genes)
		fitness = get_fitness(guess_instance)
		guess_instance.fitness = fitness
		population.append(guess_instance)
		print(fitness)
	return population


def main():
	population = generate_population(5)
	crossover(population[0], population[1])



if __name__ == "__main__":
	main()
