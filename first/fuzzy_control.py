from sets import MutableFuzzySet, CalculatedFuzzySet
from domain import SimpleDomain, CompositeDomain


def fuzzification(singleton, first, last):
	"""
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
	angle_domain = SimpleDomain(-90, 90)
	my_angle_rule = Rule(angle_domain)
	my_angle_rule.print_fuzzy_set()