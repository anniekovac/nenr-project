import numpy
from pprint import pprint as pp
import matplotlib.pyplot as plt
import os


class Sample(object):
	def __init__(self, inputs, outputs):
		self.inputs = inputs
		self.outputs = outputs


class Neuron(object):
	def __init__(self, previous_layer_neurons):
		self.layer_number = None
		self.output = None
		self.previous_layer_neurons = previous_layer_neurons
		self.weights_from_previous_layer = numpy.random.uniform(low=-1, high=1,
																size=(len(previous_layer_neurons),))
		self.gradients_from_next_layer = None


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
	:param input: list
	:param neural_net: list of lists
	:return: list
	"""
	for layer_index, layer in enumerate(neural_net):
		for neuron_idx, neuron in enumerate(layer):
			if layer_index == 0:
				neural_net[layer_index][neuron_idx].input = input[neuron_idx]
				neural_net[layer_index][neuron_idx].output = input[neuron_idx]
			else:
				neurons_from_previous_layer = neuron.previous_layer_neurons
				weights_from_previous_layer = neuron.weights_from_previous_layer
				sum_of_products = 0
				for weight_idx, previous_neuron in enumerate(neurons_from_previous_layer):
					sum_of_products += previous_neuron.output*weights_from_previous_layer[weight_idx]

				neural_net[layer_index][neuron_idx].output = sigmoid(sum_of_products)
		if layer_index == len(neural_net) - 1:
			nn_output = [neuron.output for neuron in layer]
	return nn_output


def backpropagation(eta, samples, neural_net):
	"""
	:param eta: stopa ucenja
	:param samples: lista uzoraka
	"""
	# initialization of gradients
	# inicijalizacija gradijenata na nulu, mora se dogoditi pri svakom uzorku
	for layer_idx, layer in enumerate(neural_net):
		for neuron_idx, neuron in enumerate(layer):
			if layer_idx == len(neural_net) - 1:
				break
			neural_net[layer_idx][neuron_idx].gradients_from_next_layer = numpy.zeros(len(neural_net[layer_idx + 1]))

	# za svaki uzorak
	for i in range(0, len(samples)-1):

		# izracunati output koji daje neuronska mreza
		nn_outputs = get_neural_net_output(samples[i].inputs, neural_net)

		# izracunati pogresku output layera neuronske mreze
		e = numpy.subtract(samples[i].outputs, nn_outputs)

		# prolazanje unazad po neuronskoj mrezi,
		# od zadnjeg sloja prema prvom
		for layer_idx in range(len(neural_net)-1, 0, -1):
			layer = neural_net[layer_idx]  # oznacavanje jednog sloja
			previous_layer = neural_net[layer_idx-1]  # sloj prethodni od layera

			next_e = numpy.zeros(len(previous_layer))  # inicijaliziranje greske za prethodni sloj
			# ZA SVAKI NEURON U PRETHODNOM SLOJU
			for neuron_in_previous_idx, neuron_in_previous in enumerate(previous_layer):  # neuron in previous: i
				# ZA SVAKI NEURON U TRENUTNOM SLOJU
				for neuron_idx, neuron in enumerate(layer):  # neuron : j
					# izracunaj delta za neuron j
					delta = derivatives_sigmoid(neuron.output)*e[neuron_idx]

					# pomocu delte izracunaj gradijent
					# delta - delta izracunata za j-ti neuron
					# neuron_in_previous.output - output i-tog neurona
					gradient = delta*neuron_in_previous.output

					# DODAVANJE GRADIJENTA ZA SVAKI POJEDINI NEURON U TRENUTOM SLOJU
					# dodaju se gradijenti na neuron iz proslog sloja
					my_var = neural_net[layer_idx - 1][neuron_in_previous_idx].gradients_from_next_layer[neuron_idx]
					neural_net[layer_idx - 1][neuron_in_previous_idx].gradients_from_next_layer[neuron_idx] = my_var + gradient

					# izracunavanje pogreske koja ce se koristiti u sljedecoj iteraciji
					next_e[neuron_in_previous_idx] += (delta * neuron.weights_from_previous_layer[neuron_in_previous_idx])
					# racunam e u ovom koraku za sljedeci korak (jer j u ovom koraku u sljedecem
					# postaje o, i vise necu imati njegove tezine)
			e = next_e

	# UPDATING WEIGHTS
	for layer_idx in range(1, len(neural_net)):
		layer = neural_net[layer_idx]
		previous_layer = neural_net[layer_idx - 1]
		for neuron_idx, neuron in enumerate(layer):
			for previous_idx, previous_neuron in enumerate(previous_layer):
				change = eta*previous_neuron.gradients_from_next_layer[neuron_idx]
				neural_net[layer_idx][neuron_idx].weights_from_previous_layer[previous_idx] += change

	return neural_net


def approx_kvadrat(nn):
	inputs = numpy.array([[-1], [-0.8], [-0.6], [-0.4], [-0.2], [0.0], [0.2], [0.4], [0.6], [0.8], [1]])
	outputs = numpy.array([[1], [0.64], [0.36], [0.16], [0.04], [0], [0.04], [0.16], [0.36], [0.64], [1]])
	sample = Sample(inputs, outputs)

	inputs = numpy.array([item[0] for item in inputs])
	wanted_outputs = numpy.array([item[0] for item in outputs])
	nn_outputs = []
	for i in inputs:
		input = [i]
		output = get_neural_net_output(input, nn)
		nn_outputs.append(output)
	nn_outputs = numpy.array(nn_outputs)

	brojac = 10000
	while brojac:
		nn = backpropagation(1, sample, nn)
		MSE = 0
		if brojac % 1000 == 0:
			for idx, i in enumerate(inputs):
				input = [i]
				output = get_neural_net_output(input, nn)
				MSE += numpy.square(wanted_outputs[idx] - output)
				MSE = MSE/len(inputs)
			print("Iteration: {}, MSE: {}".format(brojac, MSE))
		brojac -= 1


	nn_outputs_after = []
	for i in inputs:
		input = [i]
		output = get_neural_net_output(input, nn)
		nn_outputs_after.append(output)
	nn_outputs_after = numpy.array(nn_outputs_after)

	plt.figure(2)
	plt.plot(inputs, wanted_outputs, label="Wanted outputs")
	plt.plot(inputs, nn_outputs, label="NN outputs before learning")
	plt.plot(inputs, nn_outputs_after, label="NN outputs after learning")
	plt.legend()
	plt.show()


def get_database(path_to_db):
	with open(path_to_db, 'r') as database:
		samples = []
		for line in database:
			final_points = []
			points = line.split("\t")
			for item in points:
				if "," in item:
					final_points.append([float(i) for i in item.split(",")])
				else:
					str_output = item.rstrip("\n")
					output = [int(number) for number in str_output]
			final_points = numpy.array(final_points)
			output = numpy.array(output)
			sample = Sample(final_points, output)
			samples.append(sample)
		samples = numpy.array(samples)
	return samples


def train(samples, neural_net):
	brojac = 10000
	while brojac:
		neural_net = backpropagation(1, samples, neural_net)
		MSE = 0
		if brojac % 1000 == 0:
			for idx, i in enumerate(samples.inputs):
				input = [i]
				output = get_neural_net_output(input, nn)
				MSE += numpy.square(wanted_outputs[idx] - output)
				MSE = MSE/len(inputs)
			print("Iteration: {}, MSE: {}".format(brojac, MSE))
		brojac -= 1


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
	arch_numbers = [100, 6, 10, 6, 5]
	list_of_lists = create_network_architecture(arch_numbers)
	#approx_kvadrat(list_of_lists)
	samples = get_database(os.path.join(os.getcwd(), "my_final_database.txt"))
	train(samples, list_of_lists)
