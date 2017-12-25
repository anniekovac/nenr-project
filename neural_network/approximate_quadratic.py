import matplotlib.pyplot as plt
import numpy
from define_classes import Sample
from neural_network_util import get_neural_net_output, create_network_architecture, backpropagation


def approx_kvadrat(nn):
	"""
	Function for approximation of quadratic function.
	:param nn: list of lists
	:return: 
	"""
	inputs = numpy.array([[-1], [-0.8], [-0.6], [-0.4], [-0.2], [0.0], [0.2], [0.4], [0.6], [0.8], [1]])
	outputs = numpy.array([[1], [0.64], [0.36], [0.16], [0.04], [0], [0.04], [0.16], [0.36], [0.64], [1]])
	samples = [Sample(input, output) for (input, output) in zip(inputs, outputs)]

	inputs = numpy.array([item[0] for item in inputs])
	wanted_outputs = numpy.array([item[0] for item in outputs])
	nn_outputs = []
	for i in inputs:
		input = [i]
		output = get_neural_net_output(input, nn)
		nn_outputs.append(output)
	nn_outputs = numpy.array(nn_outputs)

	brojac = 40000
	while brojac:
		nn = backpropagation(0.1, samples, nn)
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


if __name__ == '__main__':

	arch_numbers = [1, 6, 6, 6, 1]
	list_of_lists = create_network_architecture(arch_numbers)
	approx_kvadrat(list_of_lists)