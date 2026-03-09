"""
Data Structure Experiments

Compares performance of different data structures for various operations.
"""

import sys
import time
import random
from pathlib import Path
from typing import List, Dict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_structures import DynamicArray, Stack, Queue, LinkedList
from experiments.timing_utils import format_time


def benchmark_dynamic_array(sizes: List[int], trials: int = 3) -> Dict:
    """Benchmark DynamicArray operations."""
    results = {'append': [], 'insert_front': [], 'access': [], 'delete': [], 'search': []}
    
    for size in sizes:
        # Append
        times = []
        for _ in range(trials):
            arr = DynamicArray()
            start = time.perf_counter()
            for i in range(size):
                arr.append(i)
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)  # Per-operation time
        results['append'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Insert at front (expensive)
        if size <= 5000:  # Limit for O(n²) operations
            times = []
            for _ in range(trials):
                arr = DynamicArray()
                start = time.perf_counter()
                for i in range(min(size, 1000)):
                    arr.insert(0, i)
                elapsed = time.perf_counter() - start
                times.append(elapsed / min(size, 1000))
            results['insert_front'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Random access
        arr = DynamicArray.from_list(list(range(size)))
        times = []
        for _ in range(trials):
            start = time.perf_counter()
            for _ in range(size):
                _ = arr[random.randint(0, size - 1)]
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)
        results['access'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Search
        times = []
        for _ in range(trials):
            start = time.perf_counter()
            for _ in range(100):
                arr.search(random.randint(0, size - 1))
            elapsed = time.perf_counter() - start
            times.append(elapsed / 100)
        results['search'].append({'size': size, 'mean': sum(times) / len(times)})
    
    return results


def benchmark_stack(sizes: List[int], trials: int = 3) -> Dict:
    """Benchmark Stack operations."""
    results = {'push': [], 'pop': [], 'peek': []}
    
    for size in sizes:
        # Push
        times = []
        for _ in range(trials):
            stack = Stack()
            start = time.perf_counter()
            for i in range(size):
                stack.push(i)
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)
        results['push'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Pop
        times = []
        for _ in range(trials):
            stack = Stack.from_list(list(range(size)))
            start = time.perf_counter()
            while not stack.is_empty():
                stack.pop()
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)
        results['pop'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Peek
        stack = Stack.from_list(list(range(size)))
        times = []
        for _ in range(trials):
            start = time.perf_counter()
            for _ in range(size):
                stack.peek()
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)
        results['peek'].append({'size': size, 'mean': sum(times) / len(times)})
    
    return results


def benchmark_queue(sizes: List[int], trials: int = 3) -> Dict:
    """Benchmark Queue operations."""
    results = {'enqueue': [], 'dequeue': [], 'front': []}
    
    for size in sizes:
        # Enqueue
        times = []
        for _ in range(trials):
            queue = Queue()
            start = time.perf_counter()
            for i in range(size):
                queue.enqueue(i)
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)
        results['enqueue'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Dequeue
        times = []
        for _ in range(trials):
            queue = Queue.from_list(list(range(size)))
            start = time.perf_counter()
            while not queue.is_empty():
                queue.dequeue()
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)
        results['dequeue'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Front (peek)
        queue = Queue.from_list(list(range(size)))
        times = []
        for _ in range(trials):
            start = time.perf_counter()
            for _ in range(size):
                queue.front()
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)
        results['front'].append({'size': size, 'mean': sum(times) / len(times)})
    
    return results


def benchmark_linked_list(sizes: List[int], trials: int = 3) -> Dict:
    """Benchmark LinkedList operations."""
    results = {'insert_front': [], 'insert_end': [], 'delete_front': [], 'search': [], 'traverse': []}
    
    for size in sizes:
        # Insert at front
        times = []
        for _ in range(trials):
            ll = LinkedList()
            start = time.perf_counter()
            for i in range(size):
                ll.insert_front(i)
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)
        results['insert_front'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Insert at end
        times = []
        for _ in range(trials):
            ll = LinkedList()
            start = time.perf_counter()
            for i in range(size):
                ll.insert_end(i)
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)
        results['insert_end'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Delete from front
        times = []
        for _ in range(trials):
            ll = LinkedList.from_list(list(range(size)))
            start = time.perf_counter()
            while not ll.is_empty():
                ll.delete_front()
            elapsed = time.perf_counter() - start
            times.append(elapsed / size)
        results['delete_front'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Search
        ll = LinkedList.from_list(list(range(size)))
        times = []
        for _ in range(trials):
            start = time.perf_counter()
            for _ in range(100):
                ll.search(random.randint(0, size - 1))
            elapsed = time.perf_counter() - start
            times.append(elapsed / 100)
        results['search'].append({'size': size, 'mean': sum(times) / len(times)})
        
        # Traverse
        ll = LinkedList.from_list(list(range(size)))
        times = []
        for _ in range(trials):
            start = time.perf_counter()
            ll.traverse()
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        results['traverse'].append({'size': size, 'mean': sum(times) / len(times)})
    
    return results


def print_ds_results(name: str, results: Dict) -> None:
    """Print data structure benchmark results."""
    print(f"\n{name} Benchmark Results")
    print("=" * 70)
    
    for op_name, op_results in results.items():
        print(f"\n{op_name}:")
        print(f"  {'Size':>10} | {'Time/Op':>15}")
        print(f"  {'-'*10}-+-{'-'*15}")
        for r in op_results:
            print(f"  {r['size']:>10} | {format_time(r['mean']):>15}")


def run_experiments():
    """Run all data structure experiments."""
    
    # Ensure results directories exist
    results_dir = PROJECT_ROOT / 'results'
    plots_dir = results_dir / 'plots'
    data_dir = results_dir / 'raw_data'
    plots_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    trials = 3
    
    print("\n" + "=" * 70)
    print("DATA STRUCTURE EXPERIMENTS")
    print("=" * 70)
    print(f"\nInput sizes: {sizes}")
    print(f"Trials per size: {trials}")
    
    # Run benchmarks
    print("\nRunning Dynamic Array benchmarks...")
    array_results = benchmark_dynamic_array(sizes, trials)
    print_ds_results("Dynamic Array", array_results)
    
    print("\nRunning Stack benchmarks...")
    stack_results = benchmark_stack(sizes, trials)
    print_ds_results("Stack", stack_results)
    
    print("\nRunning Queue benchmarks...")
    queue_results = benchmark_queue(sizes, trials)
    print_ds_results("Queue", queue_results)
    
    print("\nRunning Linked List benchmarks...")
    ll_results = benchmark_linked_list(sizes, trials)
    print_ds_results("Linked List", ll_results)
    
    # Generate comparison plots
    try:
        from experiments.plot_results import plot_ds_comparison
        plot_ds_comparison(
            sizes,
            {
                'DynamicArray': array_results,
                'Stack': stack_results,
                'Queue': queue_results,
                'LinkedList': ll_results
            },
            str(plots_dir)
        )
        print(f"\nPlots saved to {plots_dir}")
    except ImportError as e:
        print(f"\nNote: Could not generate plots ({e})")
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY: DATA STRUCTURE TRADE-OFFS")
    print("=" * 70)
    print("""
ARRAYS (Dynamic Array):
  ✓ O(1) random access - excellent for index-based retrieval
  ✓ O(1) amortized append - efficient for building sequences
  ✓ Good cache locality - fast sequential access
  ✗ O(n) insertion/deletion at arbitrary positions
  ✗ May waste space during resize operations

STACKS (Array-based):
  ✓ O(1) push/pop/peek - optimal for LIFO operations
  ✓ Simple implementation with arrays
  ✓ Good for function calls, undo operations, expression parsing
  ✗ Only efficient access to top element

QUEUES (Circular Array):
  ✓ O(1) enqueue/dequeue - optimal for FIFO operations
  ✓ No element shifting needed (circular design)
  ✓ Good for BFS, task scheduling, buffering
  ✗ Fixed capacity (unless dynamic resizing)

LINKED LISTS:
  ✓ O(1) insertion at front - no shifting needed
  ✓ O(1) deletion at front
  ✓ Dynamic size - no wasted capacity
  ✓ Easy to implement stacks/queues
  ✗ O(n) random access - must traverse from head
  ✗ Poor cache locality - nodes scattered in memory
  ✗ Extra memory for pointers

WHEN TO USE WHAT:
  - Need random access? → Array
  - Frequent insertions at front? → Linked List
  - LIFO operations? → Stack (array-based)
  - FIFO operations? → Queue (circular array)
  - Unknown size, frequent modifications? → Linked List
  - Known size, frequent lookups? → Array
""")
    
    return {
        'array': array_results,
        'stack': stack_results,
        'queue': queue_results,
        'linked_list': ll_results
    }


if __name__ == "__main__":
    run_experiments()
