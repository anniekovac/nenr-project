from domain import Domain


class MutableFuzzySet(Domain):
	def __init__(self, domain):
		self.domain = domain
		self.memberships = [None]*len(self.domain)

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

	def set(self, domain_element, element_value):
		"""
		:param domain_element: DomainElement 
		:param element_value: double
		:return: MutableFuzzySet
		"""
		index = self.domain.index_of_element(domain_element)
		self.memberships[index] = element_value
		return self

