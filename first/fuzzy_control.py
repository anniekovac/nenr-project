from matplotlib import pyplot
from sets import MutableFuzzySet, CalculatedFuzzySet
from domain import SimpleDomain, CompositeDomain


def plot_fuzzy_set(fuzzy_set, y_axis_title="Membership function", x_axis_title="Domain"):
	yPoints = fuzzy_set.memberships
	xPoints = fuzzy_set.domain.domain_elements
	pyplot.stem(xPoints, yPoints)
	pyplot.xlabel(x_axis_title, fontsize=18)
	pyplot.ylabel(y_axis_title, fontsize=18)
	pyplot.show()


def fuzzification(singleton, first, last):
	"""
	This function is used for fuzzification of singleton value.
	It creates fuzzy set out of singleton value.
	:param singleton: int (single value of input variable) 
	:param first: int (first element of domain)
	:param last: int (last element of domain - not included in the domain) 
	:return: FuzzySet
	"""
	my_fuzzy_domain = SimpleDomain(first, last)
	my_fuzzy_set = MutableFuzzySet(my_fuzzy_domain, set_name="Input fuzzificated set")
	my_fuzzy_set.set_value_at(singleton, 1)
	return my_fuzzy_set

class Rule(CalculatedFuzzySet):
	"""
	Domena se definira izvan pravila, te se zatim zove pravilo.
	"""
	pass

if __name__ == "__main__":
	# domena ovisi o tome je li pravilo za akceleraciju
	# ili za kut
	angle_domain = SimpleDomain(-90, 91)
	my_angle_rule = Rule(angle_domain)
	my_singleton = 2
	my_fuzzyficated = fuzzification(my_singleton, 0, 5)
	plot_fuzzy_set(my_fuzzyficated)