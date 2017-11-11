from fuzzy_control import RuddRuleBase, AccRuleBase, plot_fuzzy_set, defuzzyfication
from fuzzy_inputs import *

if __name__ == "__main__":


	my_input = input("Please select one of my bases (type 'acc' or 'rudd'): ")

	if my_input == "rudd":
		my_base = RuddRuleBase()
	elif my_input == "acc":
		my_base = AccRuleBase()

	my_input = input("Enter L, D, LK, DK, V, S:\n")
	nums_from_input = [int(s) for s in my_input.split(" ") if s.isdigit()]
	L, D, LK, DK, V, S = nums_from_input
	input_dict = dict(L=L, D=D, LK=LK, DK=DK, V=V, S=S)

	my_base.instant_values = input_dict
	my_base.update_input_values_for_rules()
	fuzzy_result = my_base.calculate_rule_union()
	plot_fuzzy_set(fuzzy_result)

