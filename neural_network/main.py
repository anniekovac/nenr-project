import gui
import numpy

if __name__ == '__main__':
	gui.MyPaintApp().run()
	touch_points = numpy.array(gui.points)
	Tc_x = numpy.mean(touch_points[:, 0])
	Tc_y = numpy.mean(touch_points[:, 1])
	normalized_touch_points = touch_points - numpy.array([Tc_x, Tc_y])
	max_x = numpy.amax(numpy.absolute(normalized_touch_points[:, 0]))
	max_y = numpy.amax(numpy.absolute(normalized_touch_points[:, 1]))
	m = max(max_x, max_y)
	normalized_touch_points = normalized_touch_points/m
	print(Tc_x, Tc_y)
	print(max_x, max_y)
