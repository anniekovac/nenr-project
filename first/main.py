from fuzzy_control import RuddRuleBase, AccRuleBase


if __name__ == "__main__":

	rudd = RuddRuleBase()
	acc = AccRuleBase()

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

		acc.instant_values = input_dict

