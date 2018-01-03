import numpy
from pprint import pprint as pp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Sample(object):
	def __init__(self, x, y, f):
		self.x = x
		self.y = y
		self.f = f


def my_function(x, y):
	"""
	Function defined by assignment.
	:param x: int
	:param y: int
	:return: float
	"""
	return (numpy.square(x - 1) + numpy.square(y + 2) - 5*x*y + 3) * numpy.square(numpy.cos(x/5))


def plot3d(x, y):
	"""
	Function for plotting function calculated from 
	x, y data in 3d grid.
	:param x: list
	:param y: list
	"""
	x, y = numpy.meshgrid(x, y)
	f = my_function(x, y)
	#function = numpy.array(list(f.values()))
	fig = plt.figure()
	ax = fig.gca(projection="3d")
	surf = ax.plot_surface(x, y, f)
	ax.set_title('Function')
	plt.show()


def generate_database():
	"""
	Generating database for my_function in its domain.
	:return: numpy.array of Sample class instances
	"""
	x = [i for i in range(-4, 5)]
	y = [j for j in range(-4, 5)]
	samples = []
	for i in x:
		for j in y:
			output = my_function(i, j)
			sample = Sample(i, j, output)
			samples.append(sample)
	samples = numpy.array(samples)
	return samples


if __name__ == '__main__':
	x = [i for i in range(-4, 5)]
	y = [j for j in range(-4, 5)]
	plot3d(x, y)