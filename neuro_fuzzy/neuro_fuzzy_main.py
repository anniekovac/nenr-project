import numpy
from database_util import generate_database
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


class MembershipFunctionNeuron(InputNeuron):
	"""
	This Neuron is meant to be used only in layer 1, 
	where neurons use membership functions.
	"""
	def __init__(self, previous_layer_neurons):
		super().__init__(previous_layer_neurons)
		self.membership_function = None
		self.a = None
		self.b = None
		self.antecedent_type = None


def set_net_acrhitecture(number_of_rules):
	"""
	Defining network architecture.
	:arg number_of_rules: int
	:return: numpy.array - list of lists in which lists are layers
							instances of classes Neuron and InputNeuron are
							used in lists that represent layers
	"""
	# initializing number and types of neurons
	input_neurons = numpy.array([[MembershipFunctionNeuron(numpy.array([])), MembershipFunctionNeuron(numpy.array([]))] for i in range(number_of_rules)])
	layer2 = numpy.array([Neuron(input_neurons) for i in range(number_of_rules)])
	layer3 = numpy.array([Neuron(layer2) for i in range(number_of_rules)])
	layer4 = numpy.array([Neuron(layer3) for i in range(number_of_rules)])
	layer5 = numpy.array([Neuron(layer4)])
	neural_net = numpy.array([input_neurons, layer2, layer3, layer4, layer5])

	# initializing membership functions for neurons that have them
	# neurons in input layer are using these membership functions
	for index, neurons_couple in enumerate(input_neurons):

		# first neuron - its fuzzy set is set A from antecedent
		neural_net[0][index][0].a = numpy.random.uniform(low=0, high=1) # a parameter of membership function
		neural_net[0][index][0].b = numpy.random.uniform(low=0, high=1) # b parameter of membership function
		neural_net[0][index][0].antecedent_type = "A"

		# second neuron - its fuzzy set is set B from antecedent
		neural_net[0][index][1].a = numpy.random.uniform(low=0, high=1) # a parameter of membership function
		neural_net[0][index][1].b = numpy.random.uniform(low=0, high=1) # b parameter of membership function
		neural_net[0][index][1].antecedent_type = "B"

	return neural_net


def membership_function(x, a=1, b=1):
	"""
	Calculating membership function on domain x based on 
	function defined in homework preparations.
	:param x: int, float or numpy.array (domain of the fuzzy set) 
	:param a: float
	:param b: float
	:return: dict
	"""
	member_func = 1/(1 + numpy.exp(b*(x - a)))
	membership_dict = dict()
	if isinstance(x, int) or isinstance(x, float):
		return member_func
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


def main(number_of_rules=2):
	samples = generate_database()  # generating database of x, y, f
	nn = set_net_acrhitecture(number_of_rules)  # getting neural net of architecture based on number of rules
	for sample in samples:  # for every sample
		for index, neuron_couple in enumerate(nn[0]):  # for every neuron in input neurons
			input_neuron_A = neuron_couple[0]
			input_neuron_B = neuron_couple[1]

			# checking if neurons have the right antecedent value
			# just in case, this can be removed later if proven good
			if input_neuron_A.antecedent_type != "A":
				raise ValueError("Input neuron A on index {} has wrong antecedent value!".format(index))
			if input_neuron_B.antecedent_type != "B":
				raise ValueError("Input neuron B on index {} has wrong antecedent value!".format(index))

			# found membership values for both x and y
			w_A = membership_function(sample.x, input_neuron_A.a, input_neuron_A.b)  # fuzzy set A is connected to x
			w_B = membership_function(sample.y, input_neuron_B.a, input_neuron_B.b)  # fuzzy set A is connected to y

			# setting outputs of input neurons to these
			# previously calculated weights
			nn[0][index][0].output = w_A
			nn[0][index][1].output = w_B



# TODO: make a difference between A and B part of the antecedent
# TODO: still the same but make it better: now A and B are placed in a list together as a couple
# but in the next layer they need to be separated so neurons will calculate them better
if __name__ == '__main__':
	# nn = set_net_acrhitecture(2)
	# x = numpy.array([i for i in range(-4, 4)])
	# y = numpy.array([i for i in range(-4, 4)])
	# A = membership_function(x, a=2, b=3)
	# B = membership_function(y, a=1, b=1)
	main()
