from fuzzy_control import fuzzyfication, plot_fuzzy_set, Rule
from domain import SimpleDomain
from sets import CalculatedFuzzySet

def fuzzy_magic(nums_from_input):
	"""
	This is where all the magic happens.
	:param nums_from_input: [int] (list of ints from standard input)
	:return: None
	"""
	L, D, LK, DK, V, S = nums_from_input
	distance_domain = (0, 1301)
	fuzzy_setL = fuzzyfication(L, *distance_domain)
	fuzzy_setD = fuzzyfication(D, *distance_domain)
	fuzzy_setLK = fuzzyfication(LK, *distance_domain)
	fuzzy_setDK = fuzzyfication(DK, *distance_domain)

	fuzzy_setS = fuzzyfication(S, 0, 2)
	fuzzy_setV = fuzzyfication(V, 20, 51)
	#plot_fuzzy_set(fuzzy_setL)

	angle_domain = SimpleDomain(-90, 91)
	distance_domain = SimpleDomain(0, 1301)
	dangerously_close = CalculatedFuzzySet(distance_domain, "l")
	dangerously_close.set_calculated_memberships("l", alpha=0.1, beta=0.7)
	close = CalculatedFuzzySet(distance_domain, "l")
	close.set_calculated_memberships("l", alpha=0.4, beta=0.7)
	#plot_fuzzy_set(close)
	my_rule = Rule(angle_domain, L=fuzzy_setL, LK=fuzzy_setLK)


if __name__ == "__main__":

	while True:

		# getting input from keyboard and turning it to integers
		my_input = input("Please enter L D LK DK V S in this order:")
		if "KRAJ" in my_input:
			break
		nums_from_input = [int(s) for s in my_input.split(" ") if s.isdigit()]
		fuzzy_magic(nums_from_input)




		# L - udaljenost broda od obale prema lijevo
		# D - udaljenost broda od obale prema desno
		# LK - udaljenost broda od obale naprijed lijevo pod 45
		# DK - udaljenost broda od obale naprijed desno pod 45
		# V - iznos brzine broda
		# S - podatak o tome krece li se brod u pravom smjeru (1 ako da, 0 ako ne)


