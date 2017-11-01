if __name__ == "__main__":

	while True:

		# getting input from keyboard and turning it to integers
		my_input = input("Please enter L D LK DK V S in this order:")
		if "KRAJ" in my_input:
			break
		nums_from_input = [int(char) for char in my_input if char.isdigit()]
		L, D, LK, DK, V, S = nums_from_input

		# L - udaljenost broda od obale prema lijevo
		# D - udaljenost broda od obale prema desno
		# LK - udaljenost broda od obale naprijed lijevo pod 45
		# DK - udaljenost broda od obale naprijed desno pod 45
		# V - iznos brzine broda
		# S - podatak o tome krece li se brod u pravom smjeru (1 ako da, 0 ako ne)


