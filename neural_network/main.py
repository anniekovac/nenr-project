import numpy
import os
import get_database
from define_classes import Sample
from neural_network_util import get_neural_net_output, create_network_architecture, train


def get_database_from_txt(path_to_db):
	"""
	Function used for importing database of greek letters.
	:param path_to_db: str (path to database you want to import)
	:return: numpy.array
	"""
	with open(path_to_db, 'r') as database:
		samples = []
		for line in database:
			final_points = []
			points = line.split("\t")
			for item in points:
				if "," in item:
					points = [float(i) for i in item.split(",")]
					final_points.append([points[0]])
					final_points.append([points[1]])
				else:
					str_output = item.rstrip("\n")
					output = [int(number) for number in str_output]
			final_points = numpy.array(final_points)
			output = numpy.array(output)
			sample = Sample(final_points, output)
			samples.append(sample)
		samples = numpy.array(samples)
	return samples


def get_user_input(M):
	"""
	Collect users input by using GUI. GUI will open, 
	user can draw wanted letter and GUI will return 
	points in which gesture was made.
	:param M: int (number of represent points)
	:return: numpy.array
	"""
	points = get_database.run_gui()
	normalized_points = get_database.normalize_points(points)
	D = get_database.calculate_distance(normalized_points)
	represent_points = get_database.return_represent_points(normalized_points, M, D)
	return represent_points


def translate_output(final_inputs, nn):
	"""
	Decide what letter is the output of neural network.
	:param final_inputs: 
	:param nn: list of lists (neural network architecture)
	:return: str (classified letter)
	"""
	output_list = get_neural_net_output(final_inputs, nn)
	decode_output = ["alpha", "beta", "gamma", "delta", "epsilon"]
	return decode_output[numpy.argmax(output_list)]


# TODO: implement possibility of multiple outputs in GUI
# TODO: implement 3 different algorithms of learning
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
	arch_numbers = [100, 6, 5]
	list_of_lists = create_network_architecture(arch_numbers)
	samples = get_database_from_txt(os.path.join(os.getcwd(), "greek_letters_database.txt"))
	nn = train(samples, list_of_lists)
	radi = True
	while radi:
		represent_points = get_user_input(M)
		final_inputs = []
		for x, y in represent_points:
			final_inputs.append(x)
			final_inputs.append(y)
		final_inputs = numpy.array(final_inputs)
		print(translate_output(final_inputs, nn))
		radi = input("Hoces li jos (True ili False):\n")
		radi = bool(radi)