from matplotlib import pyplot
from sets import MutableFuzzySet, CalculatedFuzzySet
from domain import SimpleDomain
from operations import zadeh_or
from fuzzy_inputs import *


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


class AccRuleBase(object):
	def __init__(self):
		self.instant_values = dict()


class RuddRuleBase(object):
	def __init__(self):
		self.instant_values = dict()

		# RULES
		self.rule_sharp_right = Rule(angle_domain, L=dangerously_close, D=not_close,
									 LK=zadeh_or(dangerously_close, close),
									 DK=not_close, S=correct_direction, V=small_velocity, K_rule=sharp_right)

		self.rule_sharp_left = Rule(angle_domain, L=dangerously_close, D=not_close,
									LK=zadeh_or(dangerously_close, close),
									DK=not_close, S=correct_direction, V=small_velocity, K_rule=sharp_right)

	def update_input_values_for_rules(self):
		"""
		Updating input values in each rule.
		"""
		self.rule_sharp_right.instant_values = self.instant_values
		self.rule_sharp_left.instant_values = self.instant_values

	def calculate_rule_union(self):
		"""
		Calculating final fuzzy set that will be result of all rules combined together.
		:return: FuzzySet
		"""
		result = zadeh_or(self.rule_sharp_left, self.rule_sharp_right)
		return result
