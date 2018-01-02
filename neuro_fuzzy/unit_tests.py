import numpy
from neuro_fuzzy_main import membership_function, t_norm, calculate_f_for_rule, calculate_mean_weights, calculate_output


def test1(x, y, A, B):
	"""
	This test is made for only two rules, and randomly
	distributed weights.
	1. calculate value of the function for rule 1
	2. calculate value of the function for rule 2
	3. calculate mean weights
	4. by using mean weights, calculate final output
	"""
	p1, q1, r1 = 2, 3, 1
	f1 = calculate_f_for_rule(x, y, p1, q1, r1)
	p2, q2, r2 = 1, 1, 1
	f2 = calculate_f_for_rule(x, y, p2, q2, r2)
	initial_weights = numpy.random.random_sample(2, )
	rule_outputs = numpy.array([f1, f2])
	mean_weights = calculate_mean_weights(initial_weights, rule_outputs)
	output = calculate_output(mean_weights, rule_outputs)
	return output


if __name__ == '__main__':
	x = numpy.array([i for i in range(-4, 4)])
	y = numpy.array([i for i in range(-4, 4)])

	A = membership_function(x, a=2, b=3)
	B = membership_function(y, a=1, b=1)

	print(test1(x[0], y[1], A, B))
