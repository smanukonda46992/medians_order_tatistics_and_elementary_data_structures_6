"""
Elementary Data Structures Module

Provides implementations of:
- DynamicArray: Resizable array with amortized O(1) append
- Matrix: 2D array with basic operations
- Stack: LIFO data structure
- Queue: FIFO data structure
- LinkedList: Singly linked list
- RootedTree: Tree using linked representation
"""

from .dynamic_array import DynamicArray
from .matrix import Matrix
from .stack import Stack
from .queue import Queue
from .linked_list import LinkedList, Node
from .rooted_tree import RootedTree, TreeNode

__all__ = [
    'DynamicArray',
    'Matrix',
    'Stack',
    'Queue',
    'LinkedList',
    'Node',
    'RootedTree',
    'TreeNode'
]
