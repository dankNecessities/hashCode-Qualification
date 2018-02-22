T = True
M = False
test_pizza = [
			  [T, T, T, T, T],
			  [T, M, M, M, T],
			  [T, T, T, T, T],
			  ]

test_pizza_2 = [
			  [M, T, M, T, T],
			  [T, M, T, M, T],
			  [T, M, T, T, T],
			  [M, T, T, M, M],
			  [T, T, T, M, M],
			  ]

"""
RULES:
1) Max no of total ingredients per slice = H
2) Minimum no of each ingredient per slice = L
"""

def max_pizza(pizza, min_ingredients, max_total):
	"""
	#Slicing algorithm
	Intuitively;
		Cut a slice with max ingredients, must contain at least L of either ingredient
			Max_slices are either 2x3 or 3x2
				We get the 2x3 or 3x2 as multiples of the max size (assuming it is an even no.)
			Randomly cut 2x3, 3x2 rectangles from the pizza until remainder < H ingredients
			Store coordinates of each cut
		Remove cuts from grid using coordinates
		The remainder must contain at least one ingredient of each
		Store results of no of slices for each cutting run
		The smallest no of slices, with each of its cut coordinates is returned
	"""
	pass

def cut_slice(pizza, min_ingredients, max_total);
	L = min_ingredients
	H = max_total

	pizza_buffer = pizza

def get_multiples_set(n):
	div_set = []
	multiples_set = []
	q = 0
	for i in range(n):
		q + 1
		div_set.append(q)

	for j in div_set:
