class DomainElement(object):

    def get_number_of_components(self):
        """
        :return: int 
        """
        pass

    def get_component_value(self, component):
        """
        :param component: int 
        :return: int
        """
        pass

    def hash_code(self):
        """
        :return: int
        """
        pass

    def equals(self, instance):
        """
        :param instance: Object 
        :return: boolean
        """
        pass

    def to_string(self):
        """
        :return: string 
        """
        pass

class Domain(object):
    def index_of_element(self, domain_element):
        """
        :param domain_element: DomainElement 
        :return: int
        """
        pass

    def element_for_index(self, index):
        """
        :param index: int 
        :return: DomainElement
        """
        pass


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

    def print_simple_domain(self):
        """
        Printing simple domain. 
        """
        print("Elementi domene {}:".format(self.domain_name))
        for element in range(self.first, self.last):
            print("Element domene: {}".format(element))
        print("Kardinalitet domene je: ".format(self.get_cardinality()))

    def get_cardinality(self):
        """
        :return: int 
        """
        return len([element for element in range(self.first, self.last)])

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

    def __init__(self, list_of_domains):
        self.list_of_domains = list_of_domains

    def get_cardinality(self):
        """
        :return: int 
        """
        pass

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
    simple_domain = SimpleDomain(1, 20)
    simple_domain.print_simple_domain()

