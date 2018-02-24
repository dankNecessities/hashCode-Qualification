import unittest, random, copy
from pizza_soln_beta_1 import get_multiples_set, insert_zeroes, randomized_cuts, optimal_cuts
from pizza_soln_beta_1 import find_ingredients, cut_slice, has_zero, count_remainder, test_generator

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

	def test_find_ingredients(self):
		f_arr = [['a', 'b', 'c'],['a', 'g', 'f'],['a', 'a', 'b']]
		self.assertEqual(find_ingredients(f_arr, 'a', 2), True)
		g_arr = [['a', 'b', 'c'],['q', 'g', 'f'],['f', 'q', 'b']]
		self.assertEqual(find_ingredients(g_arr, 'a', 2), False)
		n_arr = [
				 [1, 2, 3], 
				 [4, 2, 6], 
				 [5, 8, 9]]
		self.assertEqual(find_ingredients(n_arr, 5, 1), True)
		b_arr = [[True, False], [False, False], [True, True]]
		self.assertEqual(find_ingredients(b_arr, True, 2), True)

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
		cursor, pizza, piece = cut_slice(s_arr, (0, 0), (2, 0))
		self.assertEqual(cursor, (0, 0))
		self.assertEqual(pizza, r_arr)
		self.assertEqual(p_arr, piece)

		cursor, pizza, piece = cut_slice(s_arr, (2, 1), (3, 2))
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

	def test_count_remainder(self):
		z_arr = [
				 [0, 0, 8],
				 [3, 4, 6],
				 [1, 0, 8]]
		p_arr = [
				 [4, 6, 8],
				 [3, 4, 6],
				 [1, 9, 8]]
		n_arr = [
				 [0, 0, 0],
				 [0, 0, 0],
				 [0, 0, 0]]		 
		z_left = count_remainder(z_arr)
		p_left = count_remainder(p_arr)
		n_left = count_remainder(n_arr)
		self.assertEqual(z_left, 6)
		self.assertEqual(p_left, 9)
		self.assertEqual(n_left, 0)

	def test_randomized_cuts(self):
		test_pizza = [
			  [T, T, T, T, T],
			  [T, M, M, M, T],
			  [T, T, T, T, T],
			  ]
		n = 6
		cuts_set = get_multiples_set(n)
		cuts_set.append((int(n/2), 1))
		cuts_set.append((1, int(n/2)))
		#cuts_set.append((int(n/3), 2))
		#cuts_set.append((2, int(n/3)))
		'''
		no_of_cuts, cuts_order, un_cuts = randomized_cuts(test_pizza, cuts_set, T, M, 1)
		print("No of cuts: {}".format(no_of_cuts))
		print("Cuts order: {}".format(cuts_order))
		print("Uncut items: {}".format(un_cuts))'''

	def test_optimal_cuts(self):
		test_pizza_2 = [
			  [M, T, M, T, T],
			  [T, M, T, M, T],
			  [T, M, T, T, T],
			  [M, T, T, M, M],
			  [T, T, T, M, M],
			  ]
		#optimal_cuts(test_pizza_2, 1, T, M, 6)

	def test_test_generator(self):
		gen_pizza = test_generator((5, 5), ('T', 'M'))
		for a in gen_pizza:
			y = "               [ "
			for b in a:
				y += str(b)
				y += " "
			y += " ]"
			print(y)
		print("")

if __name__ == '__main__':
	T = 'T'
	M = 'M'
	unittest.main()