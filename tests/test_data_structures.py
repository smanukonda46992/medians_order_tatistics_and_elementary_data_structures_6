"""
Unit tests for elementary data structures.
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_structures import DynamicArray, Matrix, Stack, Queue, LinkedList, RootedTree


class TestDynamicArray(unittest.TestCase):
    """Tests for DynamicArray."""
    
    def test_append(self):
        """Test append operation."""
        arr = DynamicArray()
        for i in range(10):
            arr.append(i)
        self.assertEqual(len(arr), 10)
        self.assertEqual(arr[0], 0)
        self.assertEqual(arr[9], 9)
    
    def test_insert(self):
        """Test insert operation."""
        arr = DynamicArray.from_list([1, 2, 4, 5])
        arr.insert(2, 3)
        self.assertEqual(arr.to_list(), [1, 2, 3, 4, 5])
    
    def test_delete(self):
        """Test delete operation."""
        arr = DynamicArray.from_list([1, 2, 3, 4, 5])
        deleted = arr.delete(2)
        self.assertEqual(deleted, 3)
        self.assertEqual(arr.to_list(), [1, 2, 4, 5])
    
    def test_access(self):
        """Test random access."""
        arr = DynamicArray.from_list([10, 20, 30, 40, 50])
        self.assertEqual(arr[0], 10)
        self.assertEqual(arr[2], 30)
        self.assertEqual(arr[-1], 50)
    
    def test_search(self):
        """Test search operation."""
        arr = DynamicArray.from_list([1, 2, 3, 4, 5])
        self.assertEqual(arr.search(3), 2)
        self.assertEqual(arr.search(10), -1)
    
    def test_resize(self):
        """Test automatic resizing."""
        arr = DynamicArray(initial_capacity=2)
        for i in range(100):
            arr.append(i)
        self.assertEqual(len(arr), 100)
        self.assertTrue(arr.capacity >= 100)
    
    def test_negative_indexing(self):
        """Test negative index access."""
        arr = DynamicArray.from_list([1, 2, 3, 4, 5])
        self.assertEqual(arr[-1], 5)
        self.assertEqual(arr[-2], 4)
    
    def test_out_of_bounds(self):
        """Test index out of bounds."""
        arr = DynamicArray.from_list([1, 2, 3])
        with self.assertRaises(IndexError):
            _ = arr[10]


class TestMatrix(unittest.TestCase):
    """Tests for Matrix."""
    
    def test_creation(self):
        """Test matrix creation."""
        m = Matrix(3, 4)
        self.assertEqual(m.rows, 3)
        self.assertEqual(m.cols, 4)
        self.assertEqual(m.shape, (3, 4))
    
    def test_get_set(self):
        """Test element access and modification."""
        m = Matrix(3, 3)
        m[1, 1] = 5
        self.assertEqual(m[1, 1], 5)
        self.assertEqual(m.get(1, 1), 5)
    
    def test_row_col_access(self):
        """Test row and column access."""
        m = Matrix.from_list([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(m.get_row(1), [4, 5, 6])
        self.assertEqual(m.get_col(1), [2, 5, 8])
    
    def test_transpose(self):
        """Test matrix transpose."""
        m = Matrix.from_list([[1, 2, 3], [4, 5, 6]])
        t = m.transpose()
        self.assertEqual(t.shape, (3, 2))
        self.assertEqual(t[0, 1], 4)
    
    def test_addition(self):
        """Test matrix addition."""
        m1 = Matrix.from_list([[1, 2], [3, 4]])
        m2 = Matrix.from_list([[5, 6], [7, 8]])
        result = m1.add(m2)
        self.assertEqual(result.to_list(), [[6, 8], [10, 12]])
    
    def test_multiplication(self):
        """Test matrix multiplication."""
        m1 = Matrix.from_list([[1, 2], [3, 4]])
        m2 = Matrix.from_list([[5, 6], [7, 8]])
        result = m1.multiply(m2)
        self.assertEqual(result.to_list(), [[19, 22], [43, 50]])
    
    def test_identity(self):
        """Test identity matrix."""
        m = Matrix.identity(3)
        self.assertEqual(m[0, 0], 1)
        self.assertEqual(m[1, 1], 1)
        self.assertEqual(m[0, 1], 0)


class TestStack(unittest.TestCase):
    """Tests for Stack."""
    
    def test_push_pop(self):
        """Test push and pop operations."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 1)
    
    def test_peek(self):
        """Test peek operation."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        self.assertEqual(stack.peek(), 2)
        self.assertEqual(len(stack), 2)  # Peek shouldn't remove
    
    def test_is_empty(self):
        """Test is_empty method."""
        stack = Stack()
        self.assertTrue(stack.is_empty())
        stack.push(1)
        self.assertFalse(stack.is_empty())
    
    def test_pop_empty(self):
        """Test pop from empty stack."""
        stack = Stack()
        with self.assertRaises(IndexError):
            stack.pop()
    
    def test_lifo_order(self):
        """Test LIFO ordering."""
        stack = Stack.from_list([1, 2, 3, 4, 5])
        result = []
        while not stack.is_empty():
            result.append(stack.pop())
        self.assertEqual(result, [5, 4, 3, 2, 1])


class TestQueue(unittest.TestCase):
    """Tests for Queue."""
    
    def test_enqueue_dequeue(self):
        """Test enqueue and dequeue operations."""
        queue = Queue()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.dequeue(), 3)
    
    def test_front(self):
        """Test front operation."""
        queue = Queue()
        queue.enqueue(1)
        queue.enqueue(2)
        self.assertEqual(queue.front(), 1)
        self.assertEqual(len(queue), 2)  # Front shouldn't remove
    
    def test_is_empty(self):
        """Test is_empty method."""
        queue = Queue()
        self.assertTrue(queue.is_empty())
        queue.enqueue(1)
        self.assertFalse(queue.is_empty())
    
    def test_dequeue_empty(self):
        """Test dequeue from empty queue."""
        queue = Queue()
        with self.assertRaises(IndexError):
            queue.dequeue()
    
    def test_fifo_order(self):
        """Test FIFO ordering."""
        queue = Queue.from_list([1, 2, 3, 4, 5])
        result = []
        while not queue.is_empty():
            result.append(queue.dequeue())
        self.assertEqual(result, [1, 2, 3, 4, 5])
    
    def test_circular_behavior(self):
        """Test circular array behavior."""
        queue = Queue(capacity=4)
        # Fill and empty multiple times to test wrapping
        for _ in range(3):
            for i in range(3):
                queue.enqueue(i)
            for i in range(3):
                self.assertEqual(queue.dequeue(), i)


class TestLinkedList(unittest.TestCase):
    """Tests for LinkedList."""
    
    def test_insert_front(self):
        """Test insert at front."""
        ll = LinkedList()
        ll.insert_front(3)
        ll.insert_front(2)
        ll.insert_front(1)
        self.assertEqual(ll.to_list(), [1, 2, 3])
    
    def test_insert_end(self):
        """Test insert at end."""
        ll = LinkedList()
        ll.insert_end(1)
        ll.insert_end(2)
        ll.insert_end(3)
        self.assertEqual(ll.to_list(), [1, 2, 3])
    
    def test_delete(self):
        """Test delete operation."""
        ll = LinkedList.from_list([1, 2, 3, 4, 5])
        self.assertTrue(ll.delete(3))
        self.assertEqual(ll.to_list(), [1, 2, 4, 5])
        self.assertFalse(ll.delete(10))
    
    def test_search(self):
        """Test search operation."""
        ll = LinkedList.from_list([1, 2, 3, 4, 5])
        self.assertTrue(ll.search(3))
        self.assertFalse(ll.search(10))
    
    def test_reverse(self):
        """Test reverse operation."""
        ll = LinkedList.from_list([1, 2, 3, 4, 5])
        ll.reverse()
        self.assertEqual(ll.to_list(), [5, 4, 3, 2, 1])
    
    def test_get_middle(self):
        """Test get middle element."""
        ll = LinkedList.from_list([1, 2, 3, 4, 5])
        self.assertEqual(ll.get_middle(), 3)
    
    def test_find(self):
        """Test find index."""
        ll = LinkedList.from_list([1, 2, 3, 4, 5])
        self.assertEqual(ll.find(3), 2)
        self.assertEqual(ll.find(10), -1)
    
    def test_delete_front(self):
        """Test delete from front."""
        ll = LinkedList.from_list([1, 2, 3])
        self.assertEqual(ll.delete_front(), 1)
        self.assertEqual(ll.to_list(), [2, 3])


class TestRootedTree(unittest.TestCase):
    """Tests for RootedTree."""
    
    def test_creation(self):
        """Test tree creation."""
        tree = RootedTree(1)
        self.assertEqual(tree.root.data, 1)
        self.assertEqual(len(tree), 1)
    
    def test_insert(self):
        """Test insert operation."""
        tree = RootedTree(1)
        tree.insert(1, 2)
        tree.insert(1, 3)
        tree.insert(2, 4)
        self.assertEqual(len(tree), 4)
    
    def test_find(self):
        """Test find operation."""
        tree = RootedTree(1)
        tree.insert(1, 2)
        tree.insert(1, 3)
        node = tree.find(2)
        self.assertIsNotNone(node)
        self.assertEqual(node.data, 2)
        self.assertIsNone(tree.find(10))
    
    def test_height(self):
        """Test height calculation."""
        tree = RootedTree(1)
        tree.insert(1, 2)
        tree.insert(2, 3)
        tree.insert(3, 4)
        self.assertEqual(tree.height(), 3)
    
    def test_traversals(self):
        """Test tree traversals."""
        tree = RootedTree(1)
        tree.insert(1, 2)
        tree.insert(1, 3)
        tree.insert(2, 4)
        tree.insert(2, 5)
        
        # Pre-order: root, then children
        preorder = tree.traverse_preorder()
        self.assertEqual(preorder[0], 1)
        
        # Level-order: level by level
        levelorder = tree.traverse_levelorder()
        self.assertEqual(levelorder, [1, 2, 3, 4, 5])
    
    def test_leaves(self):
        """Test get leaves."""
        tree = RootedTree(1)
        tree.insert(1, 2)
        tree.insert(1, 3)
        tree.insert(2, 4)
        leaves = tree.get_leaves()
        leaf_data = [n.data for n in leaves]
        self.assertIn(3, leaf_data)
        self.assertIn(4, leaf_data)


if __name__ == '__main__':
    unittest.main()
