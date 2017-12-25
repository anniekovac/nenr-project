import numpy


class Sample(object):
	def __init__(self, inputs, outputs):
		self.inputs = inputs
		self.outputs = outputs


class Neuron(object):
	def __init__(self, previous_layer_neurons):
		self.layer_number = None
		self.output = None
		self.previous_layer_neurons = previous_layer_neurons
		self.weights_from_previous_layer = numpy.random.uniform(low=-1.5, high=1.5,
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
