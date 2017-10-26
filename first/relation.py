import itertools
import numpy

import tests_relation
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
	# extracting domain elements of both sets
	domain_elements1 = fuzzy_set1.domain.domain_elements
	domain_elements2 = fuzzy_set2.domain.domain_elements

	# defining UxW space in which composition will be defined
	u = fuzzy_set1.domain.get_component(0).domain_elements
	w = fuzzy_set2.domain.get_component(1).domain_elements

	# creating two SimpleDomain instances which will
	# create CompositeDomain

	# REMINDER: SimpleDomain(first, last) does NOT
	# include last element, so there is +1 (so it will be included)
	u_domain = SimpleDomain(u[0], u[-1]+1)
	w_domain = SimpleDomain(w[0], w[-1]+1)

	len_u = len(u)+1
	len_w = len(w)+1

	# creating empty array in domain UxW filled with zeros
	my_array = numpy.zeros(shape=(len_u, len_w))

	# iterating over domain elements of first part of
	# composite domain
	for element in domain_elements1:

		# extracting row
		my_row = [item for item in domain_elements1 if element[0] == item[0]]

		# iterating over domain elements of second part of composite domain
		for element2 in domain_elements2:

			# extracting column
			my_col = [item for item in domain_elements2 if element2[1] == item[1]]

			# extracting row and column values (these are the values
			# that we will consider in finding maximum of minimum)
			row_values = [fuzzy_set1.member_dict[item] for item in my_row]
			col_values = [fuzzy_set2.member_dict[item] for item in my_col]

			# initializing max_min value to zero
			max_min = 0
			for row, col in zip(row_values, col_values):
				# if min(row, col) is larger than
				# current max_min, then set max_min to
				# to new value
				if min(row, col) > max_min:
					max_min = min(row, col)

			# my index has the row index from the first element,
			# and column index from the second element
			my_index = (element[0], element2[1])

			# set element in my_array on index element[0], element2[1]
			# to this calculated max_min value
			my_array[element[0], element2[1]] = max_min

	# creating composite domain out of two simple domains
	# created in the beginning
	compos_domain = CompositeDomain([u_domain, w_domain])

	# initializing MutableFuzzy set with compos_domain UxW
	composition_fuzzy = MutableFuzzySet(compos_domain)

	# writing calculated values to new composition_fuzzy
	# FuzzySet
	for (x, y), value in numpy.ndenumerate(my_array):
		try:
			composition_fuzzy.set_value_at((x, y), value)
		except ValueError:
			pass
	return composition_fuzzy

if __name__ == "__main__":

	tests_relation.test_relation_characteristics()
	# tests_relation.test_composition()
	# tests_relation.test_composition2()
	# tests_relation.test_equivalence()