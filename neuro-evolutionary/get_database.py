import numpy
from pprint import pprint as pp
import matplotlib.pyplot as plt


class DataInstance(object):
	def __init__(self, coordinates, my_class):
		self.coordinates = coordinates
		self.belongs_to_class = my_class


class DataSet(object):
	def __init__(self, dataset):
		self.list_of_data = dataset

	def return_length_of_dataset(self):
		"""
		Returns length of existing dataset.
		:return: int 
		"""
		return len(self.list_of_data)

	def data_on_index(self, idx):
		"""
		Returns instance of class DataInstance on
		given index.
		:param idx: int
		:return: DataInstance class instance
		"""
		return self.list_of_data[idx]


def prepare_database_for_plot():
	"""
	This function prepares database for 
	created plot function. It creates
	new txt file called "new_db.txt" where
	classes as marked with "1, 2, 3" instead
	of "100" etc. 
	"""
	path_to_db = "zad7-dataset.txt"
	data_dict = dict()
	with open(path_to_db, "r") as database:
		for line in database:
			line = line.replace("\n", "")
			data = line.split("\t")
			x, y = data[0], data[1]
			belongs_to_class = "".join(data[2:])
			if belongs_to_class == "100":
				belongs_to_class = 1
			elif belongs_to_class == "010":
				belongs_to_class = 2
			elif belongs_to_class == "001":
				belongs_to_class = 3

			data_dict[(x, y)] = belongs_to_class

	with open("new_db.txt", "w") as file:
		for key, item in data_dict.items():
			file.write("{}\t{}\t{}\n".format(key[0], key[1], item))


def get_database():
	"""
	Creating dataset out of data found in txt file.
	Every sample is type of class DataInstance, 
	and dataset in total is instance of a class
	DataSet.
	:return: instance of class DataSet 
	"""
	path_to_db = "zad7-dataset.txt"

	dataset = []
	with open(path_to_db, "r") as database:
		for line in database:
			line = line.replace("\n", "")
			data = line.split("\t")
			x, y = data[0], data[1]
			belongs_to_class = "".join(data[2:])
			data = DataInstance((x, y), belongs_to_class)
			dataset.append(data)

	dataset = numpy.array(dataset)
	datas = DataSet(dataset)
	return datas


def plot():
	"""
	Plot function found here:
	https://stackoverflow.com/questions/44603609/python-how-to-plot-classification-data
	"""
	x, y, c = numpy.loadtxt('new_db.txt', delimiter='\t', unpack=True)
	plt.scatter(x, y, c=c)
	plt.grid()
	plt.show()


if __name__ == "__main__":
	dataset = get_database()
	prepare_database_for_plot()
	plot()