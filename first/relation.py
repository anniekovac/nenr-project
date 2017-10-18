from domain import CompositeDomain
from domain import SimpleDomain
from sets import CalculatedFuzzySet
from sets import MutableFuzzySet

def is_U_times_relation(fuzzy_set):
	"""
	Checks if domain of the fuzzy set given
	as input argument iz Cartesian product (UxU).
	:param fuzzy_set: FuzzySet instance
	:return: boolean (True or False)
	"""
	for element in fuzzy_set.domain.domain_elements:
		# checking if every element is a tuple of length 2
		if not (isinstance(element, tuple) and len(element) == 2):
			return False
	# checking if both domains that consists CompositeDomain contain the same domain_elements
	# (we already know that fuzzy_set.domain.list_of_domains contains only two elements
	# because we checked it in the first condition above)
	if fuzzy_set.domain.list_of_domains[0].domain_elements != fuzzy_set.domain.list_of_domains[1].domain_elements:
		return False
	return True

def is_symmetric(fuzzy_set):
	"""
	This function checks if relation given with input argument "fuzzy_set"
	is symmetric. This fuzzy_set input argument
	should be defined in the domain that is actually Cartesian product.
	This means that domain elements should be pair of numbers in tuple.
	:param fuzzy_set: FuzzySet instance 
	:return: boolean (True or False)
	"""
	for element in fuzzy_set.domain.domain_elements:
		a = element[0]
		b = element[1]
		index = fuzzy_set.domain.index_of_element(element)
		index2 = fuzzy_set.domain.index_of_element((b,a))
		if not fuzzy_set.memberships[index] == fuzzy_set.memberships[index2]:
			return False
	return True

def is_reflexive(fuzzy_set):
	"""
	This function should check if relation given to 
	it in the shape of "fuzzy_set" argument is reflexive.
	:param fuzzy_set: FuzzySet instance
	:return: boolean (True or False)
	"""
	for index, element in enumerate(fuzzy_set.domain.domain_elements):
		if element[0] == element[1]:
			if not fuzzy_set.memberships[index] == 1:
				return False
	return True


if __name__ == "__main__":
	simple_domain = SimpleDomain(0, 3, "Pero")
	simple_domain2 = SimpleDomain(0, 3, "Branko")
	compos = CompositeDomain([simple_domain, simple_domain2], "Composite")
	my_set = CalculatedFuzzySet(compos)
	#print(is_U_times_relation(my_set))

	mutable_set = MutableFuzzySet(compos)
	mutable_set.set_value_at((0, 0), 1)
	mutable_set.set_value_at((0, 1), 0.5)
	mutable_set.set_value_at((1, 0), 0.5)
	mutable_set.set_value_at((1, 1), 1)
	mutable_set.set_value_at((1, 2), 0.7)
	mutable_set.set_value_at((2, 1), 0.71)
	mutable_set.set_value_at((2, 2), 1)

	#print(is_symmetric(mutable_set))
	print(is_reflexive(mutable_set))
