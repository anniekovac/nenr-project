from matplotlib import pyplot
from sets import MutableFuzzySet, CalculatedFuzzySet
from domain import SimpleDomain, CompositeDomain


def plot_fuzzy_set(fuzzy_set, y_axis_title="Membership function", x_axis_title="Domain"):
	"""
	Function that plots fuzzy set graphically.
	:param fuzzy_set: FuzzySet class instance
	:param y_axis_title: str (if you want some other title for your Y axis)
	:param x_axis_title: str (if you want some other title for your X axis)
	:return: None
	"""
	yPoints = fuzzy_set.memberships
	xPoints = fuzzy_set.domain.domain_elements
	pyplot.stem(xPoints, yPoints)
	pyplot.xlabel(x_axis_title, fontsize=16)
	pyplot.ylabel(y_axis_title, fontsize=16)
	pyplot.show()


def fuzzyfication(singleton, first, last):
	"""
	This function is used for fuzzyfication of singleton value.
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


def defuzzyfication(fuzzy_set):
	"""
	Function used for defuzzyfication of a fuzzy set. This means that
	we choose one value from a whole set and send it as a representative
	on the output. This is done according to COA procedure.
	:param fuzzy_set: FuzzySet class instance 
	:return: int
	"""
	membership_sum = sum(fuzzy_set.memberships)
	numerator = sum([value*domain_element for (value, domain_element) in zip(fuzzy_set.memberships, fuzzy_set.domain.domain_elements)])
	return numerator/membership_sum


class Rule(CalculatedFuzzySet):
	"""
	Domena se definira izvan pravila, te se zatim zove pravilo.
	"""
	def __init__(self, domain, **kwargs):
		"""
		:param domain: Domain class instance 
		:param kwargs: FuzzySets (for example "L", "DK" etc)
		"""
		CalculatedFuzzySet.__init__(self, domain)
		#import pdb; pdb.set_trace()




if __name__ == "__main__":

	angle_domain = SimpleDomain(-90, 91)
	distance_domain = SimpleDomain(0, 1301)
	dangerously_close = CalculatedFuzzySet(distance_domain)
	dangerously_close.set_calculated_memberships("l", alpha=0.1, beta=0.7)
	close = CalculatedFuzzySet(distance_domain, "l")
	close.set_calculated_memberships("l", alpha=0.4, beta=0.7)

	# pozitivni kutevi uzrokuju skretanje ulijevo
	# negativni kutevi uzrokuju skretanje udesno
	sharp_right = CalculatedFuzzySet(angle_domain)
	sharp_right.set_calculated_memberships("l", alpha=0.2, beta=0.4)
	sharp_left = CalculatedFuzzySet(angle_domain)
	sharp_left.set_calculated_memberships("gamma", alpha=0.6, beta=0.8)
	plot_fuzzy_set(sharp_left)



