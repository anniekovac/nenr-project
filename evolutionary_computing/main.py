import numpy


class Guess(object):
	def __init__(self, genes):
		"""
		:param genes: list 
		"""
		self.genes = genes


def get_fitness(guess):
	"""
	:param guess:   
	:return: 
	"""
	pass


def crossover(guess1, guess2):
	"""
	:param guess1: 
	:param guess2: 
	:return: new guess 
	"""
	pass


def generate_population(n):
	population = []
	for guess in range(n):
		genes = numpy.random.uniform(low=-4, high=4, size=(5,))
		guess_instance = Guess(genes)
		population.append(guess_instance)


def my_function(gene, x, y):
	b0, b1, b2, b3, b4 = gene
	return numpy.sin(b0 + b1*x)+b2*numpy.cos(x*(b3+y))*(1/(1+numpy.exp((numpy.square(x-b4)))))


def main():
	generate_population(5)


if __name__ == "__main__":
	generate_population(5)
