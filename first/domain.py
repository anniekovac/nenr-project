import itertools


class Domain(object):

    domain_elements = []

    def index_of_element(self, domain_element):
        """
        :param domain_element: DomainElement 
        :return: int
        """
        return self.domain_elements.index(domain_element)

    def element_for_index(self, index):
        """
        :param index: int 
        :return: DomainElement
        """
        return self.domain_elemens[index]


class SimpleDomain(Domain):

    def __init__(self, first, last, domain_name=""):
        """
        :param first: int 
        :param last: int
        :param domain_name: str or None
        """
        self.first = first
        self.last = last
        self.domain_name = domain_name
        self.domain_elements = [element for element in range(self.first, self.last)]

    def print_simple_domain(self):
        """
        Printing simple domain. 
        """
        print("Elementi domene {}:".format(self.domain_name))
        for element in self.domain_elements:
            print("Element domene: {}".format(element))
        print("Kardinalitet domene je: {}".format(self.get_cardinality()))

    def get_cardinality(self):
        """
        :return: int 
        """
        return len(self.domain_elements)

    def get_number_of_components(self):
        """
        Returns number of SimpleDomains that contribute to this Domain.
        In case of SimpleDomain it is always 1, but that's different
        for CompositeDomain.
        :return: int 
        """
        return 1

    def get_component(self, index=None):
        """
        Returns itself.
        :param index: int
        :return: self
        """
        return self

    def get_first(self):
        """
        :return: int 
        """
        return self.first

    def get_last(self):
        """
        :return: int 
        """
        return self.last

class CompositeDomain(Domain):
    """
    This class represents Domain consisted of multiple
    SimpleDomains. This means that its elements are Cartesian
    product of elements from every SimpleDomain given to it.
    """

    def __init__(self, list_of_domains, domain_name=None):
        self.list_of_domains = list_of_domains
        self.domain_elements = []
        self.domain_name = domain_name

        # creating list of lists
        # in these lists there are elements of every specific
        # SimpleDomain in order to create cartesian product
        list_for_cartesian = [element.domain_elements for element in self.list_of_domains]

        # creating cartesian product and appending these elements
        # to element list
        for element in itertools.product(*list_for_cartesian):
            self.domain_elements.append(element)

    def print_composite_domain(self):
        """
        Printing CompositeDomain. 
        """
        print("Elementi domene {}:".format(self.domain_name))
        for element in self.domain_elements:
            print("Element domene: {}".format(element))
        print("Kardinalitet domene je: {}".format(self.get_cardinality()))

    def get_cardinality(self):
        """
        :return: int 
        """
        return len(self.domain_elements)

    def get_number_of_components(self):
        """
        Returns number of SimpleDomains that contribute
        to Cartesian product.
        :return: int 
        """
        return len(self.list_of_domains)

    def get_component(self, index):
        """
        Returns SimpleDomain found in self.list_of_domains
        on index.
        :param index: int 
        :return: SimpleDomain
        """
        return self.list_of_domains[index]

if __name__ == "__main__":
    simple_domain = SimpleDomain(1, 3, "Pero")
    simple_domain2 = SimpleDomain(0, 4, "Jurica")
    simple_domain.print_simple_domain()
    simple_domain2.print_simple_domain()
    composite_domain = CompositeDomain([simple_domain, simple_domain2], "Barbara")
    composite_domain.print_composite_domain()
