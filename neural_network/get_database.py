import gui
import numpy
import matplotlib.pyplot as plt


def run_gui():
	"""
	Getting points from GUI.
	:return: [[x1, y1], [x2, y2], [x3, y3] ... ] list of lists
	"""
	gui.MyPaintApp().run()
	touch_points = numpy.array(gui.points)
	return touch_points


def normalize_points(touch_points):
	"""
	Function for normalizing points given by GUI.
	:param touch_points: [[x1, y1], [x2, y2], [x3, y3] ... ] list of lists 
	:return: numpy.array: [[x1, y1], [x2, y2], [x3, y3] ... ] list of lists
	"""
	Tc_x = numpy.mean(touch_points[:, 0])
	Tc_y = numpy.mean(touch_points[:, 1])
	normalized_touch_points = touch_points - numpy.array([Tc_x, Tc_y])
	max_x = numpy.amax(numpy.absolute(normalized_touch_points[:, 0]))
	max_y = numpy.amax(numpy.absolute(normalized_touch_points[:, 1]))
	m = max(max_x, max_y)
	normalized_touch_points = normalized_touch_points / m
	return normalized_touch_points


def calculate_distance(normalized_points):
	"""
	:param normalized_points: numpy.array: [[x1, y1], [x2, y2], [x3, y3] ... ] list of lists
	:return: float (total distance of gesture)
	"""
	D = 0
	for i in range(1, len(normalized_points)):
		dist = numpy.linalg.norm(normalized_points[i] - normalized_points[i-1])
		D += dist
	return D


def return_represent_points(normalized_points, M, D):
	"""
	:param normalized_points: numpy.array: [[x1, y1], [x2, y2], [x3, y3] ... ] list of lists
	:param M: int (number of representative points)
	:param D: float (total distance of a gesture)
	:return: numpy.array: [[x1, y1], [x2, y2], [x3, y3] ... ] list of lists
	"""
	represent_points = []
	distance_till_now = 0
	k = 0
	while k <= M:
		for index, point in enumerate(normalized_points):
			wanted_distance = k * D / (M - 1)  # distance that we want to keep between two points
			if index == 0:
				represent_points.append(point)
				k += 1
				continue
			else:
				distance_till_now += numpy.linalg.norm(represent_points[-1] - point)
				if distance_till_now >= wanted_distance:
					represent_points.append(point)
					k += 1
					continue
	return numpy.array(represent_points)


def test_plot_letters(normalized_points, represent_points):
	plt.figure(1)
	plt.plot(normalized_points[:, 0], normalized_points[:, 1], label="Normalized points")
	plt.plot(represent_points[:, 0], represent_points[:, 1], 'r', label="Represent points")
	plt.legend()
	plt.show()


def save_points_to_database(file_path, points, correct_output):
	"""
	Saving point coordinates to file specified with file_path.
	:param file_path: string (path to file)
	:param points: numpy.array: [[x1, y1], [x2, y2], [x3, y3] ... ] list of lists
	:param correct_output: str ("10000")
	"""
	with open(file_path, 'a') as file:
		file.write("\n")
		for point in points:
			file.write("{},{}\t".format(point[0], point[1]))
		file.write("{}".format(correct_output))


def defining_points_for_training(file, M):
	"""
	Function for easier creation of database.
	:param file: str (path to txt file of database)
	:param M: int (number of wanted represent points)
	"""
	# correct_output = input("Enter correct output:\n")
	correct_output = "00001"
	points = run_gui()
	normalized_points = normalize_points(points)
	D = calculate_distance(normalized_points)
	represent_points = return_represent_points(normalized_points, M, D)
	save_points_to_database(file, represent_points, correct_output)


if __name__ == '__main__':
	M = 50
	#file = "my_final_database.txt"
	defining_points_for_training(file, M)
	# points = run_gui()
	# normalized_points = normalize_points(points)
	# D = calculate_distance(normalized_points)
	# represent_points = return_represent_points(normalized_points, M, D)
	# test_plot_letters(normalized_points, represent_points)
