import sys
import numpy
sys.path.append("..")  # Adds higher directory to python modules path.
import evolutionary_computing.main as evol
import neural_network.neural_network_util as nn_util
from pprint import pprint as pp
import get_database


class NeuralNetwork():
	def __init__(self, number_of_params, arch_numbers):
		self.parameters_list = numpy.random.uniform(low=-4, high=4, size=(number_of_params,))
		self.arch_numbers = arch_numbers

	# TODO: if there are more hidden layers
	def calculate_output(self, input):
		"""
		This function calculates input of this neural network
		based on input given to it (coordinates of a point).
		:param input: tuple (x, y) coordinates
		:return: list
		"""
		x, y = input
		for layer_idx, neuron_number in enumerate(self.arch_numbers):
			if layer_idx == 0:
				# these are input neurons
				previous_layer_outputs = [x, y]
			elif layer_idx == 2:
				# these are neurons of second layer
				# these calculate weighted sum

				new_outputs = []

				# going through every neuron in this layer
				for neuron in range(neuron_number):

					# for this type of neuron there are always 4 parameters (wi and si for
					# two input neurons)
					parameters_for_this_neuron = self.parameters_list[neuron:neuron+4]

					weighted_sum = 0

					# going through every output from
					# the previous layer
					for idx, previous_neuron_output in enumerate(previous_layer_outputs):
						wi = float(parameters_for_this_neuron[idx*2])  # idx * 2 for 0 = 0; idx*2 for 1 = 2;
						xi = float(previous_neuron_output)
						si = parameters_for_this_neuron[idx*2 + 1]  # idx*2 + 1 for 0 = 1; idx*2 + 1 for 1 = 3
						weighted_sum += numpy.absolute(xi - wi)/numpy.absolute(si)

					new_outputs.append(1/(1 + weighted_sum))

				previous_layer_outputs = new_outputs

			elif layer_idx == len(self.arch_numbers) - 1:

				# these are neurons of every other layer
				new_outputs = []

				# for this type of neuron there are always n + 1 parameters (wi for
				# all input neurons and one more wi for current output neuron)

				# we have to figure out index for first parameter of this neuron
				number_of_params = neuron_number * self.arch_numbers[1]
				parameters_for_last_layer = self.parameters_list[-number_of_params:]

				# going through every neuron in this layer
				for neuron in range(neuron_number):

					# every neuron in this layer has as many parameters as there are
					# neurons in previous layer - for example if there is 8 neurons in previous layer,
					# there has to be 8 parameters
					parameters_for_this_neuron = parameters_for_last_layer[neuron:neuron + self.arch_numbers[1]]

					weighted_sum = 0

					# going through every output from
					# the previous layer
					for idx, previous_neuron_output in enumerate(previous_layer_outputs):
						wi = parameters_for_this_neuron[idx]
						xi = previous_neuron_output
						weighted_sum += numpy.absolute(xi - wi)

					new_outputs.append(1/(1 + weighted_sum))

				previous_layer_outputs = new_outputs

		return previous_layer_outputs


def calculate_param_number(arch_numbers):
	"""
	Function for calculating how many parameters
	neural network needs based on architecture numbers
	we have given to it.
	:param arch_numbers: list of integers [2, 8, 3] - 3 layers, 2 neurons in first, 
													 	8 neurons in second, 3 neurons in third 
	:return: int (number of parameters)
	"""
	# calculating how many parameters this network needs
	sum_of_params = 0
	for idx, number in enumerate(arch_numbers):
		if idx == 0:
			continue
		elif idx == 1:
			sum_of_params += number * 2 * 2
		elif idx == len(arch_numbers) - 1:
			sum_of_params += number * (arch_numbers[1] + 1)
		else:
			sum_of_params += number * (arch_numbers[1])
	return sum_of_params


if __name__ == '__main__':
	arch_numbers = [2, 8, 3]
	number_of_params = calculate_param_number(arch_numbers)
	nn = NeuralNetwork(number_of_params, arch_numbers)

	dataset = get_database.get_database()
	for data in dataset.list_of_data:
		#print(data.coordinates)
		print(nn.calculate_output(data.coordinates))
