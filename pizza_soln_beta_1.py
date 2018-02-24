"""
/* 
 * A semi-optimized version, for uploading.
 * Commentary is heavily reduced.
 * Cursor output is limited
 * Written in Python 3.6
 * Tests run from external file
 */
"""
import unittest, random, copy, sys

def optimal_cuts(pizza, min_ingredients, ingredient_a, ingredient_b, max_total):
	"""
	Stores a list of number of pizza cuts, coordinates of these cuts and the remainder after cutting
	"""
	unsliced_pizza = copy.deepcopy(pizza)
	#Nice output formatting, informative
	print("Pizza whose slicing is to optimized:")
	print("")
	for a in pizza:
		y = "               [ "
		for b in a:
			y += str(b)
			y += " "
		y += "]"
		print(y)
	print("")
	print("Please Wait.............")
	#run_length specifies the number of times a randomized_cut sequence is run, limits the precision
	run_length = 50
	cut_shapes = get_multiples_set(max_total)
	unsorted_results = []
	#Increase precision of cuts by including non-optimal slices
	n = max_total
	cut_shapes.append((int(n/2), 1))
	cut_shapes.append((1, int(n/2)))
	for i in range(run_length):
		level = i/run_length * 100
		sys.stdout.write(" Status: %d%% \r" % level)
		sys.stdout.flush()
		no_of_cuts, ordered_cuts, remainder = \
		randomized_cuts(unsliced_pizza, cut_shapes, ingredient_a, ingredient_b, min_ingredients)
		unsorted_results.append([no_of_cuts, ordered_cuts, remainder])	
	min_remainder = 10000000000000
	min_results = []
	#Find the lowest remainder for all the results
	for i in unsorted_results:
		tr = i[2]
		if tr < min_remainder:
			min_remainder = tr
	#Put the results with the lowest remainder into a new set
	for i in unsorted_results:
		tr = i[2]
		if tr == min_remainder:
			min_results.append(i)
	#Find the results with the fewest cuts
	min_cut = 10000000000000
	for i in min_results:
		tc = i[0]
		if tc < min_cut:
			min_cut = tc
			optimum_cuts = i
	print(" ")
	print("Optimal Cuts: {}".format(optimum_cuts[0]))
	print("Optimal Cuts Order: {}".format(optimum_cuts[1]))

def randomized_cuts(pizza, cuts_set, ingredient_a, ingredient_b, min_ingredients):
	"""
	Returns the number of cuts for a given array, the order in which the cuts were made, and the 
	remainder after performing the cuts
	"""
	pizza_buffer = copy.deepcopy(pizza)
	cuts = copy.deepcopy(cuts_set)
	#Cursor starts at the beginning of the pizza array
	init_cursor = [0, 0]
	ordered_cuts = []
	number_of_cuts = 0
	cursor = copy.deepcopy(init_cursor)

	while True:
		#Randomly select a shape for cutting
		random.shuffle(cuts)
		cut_size = cuts[0]
		#initialize the shape
		cut_start = copy.deepcopy(cursor)
		cut_end = [cursor[0] + cut_size[0] - 1, cursor[1] + cut_size[1] - 1]
		#Cut out a slice
		new_cursor, new_pizza, cut_piece = cut_slice(pizza_buffer, cut_start, cut_end)
		#For normal cuts which do not exceed range or contain zeroes, modify cursor and pizza
		if not new_pizza == [[]]:
			contains_zero, zero_location = has_zero(cut_piece)
			if not contains_zero:
				if find_ingredients(cut_piece, ingredient_a, min_ingredients) and \
				find_ingredients(cut_piece, ingredient_b, min_ingredients):
					#If the remainder does not have the required ingredients, then continue
					if not find_ingredients(pizza_buffer, ingredient_a, min_ingredients) or \
					not find_ingredients(pizza_buffer, ingredient_b, min_ingredients):
						break
					#Otherwise, we save the cut
					else:
						cursor = [new_cursor[0], new_cursor[1] + 1]		
						pizza_buffer = copy.deepcopy(new_pizza)
						number_of_cuts += 1
						#Add the positions of the cut to the order list
						ordered_cuts.append([cut_start, cut_end])
			else:
				#If a zero exists, we move the cursor to the right
				cursor = [cut_start[0], cut_start[1] + 1]	
		#If the cut is out of range we change the shape until we find one that fits
		else:
			for i in cuts:
				cut_end = [cursor[0] + i[0] - 1, cursor[1] + i[1] - 1]
				temp_new_cursor, temp_new_pizza, temp_cut_piece = \
				cut_slice(pizza_buffer, cut_start, cut_end)
				#if a cut is found in range, we check for zeroes
				if not temp_new_pizza == [[]]:
					contains_zero, zero_location = has_zero(temp_cut_piece)
					#if a zero is found, we we move the cursor to the start of a new line
					if contains_zero:
						cursor = [cut_start[0], cut_start[1] + 1]
					#If not, we count it as a normal cut
					else:
						if find_ingredients(temp_cut_piece, ingredient_a, min_ingredients) and \
						find_ingredients(temp_cut_piece, ingredient_b, min_ingredients):
							#If the remainder does not have the required ingredients, then stop
							if not find_ingredients(pizza_buffer, ingredient_a, min_ingredients) or \
							not find_ingredients(pizza_buffer, ingredient_b, min_ingredients):
								break
							else:
								cursor = [temp_new_cursor[0], temp_new_cursor[1] + 1]		
								pizza_buffer = copy.deepcopy(temp_new_pizza)
								number_of_cuts += 1
								#Add the positions of the cut to the order list
								ordered_cuts.append([cut_start, cut_end])
						#If the slice does not contain the minimum ingredients, then we shift the cursor
						else:
							cursor = [cut_start[0], cut_start[1] + 1]
					break

			#if no cut was found within range, we move the cursor to the start of a new line
			if temp_new_pizza == [[]]:
				cursor = [new_cursor[0] + 1, 0]

		#If the remainder does not have the required ingredients, then stop
		if not find_ingredients(pizza_buffer, ingredient_a, min_ingredients) or \
		not find_ingredients(pizza_buffer, ingredient_b, min_ingredients):
			break

		#When the cursor moves completely out of the pizza range, the run stops
		if cursor[0] > len(pizza_buffer):
			#cursor = [cursor[0] - 1, cursor[1]]
			break
		
	cuts_remainder = count_remainder(pizza_buffer)
	return number_of_cuts, ordered_cuts, cuts_remainder

def cut_slice(pizza, cut_start, cut_end):
	"""
	A single slice is cut out of the array, and 0s are inserted(deletion)
	Cannot cut backwards, cut_start must be to the left of cut_end
	Returns the cursor point and an empty slice if cut is out of range
	"""
	pizza_buffer = copy.deepcopy(pizza)
	cut_length = cut_end[0] - cut_start[0] + 1
	cut_height = cut_end[1] - cut_start[1] + 1
	slice_buffer = []
	point_x, point_y = cut_start[0], cut_start[1]

	#Items are added into the slice buffer from the selected range
	try:
		for i in range(cut_length):
			slice_buffer.append([])
			for j in range(cut_height):
				qq = pizza_buffer[point_x][point_y]
				slice_buffer[i].append(qq)
				point_y += 1
			point_y = cut_start[1]
			point_x += 1
		new_cursor = (cut_start[0], cut_end[1])
		pizza_buffer = insert_zeroes(pizza_buffer, cut_start, cut_end)
		return copy.deepcopy(new_cursor), copy.deepcopy(pizza_buffer), copy.deepcopy(slice_buffer)
	except IndexError:
	#If the cut exceeds the array size, return the initial cursor point and None	
		cursor = cut_start
		return copy.deepcopy(cursor), [[]], [[]]

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

def find_ingredients(grid, item, min_limit):
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

def count_remainder(grid):
	"""
	Finds how many non-zero items are left in a grid
	"""
	items_left = 0
	for i in grid:
		for j in i:
			if j != 0:
				items_left += 1
	return items_left

def test_generator(size, characters):

	row_generator = []
	char_1 = characters[0]
	char_2 = characters[1]

	for i in range(size[0]):
		row_generator.append([])
		for j in range(size[1]):
			if random.randint(0, 1) == 0:
				row_generator[i].append(char_1)
			else:
				row_generator[i].append(char_2)

	return row_generator

if __name__ == '__main__':
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
	test_pizza_3 = [
				  [M, T, M, T, T, M],
				  [T, M, T, M, T, T],
				  [T, M, T, T, T, T],
				  [M, T, M, M, M, T],
				  [T, T, T, M, T, M],
				  [T, M, T, M, M, M],
				  [T, T, T, M, M, T],
				  ]
	test_pizza_4 = [
				  [M, T, M, T, T, M, T, T, M, T],
				  [M, T, M, T, T, M, M, M, T, T],
				  [T, M, T, M, T, T, T, M, M, T],
				  [T, M, T, M, T, T, M, T, M, T],
				  [T, M, T, T, T, T, M, M, T, M],
				  [M, T, M, M, M, T, T, T, M, T],
				  [T, T, T, M, T, M, M, M, T, M],
				  [T, M, T, M, M, M, T, M, M, T],
				  [T, M, T, M, M, M, T, M, M, M],
				  [T, T, T, M, M, T, T, M, M, M],
				  ]
	#gen_pizza = test_generator((20, 20), ('T', 'M'))
	optimal_cuts(test_pizza_2, 1, T, M, 6)