import unittest, random, copy

T = 'T'
M = 'M'
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

def max_pizza_slices(pizza, min_ingredients, max_total):
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

def randomized_cuts(pizza, cuts_set, ingredient_a, ingredient_b, min_ingredients):
	"""
	Returns the number of cuts for a given array, and the order in which the cuts were made
	"""
	pizza_buffer = copy.deepcopy(pizza)
	cuts = copy.deepcopy(cuts_set)

	#Cursor starts at the beginning of the pizza array
	init_cursor = [0, 0]
	ordered_cuts = []
	number_of_cuts = 0
	zero_failure = 0
	cursor = copy.deepcopy(init_cursor)

	while find_min_ingredients(pizza_buffer, ingredient_a, min_ingredients) and \
	find_min_ingredients(pizza_buffer, ingredient_b, min_ingredients) and number_of_cuts \
	<= 10:
		#Randomly select a shape for cutting
		print("SHUFFLING CUTS")
		random.shuffle(cuts)
		cut_size = cuts[0]
		print("Cut size: {}".format(cut_size))
		print("Cursor: {}".format(cursor))
		#initialize the shape
		if max(cut_size) < len(pizza_buffer[0]):
			print("STARTING")
			cut_start = copy.deepcopy(cursor)
			cut_end = [cursor[0] + cut_size[0] - 1, cursor[1] + cut_size[1] - 1]
			new_cursor, new_pizza, cut_piece = \
			cut_slice(pizza_buffer, cut_start, cut_end, ingredient_a, ingredient_b, min_ingredients)
			print(new_pizza)
			#For normal cuts which do not exceed range or contain zeroes, modify cursor and pizza
			if not new_pizza == [[]]:
				print("in range")
				contains_zero, zero_location = has_zero(cut_piece)
				if not contains_zero:
					cursor = copy.deepcopy(new_cursor)		
					pizza_buffer = copy.deepcopy(new_pizza)
					print("Removed piece: {}".format(cut_piece))
					print("Remainder: {}".format(pizza_buffer))
					number_of_cuts += 1
					print("Cut: {}".format(number_of_cuts))
					#Add the positions of the cut to the order list
					ordered_cuts.append([cut_start, cut_end])
				else:
					#If a zero exists, we move the cursor a step down, or to the left
					print("Initial contains zero: {}".format(contains_zero))
					if contains_zero:
						if zero_failure < 1:
							cursor = [new_cursor[0] + 1, new_cursor[1]]
							zero_failure += 1
						elif zero_failure >= 1:
							cursor = [new_cursor[0], new_cursor[1] + 1]
							zero_failure = 0	

		#####REACHED HERE'''

		#When the cursor moves completely out of the pizza range, the run stops
		if cursor[0] > len(pizza_buffer) and cursor[1] > len(pizza_buffer[0]):
			break

	return number_of_cuts, ordered_cuts

def cut_slice(pizza, cut_start, cut_end, ingredient_a, ingredient_b, min_ingredients):
	"""
	A single slice is cut out of the array, and if slice is valid 0s are inserted(deletion)
	A valid cut contains the minimum number of ingredients
	Cannot cut backwards, cut_start must be to the left of cut_end
	Returns the cursor point and an empty slice if cut is out of range
	NOTE: It also modifies the array in place!
	"""
	pizza_buffer = copy.deepcopy(pizza)
	cut_length = cut_end[0] - cut_start[0] + 1
	cut_height = cut_end[1] - cut_start[1] + 1
	slice_buffer = []
	point_x, point_y = cut_start[0], cut_start[1]

	#Items are added into the slice buffer from the selected range
	try:
	#If a cut is invalid, return None	
		for i in range(cut_length):
			slice_buffer.append([])
			for j in range(cut_height):
				qq = pizza_buffer[point_x][point_y]
				slice_buffer[i].append(qq)
				point_y += 1
			point_y = cut_start[1]
			point_x += 1
		new_cursor = (cut_start[0], cut_end[1])
	except IndexError:
	#If the cut exceeds the array size, return the cursor point and None	
		cursor = cut_start
		return cursor, [[]], [[]]

	#If the minimum number of ingredients exist, then slice is valid, we insert zeroes
	if find_min_ingredients(slice_buffer, ingredient_a, min_ingredients) and \
	find_min_ingredients(slice_buffer, ingredient_b, min_ingredients):
		pizza_buffer = insert_zeroes(pizza_buffer, cut_start, cut_end)
		return new_cursor, pizza_buffer, slice_buffer
	else:
		return None, [[]], [[]]

def has_zero(array):
	"""
	Returns True if a 0 is found within the array
	Returns the location of the last zero found
	"""
	ans = False
	z_x, z_y = 0, 0
	zero_coord = None
	for i in array:
		for j in i:
			if j == 0:
				zero_coord = (z_x, z_y)
				ans = True
			z_y += 1
		z_y = 0
		z_x += 1
	return ans, zero_coord

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
	array = copy.deepcopy(grid)
	start_x, start_y = start[0], start[1]	
	end_x, end_y = end[0], end[1]
	width = end_x - start_x + 1
	height = end_y - start_y + 1

	for i in range(width):
		for j in range(height):
			array[start_x][start_y] = 0
			start_y += 1
		start_y = start[1]
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
				 [10, 10, 10]]
		z_arr = [
				 [1, 2, 3], 
				 [4, 0, 0], 
				 [7, 0, 0], 
				 [10, 0, 0]]
		r_arr = insert_zeroes(arr, (1, 1), (3, 2))
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
		b_arr = [[True, False], [False, False], [True, True]]
		self.assertEqual(find_min_ingredients(b_arr, True, 2), True)

	def test_cut_slice(self):
		s_arr = [
				 [1, 2, 3], 
				 [4, 2, 6], 
				 [5, 8, 9]]
		r_arr = [
				 [0, 2, 3],
				 [0, 2, 6],
				 [0, 8, 9]]
		p_arr = [
				 [1], [4], [5]]
		cursor, pizza, piece = cut_slice(s_arr, (0, 0), (2, 0), 1, 5, 1)
		self.assertEqual(cursor, (0, 0))
		self.assertEqual(pizza, r_arr)
		self.assertEqual(p_arr, piece)

		cursor, pizza, piece = cut_slice(s_arr, (2, 1), (3, 2), 6, 9, 1)
		self.assertEqual(cursor, (2, 1))
		self.assertEqual(pizza, [[]])
		self.assertEqual(piece, [[]])

	def test_has_zero(self):
		z_arr = [
				 [0, 0, 8],
				 [3, 4, 6],
				 [1, 0, 8]]
		p_arr = [
				 [4, 6, 8],
				 [3, 4, 6],
				 [1, 9, 8]]
		answer, location = has_zero(z_arr)
		answer2, location2 = has_zero(p_arr)
		self.assertEqual(answer, True)
		self.assertEqual(location, (2, 1))
		self.assertEqual(answer2, False)
		self.assertEqual(location2, None)

	def test_randomized_cuts(self):
		test_pizza = [
			  [T, T, T, T, T],
			  [T, M, M, M, T],
			  [T, T, T, T, T],
			  ]
		cuts_set = get_multiples_set(6)
		no_of_cuts, cuts_order = randomized_cuts(test_pizza, cuts_set, T, M, 1)

if __name__ == '__main__':

	unittest.main()
