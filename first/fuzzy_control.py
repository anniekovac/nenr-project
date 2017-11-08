from matplotlib import pyplot
from sets import MutableFuzzySet, CalculatedFuzzySet
from domain import SimpleDomain, CompositeDomain
from operations import zadeh_not


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
	numerator = sum([value * domain_element for (value, domain_element) in
					 zip(fuzzy_set.memberships, fuzzy_set.domain.domain_elements)])
	return numerator / membership_sum


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
		self.instant_values = dict()
		self.fuzzy_sets = kwargs

	def calculate_fuzzy_rule(self):
		minimum = 1
		for key, value in self.instant_values.items():
			fuzzy_set = self.fuzzy_sets[key]
			if fuzzy_set.member_dict[value] < minimum:
				minimum = fuzzy_set.member_dict[value]

		key = [value for (item, value) in self.fuzzy_sets.items() if "rule" in item]
		if len(key) != 1:
			raise ValueError
		fuzzy_rule = key[0]

		for (idx, item) in enumerate(fuzzy_rule.memberships):
			if item > minimum:
				fuzzy_rule.memberships[idx] = minimum
		fuzzy_rule.update_member_dict()


if __name__ == "__main__":
	# defining domains
	angle_domain = SimpleDomain(-90, 91)
	distance_domain = SimpleDomain(0, 701)  # it is enough for distance domain to have 700 pixels
	velocity_domain = SimpleDomain(20, 51)
	direction_domain = SimpleDomain(0, 2)
	acceleration_domain = SimpleDomain(-10, 11)

	# defining direction implications
	correct_direction = MutableFuzzySet(direction_domain)
	correct_direction.set_value_at(0, 0)
	correct_direction.set_value_at(1, 1)

	# defining distance implications
	dangerously_close = CalculatedFuzzySet(distance_domain)
	dangerously_close.set_calculated_memberships("l", alpha=0.1, beta=0.2)
	close = CalculatedFuzzySet(distance_domain)
	close.set_calculated_memberships("l", alpha=0.1, beta=0.35)
	not_close = zadeh_not(close)
	not_dangerously_close = zadeh_not(dangerously_close)

	# defining angle implications
	# pozitivni kutevi uzrokuju skretanje ulijevo
	# negativni kutevi uzrokuju skretanje udesno
	sharp_right = CalculatedFuzzySet(angle_domain)
	sharp_right.set_calculated_memberships("l", alpha=0.2, beta=0.4)
	sharp_left = CalculatedFuzzySet(angle_domain)
	sharp_left.set_calculated_memberships("gamma", alpha=0.6, beta=0.8)

	# defining velocity implications
	small_velocity = CalculatedFuzzySet(velocity_domain)
	small_velocity.set_calculated_memberships("l", alpha=0.2, beta=0.3)
	large_velocity = CalculatedFuzzySet(velocity_domain)
	large_velocity.set_calculated_memberships("gamma", alpha=0.68, beta=0.7)

	# defining acceleration implications
	large_acceleration = CalculatedFuzzySet(acceleration_domain)
	large_acceleration.set_calculated_memberships("gamma", alpha=0.68, beta=0.7)

	# print(defuzzyfication(sharp_left))
	# print(defuzzyfication(sharp_right))
	# print(defuzzyfication(dangerously_close))
	# print(defuzzyfication(close))

	# plot_fuzzy_set(close)
	my_rule = Rule(acceleration_domain, L=close, D=not_close, LK=not_close, DK=not_close, V=small_velocity,
				   S=correct_direction, Arule=large_acceleration)
	my_rule.instant_values = dict(L=100, D=100, LK=100, DK=100, V=25, S=1)
	# print(my_rule.instant_values)
	my_rule.calculate_fuzzy_rule()
