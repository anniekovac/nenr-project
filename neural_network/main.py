import gui
import numpy
from pprint import pprint as pp

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
	represent_points.append(normalized_points[0])
	# k = 1
	p1 = 0
	p2 = 1
	offset = 0
	while(len(represent_points) < M):
		#wanted_distance = k*D/(M-1)  # distance that we want to keep between two points
		wanted_distance = D / (M - 1)  # distance that we want to keep between two points
		wanted_distance_with_offset = wanted_distance + offset
		try:
			first_point = normalized_points[p1]  # first normalized point after the one we are looking at
			second_point = normalized_points[p2]  # second normalized point after the one we are looking at
		except:
			print("da")
		last_repr_point = represent_points[-1]  # last added represent_point
		dist_to_first = numpy.linalg.norm(last_repr_point-first_point)
		dist_to_second = dist_to_first + numpy.linalg.norm(first_point-second_point)
		if dist_to_second < wanted_distance_with_offset:
			p1 = p2
			p2 += 1
			continue
		else:
			if numpy.absolute(wanted_distance_with_offset-dist_to_first) < numpy.absolute(wanted_distance_with_offset-dist_to_second):
				offset = (wanted_distance_with_offset - dist_to_first)
				represent_points.append(first_point)
				p1 += 1
				p2 = p1 + 1
			else:
				represent_points.append(second_point)
				offset = wanted_distance_with_offset - dist_to_second
				p1 = p2 + 1
				p2 = p1 + 1
			#k += 1
	pp(represent_points)


def save_points_to_database(file_path, points):
	"""
	Saving point coordinates to file specified with file_path.
	:param file_path: string (path to file)
	:param points: numpy.array: [[x1, y1], [x2, y2], [x3, y3] ... ] list of lists
	"""
	with open(file_path, 'w') as file:
		for point in points:
			file.write("{}	{}\n".format(point[0], point[1]))


if __name__ == '__main__':
	M = 50

	touch_points = run_gui()
	points = run_gui()
	normalized_points = normalize_points(points)
	D = calculate_distance(normalized_points)
	return_represent_points(normalized_points, M, D)
	print(len(normalized_points))
	save_points_to_database("database.txt", normalized_points)