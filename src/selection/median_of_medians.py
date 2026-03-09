"""
Median of Medians (Deterministic Selection) Algorithm

This algorithm selects the k-th smallest element in O(n) worst-case time.
Also known as BFPRT algorithm after Blum, Floyd, Pratt, Rivest, and Tarjan (1973).

Key Insight:
    By choosing the median of medians as the pivot, we guarantee that at least
    30% of elements are less than the pivot and at least 30% are greater.
    This ensures that each recursive call reduces the problem size by at least
    a constant fraction, leading to O(n) worst-case time complexity.

Time Complexity Analysis:
    Let T(n) be the time to select from n elements.
    
    Step 1: Divide into groups of 5                          → O(n)
    Step 2: Find median of each group                        → O(n) [constant time per group]
    Step 3: Recursively find median of medians               → T(n/5)
    Step 4: Partition around median of medians               → O(n)
    Step 5: Recurse on one side (at most 7n/10 elements)     → T(7n/10)
    
    Recurrence: T(n) = T(n/5) + T(7n/10) + O(n)
    
    By substitution or master theorem variant:
    T(n) = cn for some constant c, confirming O(n) complexity.

Space Complexity: O(log n) due to recursion stack
"""

from typing import List, Any, Optional
from .utils import validate_array, validate_k, partition, get_median


def median_of_medians(arr: List[Any], k: int) -> Optional[Any]:
    """
    Find the k-th smallest element using the Median of Medians algorithm.
    
    This deterministic algorithm guarantees O(n) worst-case time complexity
    by carefully choosing a pivot that ensures balanced partitioning.
    
    Args:
        arr: Input array (will not be modified, a copy is used internally)
        k: The k-th smallest element to find (1-indexed, i.e., k=1 returns minimum)
        
    Returns:
        The k-th smallest element, or None if invalid input
        
    Examples:
        >>> median_of_medians([3, 1, 4, 1, 5, 9, 2, 6], 1)
        1
        >>> median_of_medians([3, 1, 4, 1, 5, 9, 2, 6], 4)
        3
        >>> median_of_medians([3, 1, 4, 1, 5, 9, 2, 6], 8)
        9
        
    Time Complexity: O(n) worst-case
    Space Complexity: O(n) for copy + O(log n) for recursion = O(n)
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
    return _select(arr_copy, 0, len(arr_copy) - 1, k - 1)  # Convert to 0-indexed


def _select(arr: List[Any], low: int, high: int, k: int) -> Any:
    """
    Internal recursive selection function.
    
    Args:
        arr: Array to search (modified in-place during partitioning)
        low: Lower bound of search range
        high: Upper bound of search range
        k: 0-indexed position of element to find (k-th smallest has index k)
        
    Returns:
        The element at position k after the array would be sorted
    """
    # Base case: single element
    if low == high:
        return arr[low]
    
    # Find pivot using median of medians
    pivot_idx = _get_pivot_index(arr, low, high)
    
    # Partition around pivot
    pivot_idx = partition(arr, low, high, pivot_idx)
    
    # Determine which partition contains k-th element
    if k == pivot_idx:
        return arr[k]
    elif k < pivot_idx:
        return _select(arr, low, pivot_idx - 1, k)
    else:
        return _select(arr, pivot_idx + 1, high, k)


def _get_pivot_index(arr: List[Any], low: int, high: int) -> int:
    """
    Find the index of median of medians to use as pivot.
    
    Process:
    1. Divide array into groups of 5
    2. Find median of each group using simple sort (O(1) per group)
    3. Recursively find median of these medians
    4. Return index of this median in original array
    
    Args:
        arr: Array to find pivot from
        low: Lower bound
        high: Upper bound
        
    Returns:
        Index of the median of medians element
        
    Why groups of 5?
        - 5 is small enough that sorting each group is O(1)
        - 5 provides a good balance: ensures at least 3n/10 elements on each side
        - Odd number ensures a unique median
        - Mathematical analysis shows 5 is optimal for constant factors
    """
    n = high - low + 1
    
    # For small arrays, just return median index directly
    if n <= 5:
        sorted_indices = sorted(range(low, high + 1), key=lambda i: arr[i])
        return sorted_indices[len(sorted_indices) // 2]
    
    # Divide into groups of 5 and find medians
    medians = []
    median_indices = []
    
    for i in range(low, high + 1, 5):
        group_end = min(i + 5, high + 1)
        group = arr[i:group_end]
        group_indices = list(range(i, group_end))
        
        # Sort group indices by their values
        sorted_group_indices = sorted(group_indices, key=lambda idx: arr[idx])
        median_idx = sorted_group_indices[len(sorted_group_indices) // 2]
        
        medians.append(arr[median_idx])
        median_indices.append(median_idx)
    
    # Recursively find median of medians
    if len(medians) <= 5:
        # Base case: find median directly
        sorted_indices = sorted(range(len(medians)), key=lambda i: medians[i])
        return median_indices[sorted_indices[len(sorted_indices) // 2]]
    else:
        # Recursive case: find median of medians
        mom = median_of_medians(medians, (len(medians) + 1) // 2)
        # Find index of mom in original array
        for idx in median_indices:
            if arr[idx] == mom:
                return idx
        return median_indices[0]  # Fallback


def median_of_medians_with_stats(arr: List[Any], k: int) -> dict:
    """
    Find k-th smallest element and return statistics about the computation.
    
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
        
        # Count comparisons during pivot finding
        n = high - low + 1
        stats['comparisons'] += n  # Approximate comparisons for grouping
        
        pivot_idx = _get_pivot_index(arr, low, high)
        pivot_idx = partition(arr, low, high, pivot_idx)
        stats['comparisons'] += (high - low + 1)  # Partition comparisons
        
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
