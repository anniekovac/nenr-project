import itertools
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
		if fuzzy_set.member_dict[element] != fuzzy_set.member_dict[(b, a)]:
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

def is_max_min_transitive(fuzzy_set):
	"""
	This function checks if relation given to it (fuzzy_set)
	is max min transitive.
	:param fuzzy_set: FuzzySet instance
	:return: boolean (True or False)
	"""
	original_domain_elements = fuzzy_set.domain.list_of_domains[0].domain_elements
	list_for_cartesian = [original_domain_elements]*3

	for element in itertools.product(*list_for_cartesian):
		x = element[0]
		y = element[1]
		z = element[2]

		mi_xz = fuzzy_set.member_dict[(x, z)]
		mi_xy = fuzzy_set.member_dict[(x, y)]
		mi_yz = fuzzy_set.member_dict[(y, z)]

		if mi_xz < min(mi_xy, mi_yz):
			return False

	return True

def is_fuzzy_equivalence(fuzzy_set):
	"""
	Checking if relation "fuzzy_set" is reflexive, symmetric 
	and max-min transitive.
	:param fuzzy_set: FuzzySet instance
	:return: boolean
	"""
	if not is_symmetric(fuzzy_set):
		return False
	if not is_reflexive(fuzzy_set):
		return False
	if not is_max_min_transitive(fuzzy_set):
		return False
	return True


def composition_of_binary_relations(fuzzy_set1, fuzzy_set2):
	"""
	Calculating composition of two relations.
	:param fuzzy_set1: FuzzySet (defined on domain UxV)
	:param fuzzy_set2: FuzzySet (defined on domain VxW)
	:return: FuzzySet (defined on domain UxW)
	"""
	domain_elements1 = fuzzy_set1.domain.domain_elements
	domain_elements2 = fuzzy_set2.domain.domain_elements
	for element in domain_elements1:
		my_row = [item for item in domain_elements1 if element[0] == item[0]]
		for element2 in domain_elements2:
			my_col = [item for item in domain_elements2 if element2[1] == item[1]]
			import pdb; pdb.set_trace()

if __name__ == "__main__":
	simple_domain = SimpleDomain(0, 3, "Pero")
	simple_domain2 = SimpleDomain(0, 3, "Branko")
	compos = CompositeDomain([simple_domain, simple_domain2], "Composite")
	my_set = CalculatedFuzzySet(compos)
	# print(is_U_times_relation(my_set))

	mutable_set = MutableFuzzySet(compos)
	mutable_set.set_value_at((0, 0), 1)
	mutable_set.set_value_at((0, 1), 0.5)
	mutable_set.set_value_at((1, 0), 0.5)
	mutable_set.set_value_at((1, 1), 1)
	mutable_set.set_value_at((1, 2), 0.7)
	mutable_set.set_value_at((2, 1), 0.71)
	mutable_set.set_value_at((2, 2), 1)

	# print(is_symmetric(mutable_set))
	print(is_reflexive(mutable_set))
	is_max_min_transitive(mutable_set)
	prvi = SimpleDomain(0, 2, "Pero")
	prvi2 = SimpleDomain(0, 3, "Pero")
	drugi = SimpleDomain(0, 3, "Branko")
	drugi2 = SimpleDomain(0, 4, "Branko")
	compos1 = CompositeDomain([prvi, prvi2], "Composite1")
	compos2 = CompositeDomain([drugi, drugi2], "Composite2")
	my_fuzz1 = CalculatedFuzzySet(compos1)
	my_fuzz2 = CalculatedFuzzySet(compos2)
	composition_of_binary_relations(my_fuzz1, my_fuzz2)