import numpy
from pprint import pprint as pp


def my_function(x, y):
	return (numpy.square(x - 1) + numpy.square(y + 2) - 5*x*y + 3) * numpy.square(numpy.cos(x/5))


def generate_database():
	"""
	Generating database for my_function in its domain.
	:return: 
	"""
	x = [i for i in range(-4, 5)]
	y = [j for j in range(-4, 5)]
	f = dict()
	for i in x:
		for j in y:
			output = my_function(i, j)
			f[(i, j)] = output


if __name__ == '__main__':
	generate_database()
