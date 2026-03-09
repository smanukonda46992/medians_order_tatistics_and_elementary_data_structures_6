"""
Randomized Quickselect Algorithm

This algorithm selects the k-th smallest element in O(n) expected time.
It's a modification of Quicksort that only recurses into one partition.

Key Insight:
    Unlike sorting, where we need all elements in order, selection only
    needs to identify one element. By randomly choosing pivots, we achieve
    O(n) expected time with high probability.

Time Complexity Analysis:
    Expected Case: O(n)
    
    Let T(n) be the expected time to select from n elements.
    With a random pivot, on average the partition splits the array roughly in half.
    
    E[T(n)] = n + (1/n) * Σ(i=0 to n-1) max(T(i), T(n-i-1))
    
    Analysis shows this resolves to O(n) expected time.
    
    Intuition: Each element is expected to be in only O(1) partitioning operations.
    
    Worst Case: O(n²)
    Occurs when pivot always selects minimum or maximum element.
    Probability of this is negligible: (2/n) * (2/(n-1)) * ... = O(1/n!)

Space Complexity: O(log n) expected due to recursion stack
    Worst case O(n) if all pivots are bad (highly unlikely)

Comparison with Median of Medians:
    - Randomized Select is simpler and faster in practice (lower constants)
    - Median of Medians guarantees O(n) worst-case
    - For most applications, Randomized Select is preferred
    - Use Median of Medians when adversarial input is possible
"""

import random
from typing import List, Any, Optional
from .utils import validate_array, validate_k, partition


def randomized_select(arr: List[Any], k: int) -> Optional[Any]:
    """
    Find the k-th smallest element using Randomized Quickselect.
    
    This randomized algorithm achieves O(n) expected time complexity
    by randomly choosing pivot elements, avoiding worst-case scenarios
    with high probability.
    
    Args:
        arr: Input array (will not be modified, a copy is used internally)
        k: The k-th smallest element to find (1-indexed, i.e., k=1 returns minimum)
        
    Returns:
        The k-th smallest element, or None if invalid input
        
    Examples:
        >>> randomized_select([3, 1, 4, 1, 5, 9, 2, 6], 1)
        1
        >>> randomized_select([3, 1, 4, 1, 5, 9, 2, 6], 4)
        3
        >>> randomized_select([3, 1, 4, 1, 5, 9, 2, 6], 8)
        9
        
    Time Complexity: O(n) expected, O(n²) worst case
    Space Complexity: O(n) for copy + O(log n) expected for recursion = O(n)
    """
    # Input validation
    if not validate_array(arr):
        return None
    if len(arr) == 0:
        return None
    if not validate_k(arr, k):
        return None
    
    # Work on a copy to avoid modifying input
    arr_copy = arr.copy()
    return _randomized_select(arr_copy, 0, len(arr_copy) - 1, k - 1)


def _randomized_select(arr: List[Any], low: int, high: int, k: int) -> Any:
    """
    Internal recursive randomized selection function.
    
    The key difference from Median of Medians is the pivot selection:
    instead of computing median of medians (deterministic), we simply
    choose a random element as pivot.
    
    Why Random Pivot Works:
        - On average, a random pivot gives a reasonably balanced partition
        - Even if some partitions are unbalanced, the expected total work is O(n)
        - The probability of consistently bad pivots is vanishingly small
    
    Args:
        arr: Array to search (modified in-place during partitioning)
        low: Lower bound of search range
        high: Upper bound of search range
        k: 0-indexed position of element to find
        
    Returns:
        The element at position k after the array would be sorted
    """
    # Base case: single element
    if low == high:
        return arr[low]
    
    # Choose random pivot
    pivot_idx = random.randint(low, high)
    
    # Partition around random pivot
    pivot_idx = partition(arr, low, high, pivot_idx)
    
    # Determine which partition contains k-th element
    # This is where selection differs from sorting:
    # we only recurse into ONE partition, not both
    if k == pivot_idx:
        return arr[k]
    elif k < pivot_idx:
        return _randomized_select(arr, low, pivot_idx - 1, k)
    else:
        return _randomized_select(arr, pivot_idx + 1, high, k)


def randomized_select_iterative(arr: List[Any], k: int) -> Optional[Any]:
    """
    Iterative version of Randomized Quickselect.
    
    Uses O(1) extra space instead of O(log n) for recursion stack.
    Preferred when stack space is limited or for very large arrays.
    
    Args:
        arr: Input array (will not be modified)
        k: Position of element to find (1-indexed)
        
    Returns:
        The k-th smallest element
        
    Time Complexity: O(n) expected
    Space Complexity: O(n) for array copy, O(1) auxiliary
    """
    if not validate_array(arr) or len(arr) == 0 or not validate_k(arr, k):
        return None
    
    arr_copy = arr.copy()
    low, high = 0, len(arr_copy) - 1
    k_idx = k - 1  # Convert to 0-indexed
    
    while low < high:
        # Random pivot selection
        pivot_idx = random.randint(low, high)
        pivot_idx = partition(arr_copy, low, high, pivot_idx)
        
        if k_idx == pivot_idx:
            return arr_copy[k_idx]
        elif k_idx < pivot_idx:
            high = pivot_idx - 1
        else:
            low = pivot_idx + 1
    
    return arr_copy[low]


def randomized_select_with_stats(arr: List[Any], k: int) -> dict:
    """
    Find k-th smallest element and return statistics about the computation.
    
    Useful for empirical analysis and comparing with Median of Medians.
    
    Args:
        arr: Input array
        k: Position of element to find (1-indexed)
        
    Returns:
        Dictionary containing:
            - 'result': The k-th smallest element
            - 'comparisons': Number of comparisons made
            - 'recursive_calls': Number of recursive calls
            - 'array_size': Original array size
    """
    stats = {'comparisons': 0, 'recursive_calls': 0}
    
    def _select_stats(arr, low, high, k):
        stats['recursive_calls'] += 1
        
        if low == high:
            return arr[low]
        
        # Random pivot selection
        pivot_idx = random.randint(low, high)
        
        # Count comparisons during partition
        stats['comparisons'] += (high - low + 1)
        
        pivot_idx = partition(arr, low, high, pivot_idx)
        
        if k == pivot_idx:
            return arr[k]
        elif k < pivot_idx:
            return _select_stats(arr, low, pivot_idx - 1, k)
        else:
            return _select_stats(arr, pivot_idx + 1, high, k)
    
    if not validate_array(arr) or len(arr) == 0 or not validate_k(arr, k):
        return {'result': None, 'comparisons': 0, 'recursive_calls': 0, 'array_size': 0}
    
    arr_copy = arr.copy()
    result = _select_stats(arr_copy, 0, len(arr_copy) - 1, k - 1)
    
    return {
        'result': result,
        'comparisons': stats['comparisons'],
        'recursive_calls': stats['recursive_calls'],
        'array_size': len(arr)
    }


def find_median(arr: List[Any]) -> Optional[Any]:
    """
    Find the median of an array using Randomized Select.
    
    For even-length arrays, returns the lower median.
    
    Args:
        arr: Input array
        
    Returns:
        Median element
        
    Time Complexity: O(n) expected
    """
    if not arr:
        return None
    k = (len(arr) + 1) // 2
    return randomized_select(arr, k)


def find_kth_largest(arr: List[Any], k: int) -> Optional[Any]:
    """
    Find the k-th largest element (convenience function).
    
    Args:
        arr: Input array
        k: Position from largest (1 = maximum)
        
    Returns:
        The k-th largest element
    """
    if not arr or k < 1 or k > len(arr):
        return None
    # k-th largest = (n - k + 1)-th smallest
    return randomized_select(arr, len(arr) - k + 1)
