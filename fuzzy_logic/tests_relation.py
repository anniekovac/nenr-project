from domain import CompositeDomain
from domain import SimpleDomain
from sets import MutableFuzzySet
from relation import composition_of_binary_relations
from relation import is_fuzzy_equivalence
from relation import is_U_times_relation, is_max_min_transitive
from relation import is_reflexive, is_symmetric


def test_relation_characteristics():
	"""
	Test made for testing characteristics of fuzzy relations.
	This test will test most of the functions from relation.py
	that return boolean.
	:return: None
	"""
	u = SimpleDomain(1, 6)
	u2 = CompositeDomain([u, u])

	r1 = MutableFuzzySet(u2)
	r1.set_value_at((1, 1), 1)
	r1.set_value_at((2, 2), 1)
	r1.set_value_at((3, 3), 1)
	r1.set_value_at((4, 4), 1)
	r1.set_value_at((5, 5), 1)
	r1.set_value_at((3, 1), 0.5)
	r1.set_value_at((1, 3), 0.5)

	r2 = MutableFuzzySet(u2)
	r2.set_value_at((1, 1), 1)
	r2.set_value_at((2, 2), 1)
	r2.set_value_at((3, 3), 1)
	r2.set_value_at((4, 4), 1)
	r2.set_value_at((5, 5), 1)
	r2.set_value_at((3, 1), 0.5)
	r2.set_value_at((1, 3), 0.1)

	r3 = MutableFuzzySet(u2)
	r3.set_value_at((1, 1), 1)
	r3.set_value_at((2, 2), 1)
	r3.set_value_at((3, 3), 0.3)
	r3.set_value_at((4, 4), 1)
	r3.set_value_at((5, 5), 1)
	r3.set_value_at((1, 2), 0.6)
	r3.set_value_at((2, 1), 0.6)
	r3.set_value_at((2, 3), 0.7)
	r3.set_value_at((3, 2), 0.7)
	r3.set_value_at((3, 1), 0.5)
	r3.set_value_at((1, 3), 0.5)

	r4 = MutableFuzzySet(u2)
	r4.set_value_at((1, 1), 1)
	r4.set_value_at((2, 2), 1)
	r4.set_value_at((3, 3), 1)
	r4.set_value_at((4, 4), 1)
	r4.set_value_at((5, 5), 1)
	r4.set_value_at((1, 2), 0.4)
	r4.set_value_at((2, 1), 0.4)
	r4.set_value_at((2, 3), 0.5)
	r4.set_value_at((3, 2), 0.5)
	r4.set_value_at((1, 3), 0.4)
	r4.set_value_at((3, 1), 0.4)

	print("r1 je definiran nad UxU: {}".format(is_U_times_relation(r1)))
	print("r1 je simetricna: {}".format(is_symmetric(r1)))
	print("r2 je simetricna: {}".format(is_symmetric(r2)))
	print("r1 je refleksivna: {}".format(is_reflexive(r1)))
	print("r3 je refleksivna: {}".format(is_reflexive(r3)))
	print("r3 je max-min tranzitivna: {}".format(is_max_min_transitive(r3)))
	print("r4 je max-min tranzitivna: {}".format(is_max_min_transitive(r4)))


def test_composition():
	"""
	Test made for testing composition of 
	binary relations. Test is based 
	on example from slides (example from ha-03b slide 29/66).
	:return: None
	"""
	prvi = SimpleDomain(0, 4, "Pero")
	prvi2 = SimpleDomain(0, 5, "Pero")
	drugi = SimpleDomain(0, 5, "Branko")
	drugi2 = SimpleDomain(0, 3, "Branko")
	compos1 = CompositeDomain([prvi, prvi2], "Composite1")
	compos2 = CompositeDomain([drugi, drugi2], "Composite2")

	# example from ha-03b slide 29/66
	my_fuzz1 = MutableFuzzySet(compos1)
	my_fuzz2 = MutableFuzzySet(compos2)

	my_fuzz1.set_value_at((0, 0), 0.1)
	my_fuzz1.set_value_at((0, 1), 0.7)
	my_fuzz1.set_value_at((0, 2), 0.5)
	my_fuzz1.set_value_at((0, 3), 0.1)
	my_fuzz1.set_value_at((1, 0), 0.5)
	my_fuzz1.set_value_at((1, 1), 1.0)
	my_fuzz1.set_value_at((1, 2), 0.9)
	my_fuzz1.set_value_at((1, 3), 0.4)
	my_fuzz1.set_value_at((1, 3), 0.4)
	my_fuzz1.set_value_at((2, 0), 0.2)
	my_fuzz1.set_value_at((2, 1), 0.1)
	my_fuzz1.set_value_at((2, 2), 0.6)
	my_fuzz1.set_value_at((2, 3), 0.9)

	my_fuzz2.set_value_at((0, 0), 1.0)
	my_fuzz2.set_value_at((0, 1), 0.2)
	my_fuzz2.set_value_at((1, 0), 0.7)
	my_fuzz2.set_value_at((1, 1), 0.5)
	my_fuzz2.set_value_at((2, 0), 0.3)
	my_fuzz2.set_value_at((2, 1), 0.9)
	my_fuzz2.set_value_at((3, 0), 0.0)
	my_fuzz2.set_value_at((3, 1), 0.4)

	composition_of_binary_relations(my_fuzz1, my_fuzz2)

def test_composition2():
	u1 = SimpleDomain(1, 5)
	u2 = SimpleDomain(1, 4)
	u3 = SimpleDomain(1, 5)

	u1u2 = CompositeDomain([u1, u2])
	r1 = MutableFuzzySet(u1u2)
	r1.set_value_at((1, 1), 0.3)
	r1.set_value_at((1, 2), 1)
	r1.set_value_at((3, 3), 0.5)
	r1.set_value_at((4, 3), 0.5)

	u2u3 = CompositeDomain([u2, u3])
	r2 = MutableFuzzySet(u2u3)
	r2.set_value_at((1, 1), 1)
	r2.set_value_at((2, 1), 0.5)
	r2.set_value_at((2, 2), 0.7)
	r2.set_value_at((3, 3), 1)
	r2.set_value_at((3, 4), 0.4)

	my_composition = composition_of_binary_relations(r1, r2)
	for domain_element in my_composition.domain.domain_elements:
		print("mu({}) = {}".format(domain_element, my_composition.get_value_at(domain_element)))


def test_equivalence():
	u = SimpleDomain(1, 5)
	uu = CompositeDomain([u, u])
	r = MutableFuzzySet(uu)
	r.set_value_at((1, 1), 1)
	r.set_value_at((2, 2), 1)
	r.set_value_at((3, 3), 1)
	r.set_value_at((4, 4), 1)
	r.set_value_at((1, 2), 0.3)
	r.set_value_at((2, 1), 0.3)
	r.set_value_at((2, 3), 0.5)
	r.set_value_at((3, 2), 0.5)
	r.set_value_at((3, 4), 0.2)
	r.set_value_at((4, 3), 0.2)

	r2 = r

	print("Pocetna relacija je neizrazita relacija ekvivalencije? {}".format(is_fuzzy_equivalence(r)))

	for i in range(1, 3):
		r2 = composition_of_binary_relations(r2, r)
		print("Broj odradjenih kompozicija: {}".format(i))
		print("Relacija je: ")

		for domain_element in r2.domain.domain_elements:
			print("mu({}) = {}".format(domain_element, r2.get_value_at(domain_element)))

		print("Ova relacija je neizrazita relacija ekvivalencije? {}".format(is_fuzzy_equivalence(r2)))
