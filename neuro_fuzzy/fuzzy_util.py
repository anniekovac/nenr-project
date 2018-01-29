import numpy


def membership_function(x, a=1, b=1):
	"""
	Calculating membership function on domain x based on 
	function defined in homework preparations.
	:param x: int, float or numpy.array (domain of the fuzzy set)
	:param a: float
	:param b: float
	:return: dict
	"""
	member_func = 1 / (1 + numpy.exp(b * (x - a)))
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
	return p * x + q * y + r


def calculate_mean_weights(weights):
	"""
	Calculating mean weights that are supposed to be calculated in 
	layer 3. 
	:param weights: numpy.array 
	:return: numpy.array
	"""
	mean_weights = []
	sum_of_weights = numpy.sum(weights)
	for weight in weights:
		mean_weights.append(weight / sum_of_weights)
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
		sum_of_outputs += weight * output
	return sum_of_outputs
