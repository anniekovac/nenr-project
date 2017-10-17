from sets import CalculatedFuzzySet
from domain import SimpleDomain


def zadeh_not(fuzzy_set):
	"""
	Implementation of Zadehs not function.
	This function receives FuzzySet and returns new instance of 
	FuzzySet class with operation Zadeh not calculated for 
	memberships values of input FuzzySet.
	:param fuzzy_set: instance of FuzzySet
	:return: fuzzy_not
	"""
	new_memberships = [1-value for value in fuzzy_set.memberships]
	fuzzy_not = CalculatedFuzzySet(fuzzy_set.domain)
	fuzzy_not.memberships = new_memberships
	fuzzy_not.set_name = "ZadehNot_{}".format(fuzzy_set.set_name)
	return fuzzy_not

def zadeh_or(fuzzy_set1, fuzzy_set2):
	"""
	Implementation of Zadehs or function.
	This function receives two instances of FuzzySet 
	and returns new instance of FuzzySet class with 
	operation Zadeh or calculated for 
	memberships values of two input FuzzySets.
	:param fuzzy_set1: instance of FuzzySet
	:param fuzzy_set2: instance of FuzzySet
	:return: fuzzy_or: instance of FuzzySet
	"""
	new_memberships = [max(value1, value2) for (value1, value2) in zip(fuzzy_set1.memberships, fuzzy_set2.memberships)]
	fuzzy_or = CalculatedFuzzySet(fuzzy_set1.domain)
	fuzzy_or.memberships = new_memberships
	fuzzy_or.set_name = "ZadehOr_{}_{}".format(fuzzy_set1.set_name, fuzzy_set2.set_name)
	return fuzzy_or

def zadeh_and(fuzzy_set1, fuzzy_set2):
	"""
	Implementation of Zadehs and function.
	This function receives two instances of FuzzySet 
	and returns new instance of FuzzySet class with 
	operation Zadeh and calculated for 
	memberships values of two input FuzzySets.
	:param fuzzy_set1: instance of FuzzySet
	:param fuzzy_set2: instance of FuzzySet
	:return: fuzzy_and: instance of FuzzySet
	"""
	new_memberships = [min(value1, value2) for (value1, value2) in zip(fuzzy_set1.memberships, fuzzy_set2.memberships)]
	fuzzy_and = CalculatedFuzzySet(fuzzy_set1.domain)
	fuzzy_and.memberships = new_memberships
	fuzzy_and.set_name = "ZadehAnd_{}_{}".format(fuzzy_set1.set_name, fuzzy_set2.set_name)
	return fuzzy_and

def hamTnorm(fuzzy_set1, fuzzy_set2, my_param=0.5):
	"""
	Implementation of Hamachers t-norm.
	This function receives two instances of FuzzySet 
	and returns new instance of FuzzySet class with 
	operation Hamachers t-norm calculated for 
	memberships values of two input FuzzySets.
	:param fuzzy_set1: instance of FuzzySet
	:param fuzzy_set2: instance of FuzzySet
	:return: fuzzy_t: instance of FuzzySet
	"""
	new_memberships = [0]*len(fuzzy_set1.domain.domain_elements)
	for index, (value1, value2) in enumerate(zip(fuzzy_set1.memberships, fuzzy_set2.memberships)):
		new_memberships[index] = (value1*value2)/(my_param + (1-my_param)*(value1+value2-value1*value2))
	fuzzy_t = CalculatedFuzzySet(fuzzy_set1.domain)
	fuzzy_t.memberships = new_memberships
	fuzzy_t.set_name = "Ham_T_norm_{}_{}".format(fuzzy_set1.set_name, fuzzy_set2.set_name)
	return fuzzy_t

def hamSnorm(fuzzy_set1, fuzzy_set2, my_param=0.5):
	"""
	Implementation of Hamachers s-norm.
	This function receives two instances of FuzzySet 
	and returns new instance of FuzzySet class with 
	operation Hamachers s-norm calculated for 
	memberships values of two input FuzzySets.
	:param fuzzy_set1: instance of FuzzySet
	:param fuzzy_set2: instance of FuzzySet
	:return: fuzzy_s: instance of FuzzySet
	"""
	new_memberships = [0]*len(fuzzy_set1.domain.domain_elements)
	for index, (value1, value2) in enumerate(zip(fuzzy_set1.memberships, fuzzy_set2.memberships)):
		new_memberships[index] = (value1+value2-(2-my_param)*(value1*value2))/(1 - (1-my_param)*value1*value2)
	fuzzy_s = CalculatedFuzzySet(fuzzy_set1.domain)
	fuzzy_s.memberships = new_memberships
	fuzzy_s.set_name = "Ham_T_norm_{}_{}".format(fuzzy_set1.set_name, fuzzy_set2.set_name)
	return fuzzy_s

if __name__ == "__main__":
	my_domain = SimpleDomain(0, 20)
	my_calculated = CalculatedFuzzySet(my_domain)
	my_calculated2 = CalculatedFuzzySet(my_domain, my_func="l")

	my_set = zadeh_or(my_calculated, my_calculated2)
	t_norm = hamTnorm(my_calculated, my_calculated2)
	s_norm = hamSnorm(my_calculated2, my_calculated)
