from fuzzy_control import RuddRuleBase, AccRuleBase, plot_fuzzy_set, defuzzyfication
from fuzzy_inputs import *

if __name__ == "__main__":

	#plot_fuzzy_set(my_acc_set)
	rudd = RuddRuleBase()
	acc = AccRuleBase()
	my_input = input("Please select one of my rules: ")
	try:
		my_rule = getattr(rudd, my_input)
	except AttributeError:
		try:
			my_rule = getattr(acc, my_input)
		except:
			print("Invalid choice! You can choose between: ")
			raise

	my_input = input("Enter L, D, LK, DK, V, S:\n")
	nums_from_input = [int(s) for s in my_input.split(" ") if s.isdigit()]
	L, D, LK, DK, V, S = nums_from_input
	input_dict = dict(L=L, D=D, LK=LK, DK=DK, V=V, S=S)

	my_rule.instant_values = input_dict
	#import pdb; pdb.set_trace()
	#plot_fuzzy_set(my_rule)
	result = my_rule.calculate_fuzzy_rule()

	plot_fuzzy_set(result)
	print(defuzzyfication(result))