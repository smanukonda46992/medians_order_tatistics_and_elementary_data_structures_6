"""
Utility functions for selection algorithms.
"""

from typing import List, Any


def validate_array(arr: List[Any]) -> bool:
    """
    Validate that input is a valid list.
    
    Args:
        arr: Input to validate
        
    Returns:
        True if valid, False otherwise
    """
    if arr is None:
        return False
    if not isinstance(arr, list):
        return False
    return True


def validate_k(arr: List[Any], k: int) -> bool:
    """
    Validate that k is within valid bounds.
    
    Args:
        arr: Input array
        k: The k-th smallest element to find (1-indexed)
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(k, int):
        return False
    if k < 1 or k > len(arr):
        return False
    return True


def partition(arr: List[Any], low: int, high: int, pivot_idx: int) -> int:
    """
    Partition array around pivot element.
    
    This is a standard Lomuto partition scheme modified to accept
    a specific pivot index. Elements smaller than pivot go to left,
    elements larger go to right.
    
    Args:
        arr: Array to partition (modified in-place)
        low: Lower bound index
        high: Upper bound index
        pivot_idx: Index of pivot element
        
    Returns:
        Final position of pivot element after partitioning
        
    Time Complexity: O(high - low + 1) = O(n) for the range
    Space Complexity: O(1)
    """
    # Move pivot to end
    pivot = arr[pivot_idx]
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    
    # Standard Lomuto partition
    store_idx = low
    for i in range(low, high):
        if arr[i] < pivot:
            arr[store_idx], arr[i] = arr[i], arr[store_idx]
            store_idx += 1
    
    # Move pivot to final position
    arr[store_idx], arr[high] = arr[high], arr[store_idx]
    
    return store_idx


def insertion_sort(arr: List[Any]) -> List[Any]:
    """
    Sort array using insertion sort.
    
    Used for small arrays (groups of 5) in Median of Medians algorithm.
    
    Args:
        arr: Array to sort
        
    Returns:
        Sorted array
        
    Time Complexity: O(n^2) worst case, O(n) best case
    Space Complexity: O(1)
    """
    result = arr.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def get_median(arr: List[Any]) -> Any:
    """
    Get median of a small array using insertion sort.
    
    Args:
        arr: Array to find median of (typically size <= 5)
        
    Returns:
        Median element
        
    Time Complexity: O(n^2) but n <= 5, so effectively O(1)
    Space Complexity: O(n) for sorted copy
    """
    sorted_arr = insertion_sort(arr)
    return sorted_arr[len(sorted_arr) // 2]
