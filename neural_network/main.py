import numpy

if __name__ == '__main__':
	M = 50
	net_architecture = input("Enter wanted net architecture:\n")
	arch_numbers = [int(item) for item in net_architecture.split("x")]
	if arch_numbers[0] != M*2:
		print(arch_numbers[0])
		raise ValueError("Invalid number of input layer neurons is entered! You entered {}, and it should be {}*2={}!"
			.format(arch_numbers[0], M, M*2))
	if arch_numbers[-1] != 5:
		raise ValueError("Invalid number of outputs is entered, it should be 5 and you entered {}!"
						 .format(arch_numbers[-1]))