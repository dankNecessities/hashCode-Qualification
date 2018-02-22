import unittest

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
			Slices vary in width and length
				We get the possible slices as multiples of the max size (assuming it is an even no.)
			Randomly cut rectangles from the pizza until remainder < H ingredients
			Store coordinates of each cut
		Remove cuts from grid using coordinates
		The remainder must contain at least one ingredient of each
		Store results of no of slices for each cutting run
		The smallest no of slices, with each of its cut coordinates is returned
	"""
	cut_sizes = get_multiples_set(max_total)

def random_cuts():
	cursor = [0, 0]

def cut_slice(pizza, cursor, rect_size, min_ingredients):
	"""
	A single slice is cut out of the array, and 0s are inserted(deletion)

	"""
	L = min_ingredients

	pizza_buffer = pizza
	cut_size_x, cut_sizes_y = rect_size[0], rect_size[1]
	slice_buffer = []

	#return cursor, pizza_buffer

def insert_zeroes(grid, start, end):
	"""
	Insert zeroes at a specific range in an array
	"""
	array = grid
	start_x, start_y = start[0], start[1]	
	end_x, end_y = end[0], end[1]

	width = end_x - start_x
	height = end_y - start_y 

	for i in range(width):
		for j in range(height):
			array[start_x][start_y] = 0
			start_y += 1
		start_y = 0
		start_x += 1

	return array

def get_multiples_set(n):
	"""
	Gets the dimensions of possible rectangular cuts
	"""
	div_set = []
	multiples_set = []
	q = 0
	for i in range(n):
		q += 1
		div_set.append(q)

	for j in div_set:
		if n % j == 0:
			mult_a = int(j)
			mult_b = int(n / j)
			multiples_set.append((mult_a, mult_b))

	return multiples_set

class pizzaTests(unittest.TestCase):

	def test_get_multiples_set(self):
		n = 6
		q_n = get_multiples_set(n)
		g_set = [(1, 6), (2, 3), (3, 2), (6, 1)]
		self.assertEqual(g_set, q_n)

	def test_insert_zeroes(self):
		arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0, 0, 0]]
		z_arr = [[1, 2, 3], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
		r_arr = insert_zeroes(arr, (1, 0), (3, 3))
		self.assertEqual(r_arr, z_arr)

if __name__ == '__main__':
	unittest.main()