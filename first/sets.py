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


class MutableFuzzySet(IFuzzySet):
	def __init__(self, idomain):
		self.memberships = []

	def set(self, domain_element, double_value):
		"""
		:param domain_element: DomainElement 
		:param double_value: double
		:return: MutableFuzzySet
		"""
		pass

