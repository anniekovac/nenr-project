from domain import SimpleDomain


class FuzzySet(object):

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
	def __init__(self, domain, set_name=""):
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


def _step_function(domain):
	"""
	:param domain: Domain 
	:return: list of doubles
	"""
	# this is approximately the middle
	middle = int(float(len(domain.domain_elements))/2)
	output_list = [0 if index < middle else 1 for (index, element) in enumerate(domain.domain_elements)]
	return output_list


def _gamma_function(domain):
	"""
	Implementation of gamma function.
	It returns list of values that corresponds
	to domain.domain_elements.
	In this implementation alpha_param = 0.3
	and beta_param = 0.6.
	:param domain: Domain
	:return: list of doubles
	"""
	alpha = int(0.3*len(domain.domain_elements))
	beta = int(0.6*len(domain.domain_elements))
	output_list = [0]*len(domain.domain_elements)

	for index, element in enumerate(domain.domain_elements):
		if element < alpha:
			value = 0.0
		if element >= alpha and element < beta:
			value = (element - alpha)/(beta - alpha)
		if element >= beta:
			value = 1.0
		output_list[index] = value

	return output_list


def _lambda_function(domain):
	"""
	Implementation of lambda function.
	It returns list of values that corresponds
	to domain.domain_elements.
	In this implementation alpha_param = 0.25, 
	beta_param = 0.5 and gamma_param = 0.75.
	:param domain: Domain
	:return: list of doubles
	"""
	alpha = int(0.25*len(domain.domain_elements))
	beta = int(0.5*len(domain.domain_elements))
	gamma = int(0.75*len(domain.domain_elements))
	output_list = [0]*len(domain.domain_elements)

	for index, element in enumerate(domain.domain_elements):
		if element < alpha:
			value = 0.0
		if element >= alpha and element < beta:
			value = (element - alpha)/(beta - alpha)
		if element >= beta and element < gamma:
			value = (gamma - element) / (gamma - beta)
		if element >= gamma:
			value = 1.0
		output_list[index] = value

	return output_list


def _l_function(domain):
	"""
	Implementation of L function.
	It returns list of values that corresponds
	to domain.domain_elements.
	In this implementation alpha_param = 0.3, 
	beta_param = 0.6.
	:param domain: Domain
	:return: list of doubles
	"""
	alpha = int(0.3*len(domain.domain_elements))
	beta = int(0.6*len(domain.domain_elements))
	output_list = [0]*len(domain.domain_elements)

	for index, element in enumerate(domain.domain_elements):
		if element < alpha:
			value = 1.0
		if element >= alpha and element < beta:
			value = (beta - element)/(beta - alpha)
		if element >= beta:
			value = 0.0
		output_list[index] = value

	return output_list


def unitary_function(domain, func_name="gamma"):
	"""
	Setting double values to a list based on
	domain.domain_elements list.
	:param func_name : str (name of the function you want to use)
						"step", "gamma", "lambda", "l"
	:param domain: Domain
	:return: list of doubles
	"""
	function_dict = {

		"step" : _step_function(domain),
		"gamma" : _gamma_function(domain),
		"lambda" : _lambda_function(domain),
		"l" : _l_function(domain)
	}
	return function_dict[func_name]


class CalculatedFuzzySet(FuzzySet):
	"""
	Type of FuzzySet that receives unitary function in order
	to calculate its memberships values. 
	This unitary function "defines" the way in which values 
	will be distributed across the domain of the FuzzySet.
	"""

	def __init__(self, domain, my_func="gamma", set_name=""):
		self.domain = domain
		self.unitary_function = unitary_function
		self.memberships = self.unitary_function(self.domain, my_func)
		self.set_name = set_name

if __name__ == "__main__":
	simple_domain = SimpleDomain(1, 40, "Pero")
	my_fuzzy = MutableFuzzySet(simple_domain, "PeroSet")
	my_fuzzy.set_value_at(1, 0.4)
	my_fuzzy.set_value_at(2, 0.9)
	my_fuzzy.print_fuzzy_set()
	lista = unitary_function(simple_domain, "l")
	for index, item in enumerate(lista):
		print("Index: {}, Element domene: {}, Vrijednost: {}".format(index, simple_domain.domain_elements[index], item))

	my_calculated = CalculatedFuzzySet(simple_domain)
