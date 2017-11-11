import copy
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
	defuzzyficated = int(defuzzyfication(fuzzy_set))
	yPoints = fuzzy_set.memberships
	xPoints = fuzzy_set.domain.domain_elements
	pyplot.stem(xPoints, yPoints)
	pyplot.xlabel(x_axis_title, fontsize=16)
	pyplot.ylabel(y_axis_title, fontsize=16)
	pyplot.title("Defuzzyficirana vrijednost skupa: {}".format(defuzzyficated))
	pyplot.show()


def defuzzyfication(fuzzy_set):
	"""
	Function used for defuzzyfication of a fuzzy set. This means that
	we choose one value from a whole set and send it as a representative
	on the output. This is done according to COA procedure.
	:param fuzzy_set: FuzzySet class instance 
	:return: int
	"""
	# fuzzy_set.print_fuzzy_set()
	membership_sum = sum(fuzzy_set.memberships)
	numerator = sum([value * domain_element for (value, domain_element) in
					 zip(fuzzy_set.memberships, fuzzy_set.domain.domain_elements)])
	# return numerator / membership_sum
	if membership_sum == 0:
		return 0
	else:
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
		# first, finding minimum value with which some
		# input value belongs to its set
		minimum = 1
		for key, value in self.instant_values.items():
			fuzzy_set = self.fuzzy_sets[key]
			if fuzzy_set.member_dict[value] < minimum:
				minimum = fuzzy_set.member_dict[value]

		# searching for the set that is result of this implication
		key = [value for (item, value) in self.fuzzy_sets.items() if "rule" in item]
		if len(key) != 1:
			raise ValueError
		# this is my result, if minimum == 1
		fuzzy_rule = key[0]
		if minimum == 1:
			return fuzzy_rule
		else:
			fuzzy_rule = copy.deepcopy(fuzzy_rule)

		# if my minimum is smaller than 1,
		# we need to "cut" the existing rule on the place where the minimum is placed
		for (idx, item) in enumerate(fuzzy_rule.memberships):
			if item > minimum:
				fuzzy_rule.memberships[idx] = minimum
		fuzzy_rule.update_member_dict()
		return fuzzy_rule


class AccRuleBase(object):
	def __init__(self):
		self.instant_values = dict()

		self.rule_acc = Rule(acceleration_domain, L=universal_distance_with_a_twist, D=universal_distance,
							 LK=universal_distance, DK=universal_distance, S=correct_direction, V=universal_velocity, A_rule=my_acc_set)

	def update_input_values_for_rules(self):
		"""
		Updating input values in each rule.
		"""
		self.rule_acc.instant_values = self.instant_values

	def calculate_rule_union(self):
		"""
		Calculating final fuzzy set that will be result of all rules combined together.
		:return: FuzzySet
		"""
		result = self.rule_acc.calculate_fuzzy_rule()
		#plot_fuzzy_set(result)
		return result


class RuddRuleBase(object):
	def __init__(self):
		self.instant_values = dict()

		# RULES
		self.rule_sharp_right = Rule(angle_domain, L=dangerously_close, D=universal_distance,
									 LK=dangerously_close,
									 DK=universal_distance, S=correct_direction, V=universal_velocity,
									 K_rule=sharp_right)

		self.rule_sharp_left = Rule(angle_domain, L=universal_distance, D=dangerously_close,
									LK=universal_distance,
									DK=dangerously_close, S=correct_direction, V=universal_velocity, K_rule=sharp_left)

		self.rule_keep_direction = Rule(angle_domain, L=not_close, D=not_close, LK=not_close, DK=not_close, S=correct_direction,
										V=universal_velocity, K_rule=keep_direction)

		# self.rule_keep_direction2 = Rule(angle_domain, L=dangerously_close, D=dangerously_close, LK=universal_distance,
		# 								DK=universal_distance, S=correct_direction,
		# 								V=universal_velocity, K_rule=keep_direction)

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
		result = zadeh_or(self.rule_sharp_left.calculate_fuzzy_rule(), self.rule_sharp_right.calculate_fuzzy_rule())
		#plot_fuzzy_set(result)
		return result
