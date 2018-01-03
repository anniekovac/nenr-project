import numpy
from pprint import pprint as pp


class Neuron(object):
	def __init__(self, previous_layer_neurons):
		self.layer_number = None
		self.output = None
		self.previous_layer_neurons = previous_layer_neurons


class InputNeuron(Neuron):
	def __init__(self, previous_layer_neurons):
		super().__init__(previous_layer_neurons)
		self.input = None


def set_net_acrhitecture(number_of_rules):
	"""
	Defining network architecture.
	:arg number_of_rules: int
	:return: numpy.array - list of lists in which lists are layers
							instances of classes Neuron and InputNeuron are
							used in lists that represent layers
	"""
	input_neurons = numpy.array([InputNeuron(numpy.array([])) for i in range(2*number_of_rules)])
	layer2 = numpy.array([Neuron(input_neurons) for i in range(number_of_rules)])
	layer3 = numpy.array([Neuron(layer2) for i in range(number_of_rules)])
	layer4 = numpy.array([Neuron(layer3) for i in range(number_of_rules)])

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


def t_norm(x, membership_A, membership_B):
	"""
	Implemented t-norm based on product.
	:param x: float (crisp, element of domain both for A and B) 
	:param membership_A: dict (membership dict for fuzzy set A)
	:param membership_B: dict (membership dict for fuzzy set B) 
	:return: float
	"""
	return membership_A[x] * membership_B[x]


def calculate_f_for_rule(x, y, p, q, r):
	"""
	Calculating output f for only one rule od antecedent.
	:param x: float 
	:param y: float 
	:param p: float (should be learned by neural network)
	:param q: float (should be learned by neural network)
	:param r: float (should be learned by neural network)
	:return: float
	"""
	return p*x + q*y + r


def calculate_mean_weights(weights, individual_rule_outputs):
	"""
	Calculating mean weights that are supposed to be calculated in 
	layer 3. 
	:param weights: numpy.array 
	:param individual_rule_outputs: numpy.array 
	:return: numpy.array
	"""
	mean_weights = []
	sum_of_weights = numpy.sum(weights)
	for weight, output in zip(weights, individual_rule_outputs):
		mean_weights.append(weight*output/sum_of_weights)
	mean_weights = numpy.array(mean_weights)
	return mean_weights


def calculate_output(mean_weights, individual_rule_outputs):
	"""
	Calculating final output in output neuron (layer 5).
	:param mean_weights: numpy.array 
	:param individual_rule_outputs: numpy.array
	:return: float
	"""
	sum_of_outputs = 0
	for weight, output in zip(mean_weights, individual_rule_outputs):
		sum_of_outputs += weight*output
	return sum_of_outputs


if __name__ == '__main__':
	nn = set_net_acrhitecture(3)
	pp(nn)
	x = numpy.array([i for i in range(-4, 4)])
	y = numpy.array([i for i in range(-4, 4)])
	A = membership_function(x, a=2, b=3)
	B = membership_function(y, a=1, b=1)
	print(t_norm(3, A, B))