"""
Input generators for selection algorithm experiments.
"""

import random
from typing import List, Callable, Dict


def generate_random_array(size: int, min_val: int = 0, max_val: int = None) -> List[int]:
    """Generate array with random integers."""
    if max_val is None:
        max_val = size * 10
    return [random.randint(min_val, max_val) for _ in range(size)]


def generate_sorted_array(size: int) -> List[int]:
    """Generate sorted array [0, 1, 2, ..., size-1]."""
    return list(range(size))


def generate_reverse_sorted_array(size: int) -> List[int]:
    """Generate reverse-sorted array [size-1, size-2, ..., 0]."""
    return list(range(size - 1, -1, -1))


def generate_duplicates_array(size: int, num_unique: int = 10) -> List[int]:
    """Generate array with many duplicate values."""
    unique_vals = [random.randint(0, size) for _ in range(num_unique)]
    return [random.choice(unique_vals) for _ in range(size)]


def generate_nearly_sorted_array(size: int, swaps: int = None) -> List[int]:
    """Generate nearly sorted array with some elements swapped."""
    if swaps is None:
        swaps = size // 10
    arr = list(range(size))
    for _ in range(swaps):
        i, j = random.randint(0, size - 1), random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def generate_all_same_array(size: int) -> List[int]:
    """Generate array where all elements are the same."""
    return [42] * size


def generate_alternating_array(size: int) -> List[int]:
    """Generate array with alternating high and low values."""
    return [i if i % 2 == 0 else size - i for i in range(size)]


# Dictionary of all generators for easy iteration
GENERATORS: Dict[str, Callable[[int], List[int]]] = {
    'random': generate_random_array,
    'sorted': generate_sorted_array,
    'reverse': generate_reverse_sorted_array,
    'duplicates': generate_duplicates_array,
    'nearly_sorted': generate_nearly_sorted_array,
    'all_same': generate_all_same_array,
    'alternating': generate_alternating_array,
}


def get_generator(name: str) -> Callable[[int], List[int]]:
    """Get generator by name."""
    return GENERATORS.get(name, generate_random_array)
