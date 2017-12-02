from fuzzy_control import RuddRuleBase, AccRuleBase, plot_fuzzy_set, defuzzyfication
from fuzzy_inputs import *

if __name__ == "__main__":
	"""
	This program is made for testing one of the
	rules created in the exercise. It will plot
	resultant FuzzySet and show defuzzyficated value of this
	resultant FuzzySet.
	"""
	# initializing both RuleBases
	rudd = RuddRuleBase()
	acc = AccRuleBase()

	# getting input in which rule we will want to test
	my_input = input("Please select one of my rules: ")
	try:
		my_rule = getattr(rudd, my_input)
	except AttributeError:
		try:
			my_rule = getattr(acc, my_input)
		except:
			print("Invalid choice! You can choose between: ")
			raise

	# saving input variables to dictionary
	my_input = input("Enter L, D, LK, DK, V, S:\n")
	nums_from_input = [int(s) for s in my_input.split(" ") if s.isdigit()]
	L, D, LK, DK, V, S = nums_from_input
	input_dict = dict(L=L, D=D, LK=LK, DK=DK, V=V, S=S)

	my_rule.instant_values = input_dict
	result = my_rule.calculate_fuzzy_rule()
	plot_fuzzy_set(result)
	#print(defuzzyfication(result))