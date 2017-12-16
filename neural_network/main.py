import numpy
from pprint import pprint as pp


class Neuron(object):
	def __init__(self, previous_layer_neurons):
		self.layer_number = None
		self.output = None
		self.previous_layer_neurons = previous_layer_neurons
		self.weights_from_previous_layer = numpy.random.uniform(low=-4, high=4,
																size=(len(previous_layer_neurons),))


class InputNeuron(Neuron):
	def __init__(self, previous_layer_neurons):
		super().__init__(previous_layer_neurons)
		self.input = None


def sigmoid(x):
	return 1/(1 + numpy.exp(-x))


def derivatives_sigmoid(x):
	return x * (1 - x)


def create_network_architecture(arch_numbers):
	"""
	Creating neural network based on architecture 
	given by arch_numbers.
	:param arch_numbers: list of integers
	:return: list of lists
	"""
	list_of_layers = []
	for layer_index, number in enumerate(arch_numbers):
		list_of_neurons = []
		for neuron_idx in range(number):
			if layer_index == 0:
				neuron = InputNeuron(numpy.array([]))
			else:
				neuron = Neuron(list_of_layers[layer_index-1])
			list_of_neurons.append(neuron)
		list_of_layers.append(numpy.array(list_of_neurons))
	list_of_layers = numpy.array(list_of_layers)
	return list_of_layers


def get_neural_net_output(input, neural_net):
	"""
	Getting output out of neural network.
	:param input: list of doubles
	:param neural_net: 
	:return: 
	"""
	for layer_index, layer in enumerate(neural_net):
		for neuron_idx, neuron in enumerate(layer):
			if layer_index == 0:
				neuron.input = input[neuron_idx]
				neuron.output = input[neuron_idx]
			else:
				neurons_from_previous_layer = neuron.previous_layer_neurons
				weights_from_previous_layer = neuron.weights_from_previous_layer
				sum_of_products = 0
				for weight_idx, previous_neuron in enumerate(neurons_from_previous_layer):
					sum_of_products += previous_neuron.output*weights_from_previous_layer[weight_idx]
				neuron.output = sigmoid(sum_of_products)
		if layer_index == len(neural_net) - 1:
			nn_output = layer[0].output  # AKO POSTOJI SAMO JEDAN NEURON U IZLAZNOM SLOJU
	print(nn_output)


def approx_kvadrat(nn):
	inputs = numpy.array([-1, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1])
	outputs = numpy.array([1, 0.64, 0.36, 0.16, 0.04, 0, 0.04, 0.16, 0.36, 0.64, 1])
	get_neural_net_output(inputs[0], nn)

if __name__ == '__main__':
	M = 50
	# net_architecture = input("Enter wanted net architecture:\n")
	# arch_numbers = [int(item) for item in net_architecture.split("x")]
	# if arch_numbers[0] != M*2:
	# 	print(arch_numbers[0])
	# 	raise ValueError("Invalid number of input layer neurons is entered! You entered {}, and it should be {}*2={}!"
	# 		.format(arch_numbers[0], M, M*2))
	# if arch_numbers[-1] != 5:
	# 	raise ValueError("Invalid number of outputs is entered, it should be 5 and you entered {}!"
	# 					 .format(arch_numbers[-1]))
	arch_numbers = [1, 6, 1]
	list_of_lists = create_network_architecture(arch_numbers)
	approx_kvadrat(list_of_lists)

	for layer in list_of_lists:
		pp([item.weights_from_previous_layer for item in layer])