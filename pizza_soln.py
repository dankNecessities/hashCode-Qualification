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

def cut_slice(pizza, cut_start, cut_end, ingredient_a, ingredient_b, min_ingredients):
	"""
	A single slice is cut out of the array, and 0s are inserted(deletion)
	"""
	pizza_buffer = pizza
	cut_length = cut_end[0] - cut_start[0] + 1
	cut_height = cut_end[1] - cut_start[1] + 1
	slice_buffer = []
	point_x, point_y = cut_start[0], cut_start[1]

	#Items are added into the slice buffer from the selected range
	for i in range(cut_length):
		slice_buffer.append([])
		for j in range(cut_height):
			qq = pizza_buffer[point_x][point_y]
			slice_buffer[i].append(qq)
			point_y += 1
		point_y = cut_start[1]
		point_x += 1
	new_cursor = (cut_start[0], cut_end[1])

	#If the minimum number of ingredients exist, then slice is valid, we insert zeroes
	if find_min_ingredients(slice_buffer, ingredient_a, min_ingredients) and \
	find_min_ingredients(slice_buffer, ingredient_b, min_ingredients):
		pizza_buffer = insert_zeroes(pizza_buffer, cut_start, cut_end)
		return new_cursor, pizza_buffer, slice_buffer
	else:
		return None

def find_min_ingredients(grid, item, min_limit):
	"""
	Determines whether the minimum number of items in a 2D array are present
	"""
	find_count = 0
	for i in grid:
		for j in i:
			if j == item:
				find_count += 1
	if find_count >= min_limit:
		return True
	else:
		return False

def insert_zeroes(grid, start, end):
	"""
	Insert zeroes at a specific range in an array
	"""
	array = grid
	start_x, start_y = start[0], start[1]	
	end_x, end_y = end[0], end[1]
	width = end_x - start_x + 1
	height = end_y - start_y + 1

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
		arr = [
				 [1, 2, 3], 
				 [4, 5, 6], 
				 [7, 8, 9], 
				 [0, 0, 0]]
		z_arr = [
				 [1, 2, 3], 
				 [4, 5, 6], 
				 [0, 0, 9], 
				 [0, 0, 0]]
		r_arr = insert_zeroes(arr, (2, 0), (3, 1))
		self.assertEqual(r_arr, z_arr)

	def test_find_min_ingredients(self):
		f_arr = [['a', 'b', 'c'],['a', 'g', 'f'],['a', 'a', 'b']]
		self.assertEqual(find_min_ingredients(f_arr, 'a', 2), True)
		g_arr = [['a', 'b', 'c'],['q', 'g', 'f'],['f', 'q', 'b']]
		self.assertEqual(find_min_ingredients(g_arr, 'a', 2), False)
		n_arr = [
				 [1, 2, 3], 
				 [4, 2, 6], 
				 [5, 8, 9]]
		self.assertEqual(find_min_ingredients(n_arr, 5, 1), True)

	def test_cut_slice(self):
		s_arr = [
				 [1, 2, 3], 
				 [4, 2, 6], 
				 [5, 8, 9]]
		r_arr = [
				 [1, 2, 3],
				 [0, 0, 6],
				 [0, 0, 9]]
		p_arr = [
				 [4, 2],
				 [5, 8]]
		cursor, pizza, piece = cut_slice(s_arr, (1, 0), (2, 1), 2, 5, 1)
		self.assertEqual(cursor, (1, 1))
		self.assertEqual(pizza, r_arr)
		self.assertEqual(p_arr, piece)

if __name__ == '__main__':
	unittest.main()