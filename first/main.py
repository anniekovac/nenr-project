import sys
from fuzzy_control import RuddRuleBase, AccRuleBase, defuzzyfication, plot_fuzzy_set
from fuzzy_inputs import *

if __name__ == "__main__":

	rudd = RuddRuleBase()
	acc = AccRuleBase()

	with open("original_input.txt", "w") as f:
		f.write("\nBeginning")

	while True:

		my_input = input()
		if "KRAJ" in my_input:
			break
		nums_from_input = [int(s) for s in my_input.split(" ") if s.isdigit()]
		L, D, LK, DK, V, S = nums_from_input
		input_dict = dict(L=L, D=D, LK=LK, DK=DK, V=V, S=S)

		# for the rudder
		rudd.instant_values = input_dict
		rudd.update_input_values_for_rules()
		fuzzy_k = rudd.calculate_rule_union()
		K = defuzzyfication(fuzzy_k)

		# for the acceleration
		acc.instant_values = input_dict
		acc.update_input_values_for_rules()
		fuzzy_a = acc.calculate_rule_union()
		A = defuzzyfication(fuzzy_a)

		print("{} {}".format(int(A), int(K)))
		sys.stdout.flush();

		my_val_string = str(nums_from_input).replace(",", "")
		with open("original_input.txt", "a") as f:
			f.write("\n{}, A={}, K={}".format(my_val_string, int(A), int(K)))
