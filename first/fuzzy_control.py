from sets import MutableFuzzySet, CalculatedFuzzySet
from domain import SimpleDomain, CompositeDomain


class Rule(CalculatedFuzzySet):

	# ovdje definirati domenu
	# osim domene definirati kojom se funkcijom izracunavaju
	# vrijednosti fuzzy set-a
	# prilagoditi CalculatedFuzzySet klasu
	# da moze primati neku drugu funkciju osim onih prethodno definiranih

	# domena ovisi o tome je li pravilo za akceleraciju
	# ili za kut
	domain = SimpleDomain(first, last)
	pass
