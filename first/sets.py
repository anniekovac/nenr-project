from domain import SimpleDomain


class FuzzySet(object):
	"""
	Parent class for MutableFuzzySet and
	CalculatedFuzzySet. It contains some basic 
	functionality for both of these classes.
	These internal variables should be defined in 
	children classes:
	- set_name, domain, memberships
	User is obligated to defined these
	variables if they want to use some 
	methods from FuzzySet class.
	"""
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
	"""
	MutableFuzzySet is a type of FuzzySet which
	allows you to set memberships values for each
	domain element.
	"""
	def __init__(self, domain, set_name=""):
		self.domain = domain
		self.memberships = [0]*len(self.domain.domain_elements)
		self.set_name = set_name

	def set_value_at(self, domain_element, element_value):
		"""
		This method allows you to set element_value to
		domain_element by writing that value on corresponding
		index in memberships variable.
		:param domain_element: DomainElement 
		:param element_value: double
		:return: MutableFuzzySet
		"""
		if not(element_value>=0 and element_value <=1):
			raise ValueError("Trying to set incorrect value! Try any value between 0 and 1.")
		index = self.domain.index_of_element(domain_element)
		self.memberships[index] = element_value
		return self


def _step_function(domain):
	"""
	This is a function that calculates
	values for domain elements given with
	argument domain. Function is step. 
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
	domain_len = len(domain.domain_elements)
	alpha = int(0.3*domain_len)
	beta = int(0.6*domain_len)
	output_list = [0]*domain_len

	for index, element in enumerate(domain.domain_elements):
		if index < alpha:
			value = 0.0
		if index >= alpha and index < beta:
			value = (index - alpha)/(beta - alpha)
		if index >= beta:
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
	domain_len = len(domain.domain_elements)
	alpha = int(0.25*domain_len)
	beta = int(0.5*domain_len)
	gamma = int(0.75*domain_len)
	output_list = [0]*domain_len

	for index, element in enumerate(domain.domain_elements):
		if index < alpha:
			value = 0.0
		if index >= alpha and index < beta:
			value = (index - alpha)/(beta - alpha)
		if index >= beta and index < gamma:
			value = (gamma - index) / (gamma - beta)
		if index >= gamma:
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
	domain_len = len(domain.domain_elements)
	alpha = int(0.3*domain_len)
	beta = int(0.6*domain_len)
	output_list = [0]*domain_len

	for index, element in enumerate(domain.domain_elements):
		if index < alpha:
			value = 1.0
		if index >= alpha and index < beta:
			value = (beta - index)/(beta - alpha)
		if index >= beta:
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
	try:
		my_fuzzy.set_value_at(2, 1.9)
	except ValueError:
		print("Correct error raised.")
	#my_fuzzy.print_fuzzy_set()
	lista = unitary_function(simple_domain, "l")
	# for index, item in enumerate(lista):
	# 	print("Index: {}, Element domene: {}, Vrijednost: {}".format(index, simple_domain.domain_elements[index], item))

	my_calculated = CalculatedFuzzySet(simple_domain)
