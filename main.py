#!/usr/bin/env python3
"""
Assignment 6: Medians, Order Statistics & Elementary Data Structures
Author: smanukonda46992

Usage: python main.py [all|selection|datastructures|demo|tests]
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def run_selection_experiments():
    """Run selection algorithm comparison experiments."""
    print("\n" + "=" * 60)
    print("SELECTION ALGORITHM EXPERIMENTS")
    print("=" * 60)
    from experiments.run_selection_experiments import run_experiments
    run_experiments()


def run_data_structure_experiments():
    """Run data structure experiments."""
    print("\n" + "=" * 60)
    print("DATA STRUCTURE EXPERIMENTS")
    print("=" * 60)
    from experiments.run_data_structure_experiments import run_experiments
    run_experiments()


def run_tests():
    """Run unit tests."""
    print("\n" + "=" * 60)
    print("UNIT TESTS")
    print("=" * 60)
    import unittest
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite).wasSuccessful()


def run_demo():
    """Run demonstrations."""
    print("\n" + "=" * 60)
    print("SELECTION ALGORITHMS DEMO")
    print("=" * 60)
    
    from src.selection import median_of_medians, randomized_select
    
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7]
    print(f"Array: {arr}")
    print(f"Length: {len(arr)}")
    
    for k in [1, 5, 7, len(arr)]:
        mom_result = median_of_medians(arr.copy(), k)
        rs_result = randomized_select(arr.copy(), k)
        print(f"\n{k}th smallest:")
        print(f"  Median of Medians: {mom_result}")
        print(f"  Randomized Select: {rs_result}")
    
    print("\n" + "=" * 60)
    print("DATA STRUCTURES DEMO")
    print("=" * 60)
    
    # Dynamic Array Demo
    from src.data_structures import DynamicArray
    print("\n--- Dynamic Array ---")
    darr = DynamicArray()
    for i in [10, 20, 30, 40, 50]:
        darr.append(i)
    print(f"After appending 10,20,30,40,50: {darr}")
    darr.insert(2, 25)
    print(f"After inserting 25 at index 2: {darr}")
    darr.delete(0)
    print(f"After deleting at index 0: {darr}")
    print(f"Access index 2: {darr[2]}")
    
    # Stack Demo
    from src.data_structures import Stack
    print("\n--- Stack (LIFO) ---")
    stack = Stack()
    for i in [1, 2, 3, 4, 5]:
        stack.push(i)
    print(f"After pushing 1,2,3,4,5: {stack}")
    print(f"Pop: {stack.pop()}")
    print(f"Pop: {stack.pop()}")
    print(f"Peek: {stack.peek()}")
    print(f"Stack now: {stack}")
    
    # Queue Demo
    from src.data_structures import Queue
    print("\n--- Queue (FIFO) ---")
    queue = Queue()
    for i in [1, 2, 3, 4, 5]:
        queue.enqueue(i)
    print(f"After enqueueing 1,2,3,4,5: {queue}")
    print(f"Dequeue: {queue.dequeue()}")
    print(f"Dequeue: {queue.dequeue()}")
    print(f"Front: {queue.front()}")
    print(f"Queue now: {queue}")
    
    # Linked List Demo
    from src.data_structures import LinkedList
    print("\n--- Singly Linked List ---")
    ll = LinkedList()
    ll.insert_front(3)
    ll.insert_front(2)
    ll.insert_front(1)
    ll.insert_end(4)
    ll.insert_end(5)
    print(f"After inserting 1,2,3 at front and 4,5 at end:")
    ll.display()
    ll.delete(3)
    print(f"After deleting 3:")
    ll.display()
    print(f"Search for 4: {ll.search(4)}")
    print(f"Search for 10: {ll.search(10)}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Assignment 6: Medians, Order Statistics & Elementary DS")
    print("=" * 60)
    
    command = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    if command == 'all':
        run_demo()
        run_selection_experiments()
        run_data_structure_experiments()
    elif command == 'selection':
        run_selection_experiments()
    elif command == 'datastructures':
        run_data_structure_experiments()
    elif command == 'demo':
        run_demo()
    elif command == 'tests':
        sys.exit(0 if run_tests() else 1)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
