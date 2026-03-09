"""
Timing utilities for performance measurement.
"""

import time
import statistics
from typing import Callable, List, Any, Dict


def measure_time(func: Callable, *args, **kwargs) -> tuple:
    """
    Measure execution time of a function.
    
    Returns:
        Tuple of (result, elapsed_time_seconds)
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def measure_average_time(func: Callable, args_list: List[tuple], trials: int = 5) -> Dict[str, float]:
    """
    Measure average execution time over multiple trials.
    
    Args:
        func: Function to measure
        args_list: List of argument tuples
        trials: Number of trials per argument set
        
    Returns:
        Dictionary with timing statistics
    """
    times = []
    
    for args in args_list:
        for _ in range(trials):
            _, elapsed = measure_time(func, *args)
            times.append(elapsed)
    
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times),
        'trials': len(times)
    }


def benchmark_function(func: Callable, sizes: List[int], generator: Callable, 
                       trials: int = 5, k_position: str = 'median') -> List[Dict]:
    """
    Benchmark a selection function across different input sizes.
    
    Args:
        func: Selection function to benchmark
        sizes: List of input sizes
        generator: Function to generate input arrays
        trials: Number of trials per size
        k_position: 'median', 'first', 'last', or 'random' for k value
        
    Returns:
        List of result dictionaries with timing info
    """
    import random
    
    results = []
    
    for size in sizes:
        times = []
        
        for _ in range(trials):
            arr = generator(size)
            
            # Determine k value
            if k_position == 'median':
                k = (size + 1) // 2
            elif k_position == 'first':
                k = 1
            elif k_position == 'last':
                k = size
            else:  # random
                k = random.randint(1, size)
            
            _, elapsed = measure_time(func, arr, k)
            times.append(elapsed)
        
        results.append({
            'size': size,
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times)
        })
    
    return results


def format_time(seconds: float) -> str:
    """Format time in human-readable format."""
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} μs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds:.3f} s"


def print_timing_table(results: List[Dict], title: str = "") -> None:
    """Print timing results in a formatted table."""
    if title:
        print(f"\n{title}")
        print("=" * 70)
    
    print(f"{'Size':>10} | {'Mean':>12} | {'Median':>12} | {'Std Dev':>12} | {'Min':>12}")
    print("-" * 70)
    
    for r in results:
        print(f"{r['size']:>10} | {format_time(r['mean']):>12} | "
              f"{format_time(r['median']):>12} | {format_time(r['stdev']):>12} | "
              f"{format_time(r['min']):>12}")
