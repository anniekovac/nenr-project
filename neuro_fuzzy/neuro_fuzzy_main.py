import numpy


class Neuron(object):
	def __init__(self, previous_layer_neurons):
		self.layer_number = None
		self.output = None
		self.previous_layer_neurons = previous_layer_neurons


class InputNeuron(Neuron):
	def __init__(self, previous_layer_neurons):
		super().__init__(previous_layer_neurons)
		self.input = None


def set_net_acrhitecture():
	"""
	Defining network architecture.
	:return: numpy.array - list of lists in which lists are layers
							instances of classes Neuron and InputNeuron are
							used in lists that represent layers
	"""
	input_neurons = numpy.array([InputNeuron(numpy.array([])), InputNeuron(numpy.array([])),
								 InputNeuron(numpy.array([])), InputNeuron(numpy.array([]))])
	layer2 = numpy.array([Neuron(input_neurons), Neuron(input_neurons)])
	layer3 = numpy.array([Neuron(layer2), Neuron(layer2)])
	layer4 = numpy.array([Neuron(layer3), Neuron(layer3)])
	layer5 = numpy.array([Neuron(layer4)])
	neural_net = numpy.array([input_neurons, layer2, layer3, layer4, layer5])
	return neural_net


def membership_function(x, a=1, b=1):
	"""
	Calculating membership function on domain x based on 
	function defined in homework preparations.
	:param x: numpy.array (domain of the fuzzy set) 
	:param a: float
	:param b: float
	:return: dict
	"""
	member_func = 1/(1 + numpy.exp(b*(x - a)))
	membership_dict = dict()
	for element, membership in zip(x, member_func):
		membership_dict[element] = membership
	return membership_dict

#def t_norm()


if __name__ == '__main__':
	nn = set_net_acrhitecture()
