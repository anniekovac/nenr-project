import gui
import numpy


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


if __name__ == '__main__':
	touch_points = run_gui()
	points = run_gui()
	normalized_points = normalize_points(points)
	D = calculate_distance(normalized_points)
	print(D)