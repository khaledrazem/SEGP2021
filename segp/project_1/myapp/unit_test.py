# file created by group
from itertools import combinations
import unittest

class TestStringMethods(unittest.TestCase):
    def test_case1_input(self):
        case1_input = '\nComputer Vision\nMachine Learning\nArtificial Intelligence'
        result = case1_input.split("\n")
        result.remove("")
        expected = ['Computer Vision','Machine Learning','Artificial Intelligence']

        self.assertEqual(result, expected)

    def test_filter_input(self):
        keys = ['csrfmiddlewaretoken', 'B_Computer Vision', 'A_Machine Learning', 'B_Machine Learning', 'A_Artificial Intelligence', 'B_Artificial Intelligence', 'amount', 'min_val', 'max_val']
        result = []
        for i in keys:
            if "A_" in i:
                result.append(i.replace("A_",""))
        expected = ['Machine Learning','Artificial Intelligence']
        
        self.assertEqual(result, expected)

    def test_combine_query(self):
        query_1 = "Machine Learning"
        query_2 = "Artificial Intelligence"
        result = query_1 + " + " + query_2
        expected = "Machine Learning + Artificial Intelligence"

        self.assertEqual(result, expected)

    def test_largest5_position(self):
        arr_list = [627, 122, 951, 789, 634, 464, 743, 466, 524, 36, 440, 431, 745, 954, 304]
        result = sorted(range(len(arr_list)), key=lambda sub: arr_list[sub])[-5:]
        expected = [6,12,3,2,13]

        self.assertEqual(result, expected)

    def test_pair_subset(self):
        arr_list = ['a','b','c','d','e']
        result = []
        comb = combinations(arr_list,2)
        for i in comb:
            result.append(i)
        expected = [('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'c'), ('b', 'd'), ('b', 'e'), ('c', 'd'), ('c', 'e'), ('d', 'e')]

        self.assertEqual(result, expected)
        self.assertEqual(len(result), 10)

    def test_break(self):
        count = 0
        arr = []
        while True:
            arr.append('a')
            count += 1
            
            if count >= 100:
                break;
            
        self.assertEqual(len(arr), 100)

    def test_round(self):
        result = round(10/3, 2)
        
        self.assertEqual(result, 3.33)

    def test_data_norm(self):
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        max_val = float(max(arr)) * 1.05
        min_val = float(min(arr)) * 0.95
        result = []
    
        for x in arr:
            point = (float(x) - min_val)/(max_val - min_val)*100
            if point > 100:
                point = 100
            result.append(round(point))

        expected = [0, 10, 19, 29, 38, 48, 57, 67, 76, 86, 95]
        
        self.assertEqual(result, expected)
        self.assertLessEqual(max(result),100)
        
                
if __name__ == '__main__':
    unittest.main()
