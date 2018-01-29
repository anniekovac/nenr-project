import numpy
from database_util import generate_database, plot3d
import fuzzy_util as fuzzy
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


class OutputFunctionNeuron(Neuron):
	"""
	This neuron is used in layer 4. In this layer
	"functions" fi are calculated and to calculate
	these functions parameters p, q and r are needed.
	"""
	def __init__(self, previous_layer_neurons):
		super().__init__(previous_layer_neurons)
		self.p = None
		self.q = None
		self.r = None
		self.f = None


def set_net_acrhitecture(number_of_rules):
	"""
	Defining network architecture.
	:arg number_of_rules: int
	:return: numpy.array - list of lists in which lists are layers
							instances of classes Neuron and InputNeuron are
							used in lists that represent layers
	"""
	# initializing number and types of neurons

	# input neurons are the neurons that have membership functions
	# there are as many neurons as there are rules
	layer1 = numpy.array(
		[[MembershipFunctionNeuron(numpy.array([])), MembershipFunctionNeuron(numpy.array([]))] for i in
		 range(number_of_rules)])

	# neurons from other layers have "normal" neurons
	layer2 = numpy.array([Neuron(layer1) for i in range(number_of_rules)])
	layer3 = numpy.array([Neuron(layer2) for i in range(number_of_rules)])
	layer4 = numpy.array([OutputFunctionNeuron(layer3) for i in range(number_of_rules)])
	layer5 = numpy.array([Neuron(layer4)])
	neural_net = numpy.array([layer1, layer2, layer3, layer4, layer5])

	# initializing membership functions for neurons that have them
	# neurons in input layer are using these membership functions
	for index, neurons_couple in enumerate(layer1):
		# first neuron - its fuzzy set is set A from antecedent

		# prvo idem po svim parovima: A1, B1 i onda A2, B2 itd i postavljam njihove
		# parametre a i b na neku random pocetnu vrijednost

		# ovo je A1 (tj Ai)
		neural_net[0][index][0].a = numpy.random.uniform(low=-4, high=4)  # a parameter of membership function
		neural_net[0][index][0].b = numpy.random.uniform(low=-4, high=4)  # b parameter of membership function
		neural_net[0][index][0].antecedent_type = "A"

		# second neuron - its fuzzy set is set B from antecedent

		# ovo je B1 (tj Bi)
		neural_net[0][index][1].a = numpy.random.uniform(low=-4, high=4)  # a parameter of membership function
		neural_net[0][index][1].b = numpy.random.uniform(low=-4, high=4)  # b parameter of membership function
		neural_net[0][index][1].antecedent_type = "B"

	# postavljanje parametara neurona cetvrtog
	# sloja na random vrijednosti (p, q, r)
	for index, neuron in enumerate(layer4):
		neural_net[3][index].p = numpy.random.uniform(low=-20, high=20)
		neural_net[3][index].q = numpy.random.uniform(low=-20, high=20)
		neural_net[3][index].r = numpy.random.uniform(low=-20, high=20)

	return neural_net


def forward_pass(nn, x, y):
	"""
	
	:param nn: list of lists [[Neuron(), Neuron(), ...], [...]]
	:param x: float (input)
	:param y: float (other input)
	:return: float
	"""
	# this is loop for the first layer
	for index, neuron_couple in enumerate(nn[0]):  # for every neuron in input neurons

		# ovdje se vade Ai i Bi
		# iz para [Ai, Bi] (za svaki neuron u sljedecem sloju
		# ti treba par A1, B1 pa onda A2, B2 da bi izracunala t-normu
		# pogledaj shemu
		input_neuron_A = neuron_couple[0]
		input_neuron_B = neuron_couple[1]

		# checking if neurons have the right antecedent value
		# just in case, this can be removed later if proven good
		if input_neuron_A.antecedent_type != "A":
			raise ValueError("Input neuron A on index {} has wrong antecedent value!".format(index))
		if input_neuron_B.antecedent_type != "B":
			raise ValueError("Input neuron B on index {} has wrong antecedent value!".format(index))

		# found membership values for both x and y
		w_A = fuzzy.membership_function(x, input_neuron_A.a, input_neuron_A.b)  # fuzzy set A is connected to x
		w_B = fuzzy.membership_function(y, input_neuron_B.a, input_neuron_B.b)  # fuzzy set A is connected to y

		# setting outputs of input neurons to these
		# previously calculated weights
		nn[0][index][0].output = w_A  # here 0 means that these are input_neurons, index is the index of the rule
		nn[0][index][1].output = w_B  # and 0 and 1 (the last ones) are A and B fuzzy sets for each rule

	input_neurons = nn[0]
	for rule_index, rule in enumerate(nn[1]):  # for every neuron in second layer
		neuron_couple = input_neurons[rule_index]
		final_w = neuron_couple[0].output * neuron_couple[1].output  # output is the t-norm of the two weights
		# from couple of neurons A and B on the same index
		# THIS SHOULD BE REPLACED WITH T-NORM FUNCTION??
		nn[1][rule_index].output = final_w

	# for every neuron in third layer, calculate mean weight
	mean_weights = fuzzy.calculate_mean_weights([neuron.output for neuron in nn[1]])
	for index, neuron in enumerate(nn[2]):
		nn[2][index].output = mean_weights[index]  # set output of neuron to mean weight

	for index, neuron in enumerate(nn[3]):
		# ovo je srednja tezina za neuron na indeksu kojeg
		# trenutno promatram
		mean_weight_for_idx = nn[2][index].output

		# racuna se funkcija sa sadasnjim parametrima p, q, r i inputom x i outputom
		# y za ovaj sample
		f = fuzzy.calculate_f_for_rule(x, y, neuron.p, neuron.q, neuron.r)
		nn[3][index].f = f
		nn[3][index].output = mean_weight_for_idx * f

	# u zadnjem sloju je samo jedan neuron i
	# koristi se za sumu
	for index, neuron in enumerate(nn[4]):
		nn[4][index].output = sum([neuron_from_previous.output for neuron_from_previous in nn[3]])

	return nn[4][0].output


def calculate_MSE(samples, nn):
	"""
	
	:param samples: list of class Sample instances 
	:param nn: list of lists [[Neuron(), Neuron(), ...], [...]]
	:return: float
	"""
	sum_of_squares = 0
	for sample in samples:
		nn_output = forward_pass(nn, sample.x, sample.y)
		output_should_be = sample.f
		sum_of_squares += numpy.square(nn_output - output_should_be)
	return sum_of_squares/len(samples)


def backpropagation(samples, nn, number_of_rules, eta):
	"""
	
	:param samples: list of Sample class instances 
	:param nn: list of lists [[Neuron(), Neuron(), ...], [...]]
	:return: 
	"""
	aA_gradients = numpy.zeros(shape=(1, number_of_rules))
	aB_gradients = numpy.zeros(shape=(1, number_of_rules))
	bA_gradients = numpy.zeros(shape=(1, number_of_rules))
	bB_gradients = numpy.zeros(shape=(1, number_of_rules))

	# postoji toliko p, q i r koliko postoji neurona
	# u cetvrtom sloju nn[3]
	pi_gradients = numpy.zeros(shape=(1, number_of_rules))
	qi_gradients = numpy.zeros(shape=(1, number_of_rules))
	ri_gradients = numpy.zeros(shape=(1, number_of_rules))

	for sample in samples:

		# defining difference in outputs
		# first one is output from real network as it is now,
		# second one is output that we want network to give
		diff_outputs = forward_pass(nn, sample.x, sample.y) - sample.f

		# ovo su stvari koje se racunaju pojedinacno za svako pravilo
		for rule_idx in range(number_of_rules):

			# suma tezina za p, q, r
			w_sum = 0

			# ovdje se racuna derivacija izlaza po tezinama
			# iz drugog sloja (do_k/dw_i)
			do_dw = 0
			w_square_sum = 0
			for j in range(number_of_rules):

				do_dw += nn[1][j].output * (nn[3][rule_idx].f - nn[3][j].f)
				w_square_sum += numpy.square(nn[1][j].output)
				w_sum += nn[1][j].output

			do_dw = float(do_dw)/float(w_square_sum)

			mi_B = nn[0][rule_idx][1].output  # funkcija pripadnosti neizrazitog skupa Bi (ovdje je i = rule_idx)
			mi_A = nn[0][rule_idx][0].output  # funkcija pripadnosti neizrazitog skupa Ai (ovdje je i = rule_idx)
			b_A = nn[0][rule_idx][0].b  # parameter b za neizraziti skup Ai (ovdje je i = rule_idx)
			a_A = nn[0][rule_idx][0].a  # parameter a za neizraziti skup Ai (ovdje je i = rule_idx)
			b_B = nn[0][rule_idx][1].b  # parameter b za neizraziti skup Bi (ovdje je i = rule_idx)
			a_B = nn[0][rule_idx][1].a  # parameter a za neizraziti skup Bi (ovdje je i = rule_idx)


			aA_gradients[0][rule_idx] += diff_outputs * do_dw * mi_B * b_A * mi_A * (1 - mi_A)
			bA_gradients[0][rule_idx] += diff_outputs * do_dw * mi_B * (sample.x - a_A) * mi_A * (mi_A - 1)

			aB_gradients[0][rule_idx] += diff_outputs * do_dw * mi_A* b_B * mi_B * (1 - mi_B)
			bB_gradients[0][rule_idx] += diff_outputs * do_dw * mi_A * (sample.x - a_B) * mi_B * (mi_B - 1)

			w_i = nn[1][rule_idx].output
			pi_gradients[0][rule_idx] += float(diff_outputs * w_i * sample.x) / float(w_sum)
			qi_gradients[0][rule_idx] += diff_outputs * w_i * sample.y / float(w_sum)
			ri_gradients[0][rule_idx] += diff_outputs * w_i / float(w_sum)


	# postavljanje parametara neurona cetvrtog
	# sloja
	for index, neuron in enumerate(nn[3]):
		nn[3][index].p += eta * pi_gradients[0][index]
		nn[3][index].q += eta * qi_gradients[0][index]
		nn[3][index].r += eta * ri_gradients[0][index]

	# postavljanje parametara neurona prvog sloja
	for index, neuron in enumerate(nn[0]):
		nn[0][index][0].b += eta * bA_gradients[0][index]  # parameter b za neizraziti skup Ai (ovdje je i = index)
		nn[0][index][0].a += eta * aA_gradients[0][index]  # parameter a za neizraziti skup Ai (ovdje je i = index)
		nn[0][index][1].b += eta * bB_gradients[0][index]  # parameter b za neizraziti skup Bi (ovdje je i = index)
		nn[0][index][1].a += eta * aB_gradients[0][index]  # parameter a za neizraziti skup Bi (ovdje je i = index)

	return nn


def train(max_number_of_iterations, samples, nn, number_of_rules=8):
	for i in range(0, max_number_of_iterations):
		for sample in samples:
			nn = backpropagation([sample], nn, number_of_rules, 0.000001)
		if i % 100 == 0:
			mse = calculate_MSE(samples, nn)
			# false_mse = 1/mse
			print("Iteration: {}, MSE: {}".format(i, mse))


def main(number_of_rules=8):
	samples = generate_database()  # generating database of x, y, f

	nn = set_net_acrhitecture(number_of_rules)  # getting neural net of architecture based on number of rules
	iterations = 10000
	train(iterations, samples, nn, number_of_rules)


if __name__ == '__main__':
	main()
