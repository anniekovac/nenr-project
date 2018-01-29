import numpy
from pprint import pprint as pp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from fuzzy_util import membership_function


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


def plot_membership(membership_dict, title=""):
	x_axis = []
	y_axis = []
	for key, item in membership_dict.items():
		x_axis.append(key)
		y_axis.append(item)

	x_axis = numpy.array(x_axis)
	y_axis = numpy.array(y_axis)
	plt.figure(1)
	plt.plot(x_axis, y_axis) #, label="Correct outputs")
	plt.title("Membership function {}".format(title))
	plt.grid()
	plt.show()


if __name__ == '__main__':
	x = numpy.array([i for i in range(-4, 5)])
	y = numpy.array([j for j in range(-4, 5)])
	# plot3d(x, y)
	member_dict = membership_function(x)
	plot_membership(member_dict)