if __name__ == "__main__":
	# getting input from keyboard and turning it to integers
	my_input = input("Please enter L D LK DK V S in this order:")
	nums_from_input = [int(char) for char in my_input if char.isdigit()]

	if len(nums_from_input) != 6:
		raise ValueError("Your input is invalid!")

	L, D, LK, DK, V, S = nums_from_input