import numpy
from define_classes import InputNeuron, Neuron, sigmoid, derivatives_sigmoid


def learning_algortihms(eta, samples, neural_net, choose_algorithm="BP"):
	"""
	Implementing three learning algorithms.
	- backpropagation ("BP") - using entire batch of samples
	- stohastic backpropagation ("SBP") - learning sample by sample
	- mini-batch backpropagation ("MBBP")- learning by batches of smaller size (20)
	
	:param eta: learning rate
	:param samples: numpy array (list of Sample class instances)
	:param neural_net: list of lists (architecture of neural network)
	:return: 
	"""
	if choose_algorithm == "BP":
		return backpropagation(eta, samples, neural_net)
	elif choose_algorithm == "SBP":
		nn = neural_net
		for sample in samples:
			nn = backpropagation(eta, sample, nn)
		return nn
	elif choose_algorithm == "MBBP":
		alphas = []
		betas = []
		gammas = []
		deltas = []
		epsilons = []
		for sample in samples:
			outputs = sample.outputs.tolist()
			if (outputs > [1, 0, 0, 0, 0]) - (outputs < [1, 0, 0, 0, 0]) == 0:
				alphas.append(sample)
			elif (outputs > [0, 1, 0, 0, 0]) - (outputs < [0, 1, 0, 0, 0]) == 0:
				betas.append(sample)
			elif (outputs > [0, 0, 1, 0, 0]) - (outputs < [0, 0, 1, 0, 0]) == 0:
				gammas.append(sample)
			elif (outputs > [0, 0, 0, 1, 0]) - (outputs < [0, 0, 0, 1, 0]) == 0:
				deltas.append(sample)
			elif (outputs > [0, 0, 0, 0, 1]) - (outputs < [0, 0, 0, 0, 1]) == 0:
				epsilons.append(sample)

		nn = neural_net
		for i in range(0, 10, 2):  # select every other i
			mini_batch = []
			mini_batch.extend([alphas[i], alphas[i+1]])
			mini_batch.extend([betas[i], betas[i + 1]])
			mini_batch.extend([gammas[i], gammas[i + 1]])
			mini_batch.extend([deltas[i], deltas[i + 1]])
			mini_batch.extend([epsilons[i], epsilons[i + 1]])
			mini_batch = numpy.array(mini_batch)
			nn = backpropagation(eta, mini_batch, nn)
		return nn


def train(samples, neural_net):
	"""
	Function used for training neural network. 
	Backpropagation is used in for loop.
	:param samples: numpy.array - list of Sample class instances
	:param neural_net: list of lists [[input_neuron1, input_neuron2, ...], [hidden_neuron1, hidden_neuron2...], ...] 
	:return: list of lists
	"""
	brojac = 10000
	while brojac:
		if brojac % 1000 == 0:
			# neural_net = backpropagation(0.1, samples, neural_net)
			neural_net = learning_algortihms(0.1, samples, neural_net, choose_algorithm="MBBP")
			MSE = 0
			for idx, sample in enumerate(samples):
				input = sample.inputs
				wanted_output = sample.outputs
				output = get_neural_net_output(input, neural_net)
				MSE += numpy.square(wanted_output - output)
			MSE = MSE / len(samples)
			print("Iteration: {}, MSE: {}".format(10000 - brojac, MSE))
		brojac -= 1
	return neural_net


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

				neural_net[layer_index][neuron_idx].output = float(sigmoid(sum_of_products))
		if layer_index == len(neural_net) - 1:
			nn_output = [neuron.output for neuron in layer]
	return nn_output


def backpropagation(eta, samples, neural_net):
	"""
	Implementing backpropagation algorithm.
	:param eta: learning rate
	:param samples: numpy.array - list of Sample class instances
	"""
	# initialization of gradients
	# inicijalizacija gradijenata na nulu, mora se dogoditi pri svakom uzorku
	for layer_idx, layer in enumerate(neural_net):
		for neuron_idx, neuron in enumerate(layer):
			if layer_idx == len(neural_net) - 1:
				break
			neural_net[layer_idx][neuron_idx].gradients_from_next_layer = numpy.zeros(len(neural_net[layer_idx + 1]))

	if not isinstance(samples, numpy.ndarray):
		my_sample = [samples]
		my_sample.append(None)
		samples = numpy.array(my_sample)

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
