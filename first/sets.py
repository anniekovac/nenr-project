from domain import Domain


class IFuzzySet(object):
	def get_domain(self):
		"""
		:return: IDomain 
		"""
		pass

	def get_value_at(self, domain_element):
		"""
		"Asking" domain for index of domain_element.

		:param domain_element: DomainElement 
		:return: double
		"""
		pass


class MutableFuzzySet(IFuzzySet, Domain):
	def __init__(self, domain):
		self.memberships = []
		self.domain = domain

	def set(self, domain_element, double_value):
		"""
		:param domain_element: DomainElement 
		:param double_value: double
		:return: MutableFuzzySet
		"""
		pass

