from domain import SimpleDomain


class FuzzySet(object):

	#domain = []
	#memberships = []

	def print_fuzzy_set(self):
		"""
		Printing fuzzy set (its domain and
		values for every element of domain).
		"""
		print("Set {}:".format(self.set_name))
		for index, element in enumerate(self.domain.domain_elements):
			print("d({})={}".format(element, self.memberships[index]))

	def get_domain(self):
		"""
		:return: IDomain 
		"""
		return self.domain

	def get_value_at(self, domain_element):
		"""
		"Asking" domain for value of domain_element.
		:param domain_element: DomainElement 
		:return: double
		"""
		index = self.domain.index_of_element(domain_element)
		return self.memberships[index]



class MutableFuzzySet(FuzzySet):
	def __init__(self, domain, set_name):
		self.domain = domain
		self.memberships = [0]*len(self.domain.domain_elements)
		self.set_name = set_name

	def set_value_at(self, domain_element, element_value):
		"""
		:param domain_element: DomainElement 
		:param element_value: double
		:return: MutableFuzzySet
		"""
		index = self.domain.index_of_element(domain_element)
		self.memberships[index] = element_value
		return self

def unitary_function(domain):
	"""
	Setting double values to a list based on
	domain.domain_elements list.
	:param domain: Domain
	:return: list of doubles
	"""
	### STEP FUNCTION
	# this is approximately the middle
	middle = int(float(len(domain.domain_elements))/2)
	output_list = [0 if index < middle else 1 for (index, element) in enumerate(domain.domain_elements)]
	return output_list

class CalculatedFuzzySet(FuzzySet):

	def __init__(self, domain, unitary_function):
		self.domain = domain
		self.unitary_function = unitary_function

if __name__ == "__main__":
	simple_domain = SimpleDomain(1, 5, "Pero")
	my_fuzzy = MutableFuzzySet(simple_domain, "PeroSet")
	my_fuzzy.set_value_at(1, 0.4)
	my_fuzzy.set_value_at(2, 0.9)
	#my_fuzzy.print_fuzzy_set()
	unitary_function(simple_domain)