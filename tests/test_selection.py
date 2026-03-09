"""
Unit tests for selection algorithms.
"""

import unittest
import random
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.selection import median_of_medians, randomized_select
from src.selection.randomized_select import find_median, find_kth_largest


class TestMedianOfMedians(unittest.TestCase):
    """Tests for Median of Medians algorithm."""
    
    def test_basic_selection(self):
        """Test basic k-th smallest selection."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        
        # 1st smallest (minimum)
        self.assertEqual(median_of_medians(arr, 1), 1)
        
        # Last (maximum)
        self.assertEqual(median_of_medians(arr, len(arr)), 9)
        
        # Median
        sorted_arr = sorted(arr)
        k = (len(arr) + 1) // 2
        self.assertEqual(median_of_medians(arr, k), sorted_arr[k-1])
    
    def test_sorted_array(self):
        """Test on sorted array."""
        arr = list(range(1, 101))
        for k in [1, 25, 50, 75, 100]:
            self.assertEqual(median_of_medians(arr, k), k)
    
    def test_reverse_sorted_array(self):
        """Test on reverse-sorted array."""
        arr = list(range(100, 0, -1))
        for k in [1, 25, 50, 75, 100]:
            self.assertEqual(median_of_medians(arr, k), k)
    
    def test_duplicates(self):
        """Test with duplicate elements."""
        arr = [5, 5, 5, 5, 5, 1, 1, 1, 9, 9]
        sorted_arr = sorted(arr)
        for k in range(1, len(arr) + 1):
            self.assertEqual(median_of_medians(arr, k), sorted_arr[k-1])
    
    def test_single_element(self):
        """Test with single element."""
        self.assertEqual(median_of_medians([42], 1), 42)
    
    def test_two_elements(self):
        """Test with two elements."""
        self.assertEqual(median_of_medians([5, 3], 1), 3)
        self.assertEqual(median_of_medians([5, 3], 2), 5)
    
    def test_empty_array(self):
        """Test with empty array."""
        self.assertIsNone(median_of_medians([], 1))
    
    def test_invalid_k(self):
        """Test with invalid k values."""
        arr = [1, 2, 3, 4, 5]
        self.assertIsNone(median_of_medians(arr, 0))
        self.assertIsNone(median_of_medians(arr, 6))
        self.assertIsNone(median_of_medians(arr, -1))
    
    def test_large_random_array(self):
        """Test with large random array."""
        arr = [random.randint(1, 10000) for _ in range(1000)]
        sorted_arr = sorted(arr)
        
        # Test various k values
        for k in [1, 100, 500, 750, 1000]:
            result = median_of_medians(arr, k)
            self.assertEqual(result, sorted_arr[k-1])
    
    def test_original_not_modified(self):
        """Test that original array is not modified."""
        arr = [5, 3, 8, 1, 9, 2]
        original = arr.copy()
        median_of_medians(arr, 3)
        self.assertEqual(arr, original)


class TestRandomizedSelect(unittest.TestCase):
    """Tests for Randomized Quickselect algorithm."""
    
    def test_basic_selection(self):
        """Test basic k-th smallest selection."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        
        # 1st smallest (minimum)
        self.assertEqual(randomized_select(arr, 1), 1)
        
        # Last (maximum)
        self.assertEqual(randomized_select(arr, len(arr)), 9)
    
    def test_sorted_array(self):
        """Test on sorted array."""
        arr = list(range(1, 101))
        for k in [1, 25, 50, 75, 100]:
            self.assertEqual(randomized_select(arr, k), k)
    
    def test_reverse_sorted_array(self):
        """Test on reverse-sorted array."""
        arr = list(range(100, 0, -1))
        for k in [1, 25, 50, 75, 100]:
            self.assertEqual(randomized_select(arr, k), k)
    
    def test_duplicates(self):
        """Test with duplicate elements."""
        arr = [5, 5, 5, 5, 5, 1, 1, 1, 9, 9]
        sorted_arr = sorted(arr)
        for k in range(1, len(arr) + 1):
            self.assertEqual(randomized_select(arr, k), sorted_arr[k-1])
    
    def test_single_element(self):
        """Test with single element."""
        self.assertEqual(randomized_select([42], 1), 42)
    
    def test_empty_array(self):
        """Test with empty array."""
        self.assertIsNone(randomized_select([], 1))
    
    def test_invalid_k(self):
        """Test with invalid k values."""
        arr = [1, 2, 3, 4, 5]
        self.assertIsNone(randomized_select(arr, 0))
        self.assertIsNone(randomized_select(arr, 6))
    
    def test_large_random_array(self):
        """Test with large random array."""
        arr = [random.randint(1, 10000) for _ in range(1000)]
        sorted_arr = sorted(arr)
        
        for k in [1, 100, 500, 750, 1000]:
            result = randomized_select(arr, k)
            self.assertEqual(result, sorted_arr[k-1])
    
    def test_original_not_modified(self):
        """Test that original array is not modified."""
        arr = [5, 3, 8, 1, 9, 2]
        original = arr.copy()
        randomized_select(arr, 3)
        self.assertEqual(arr, original)


class TestHelperFunctions(unittest.TestCase):
    """Tests for helper functions."""
    
    def test_find_median(self):
        """Test find_median function."""
        self.assertEqual(find_median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(find_median([1, 2, 3, 4]), 2)  # Lower median for even
        self.assertEqual(find_median([5]), 5)
        self.assertIsNone(find_median([]))
    
    def test_find_kth_largest(self):
        """Test find_kth_largest function."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        self.assertEqual(find_kth_largest(arr, 1), 9)  # Maximum
        self.assertEqual(find_kth_largest(arr, 2), 6)  # Second largest
        self.assertEqual(find_kth_largest(arr, len(arr)), 1)  # Minimum


class TestAlgorithmConsistency(unittest.TestCase):
    """Test that both algorithms produce consistent results."""
    
    def test_same_results(self):
        """Both algorithms should return same result."""
        for _ in range(10):
            arr = [random.randint(1, 1000) for _ in range(100)]
            k = random.randint(1, len(arr))
            
            mom_result = median_of_medians(arr, k)
            rs_result = randomized_select(arr, k)
            
            self.assertEqual(mom_result, rs_result,
                           f"Mismatch for k={k}: MoM={mom_result}, RS={rs_result}")


if __name__ == '__main__':
    unittest.main()
