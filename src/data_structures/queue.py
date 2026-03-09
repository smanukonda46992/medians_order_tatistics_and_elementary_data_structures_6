"""
Queue Implementation (FIFO - First In, First Out)

A queue is a linear data structure that follows the First-In-First-Out principle.
Elements are added at the rear (enqueue) and removed from the front (dequeue).

Real-World Applications:
    1. Task scheduling (CPU, print queue)
    2. Breadth-first search (BFS)
    3. Message queues in distributed systems
    4. Buffer management (keyboard buffer, network packets)
    5. Customer service systems (first come, first served)
    6. Web server request handling

Implementation Choice: Array-Based (Circular) vs Linked List
    
    Array-Based (Simple):
        + Good cache locality
        - O(n) dequeue (must shift elements)
        
    Array-Based Circular (this implementation):
        + O(1) enqueue and dequeue
        + Good cache locality
        + No element shifting needed
        - Fixed capacity (or needs resize)
        
    Linked List-Based:
        + O(1) enqueue and dequeue
        + Dynamic size
        - Poor cache locality
        - Pointer overhead

Time Complexity Analysis (Circular Array):
    enqueue():  O(1) amortized
    dequeue():  O(1)
    front():    O(1)
    rear():     O(1)
    is_empty(): O(1)
    is_full():  O(1)

Space Complexity: O(n) where n is the capacity
"""

from typing import Any, List, Optional


class Queue:
    """
    Circular array-based queue implementation.
    
    Uses two pointers (front, rear) to track positions in a circular array.
    This allows O(1) operations without element shifting.
    
    Circular Array Concept:
        - Array indices wrap around: (index + 1) % capacity
        - Front pointer: position of first element
        - Rear pointer: position where next element will be inserted
        
    Attributes:
        _data: Internal circular array
        _front: Index of front element
        _rear: Index of next insertion position
        _size: Current number of elements
        _capacity: Maximum capacity
    """
    
    INITIAL_CAPACITY = 8
    GROWTH_FACTOR = 2
    
    def __init__(self, capacity: int = None):
        """
        Initialize empty queue.
        
        Args:
            capacity: Initial capacity (default: 8)
        """
        self._capacity = capacity or self.INITIAL_CAPACITY
        self._data: List[Any] = [None] * self._capacity
        self._front = 0
        self._rear = 0
        self._size = 0
    
    def __len__(self) -> int:
        """Return number of elements. O(1)"""
        return self._size
    
    def __bool__(self) -> bool:
        """Return True if queue has elements. O(1)"""
        return self._size > 0
    
    def __repr__(self) -> str:
        """String representation."""
        elements = self.to_list()
        return f"Queue({elements})"
    
    def __str__(self) -> str:
        """Human-readable string."""
        if self.is_empty():
            return "Queue(empty)"
        return f"Queue(size={self._size}, front={self.front()})"
    
    def __contains__(self, value: Any) -> bool:
        """Check if value exists in queue. O(n)"""
        for item in self:
            if item == value:
                return True
        return False
    
    def __iter__(self):
        """Iterate over elements from front to rear. O(n)"""
        idx = self._front
        for _ in range(self._size):
            yield self._data[idx]
            idx = (idx + 1) % self._capacity
    
    def is_empty(self) -> bool:
        """
        Check if queue is empty. O(1)
        
        Returns:
            True if queue has no elements
        """
        return self._size == 0
    
    def is_full(self) -> bool:
        """
        Check if queue is at capacity. O(1)
        
        Returns:
            True if queue is full (before potential resize)
        """
        return self._size == self._capacity
    
    def _resize(self, new_capacity: int) -> None:
        """
        Resize internal array. O(n)
        
        Must linearize the circular array during resize.
        
        Args:
            new_capacity: New capacity
        """
        new_data = [None] * new_capacity
        
        # Copy elements in order from front to rear
        idx = self._front
        for i in range(self._size):
            new_data[i] = self._data[idx]
            idx = (idx + 1) % self._capacity
        
        self._data = new_data
        self._capacity = new_capacity
        self._front = 0
        self._rear = self._size
    
    def enqueue(self, value: Any) -> None:
        """
        Add element to rear of queue. O(1) amortized.
        
        If queue is full, doubles capacity before insertion.
        
        Args:
            value: Element to add
        """
        if self.is_full():
            self._resize(self._capacity * self.GROWTH_FACTOR)
        
        self._data[self._rear] = value
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1
    
    def dequeue(self) -> Any:
        """
        Remove and return front element. O(1)
        
        Returns:
            Front element
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        
        value = self._data[self._front]
        self._data[self._front] = None  # Help garbage collection
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        
        return value
    
    def front(self) -> Any:
        """
        Return front element without removing. O(1)
        
        Also called 'peek' in some implementations.
        
        Returns:
            Front element
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Front of empty queue")
        
        return self._data[self._front]
    
    def peek(self) -> Any:
        """Alias for front(). O(1)"""
        return self.front()
    
    def rear_element(self) -> Any:
        """
        Return rear element without removing. O(1)
        
        Returns:
            Most recently added element
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Rear of empty queue")
        
        rear_idx = (self._rear - 1 + self._capacity) % self._capacity
        return self._data[rear_idx]
    
    def size(self) -> int:
        """Return number of elements. O(1)"""
        return self._size
    
    def clear(self) -> None:
        """Remove all elements. O(1)"""
        self._data = [None] * self.INITIAL_CAPACITY
        self._capacity = self.INITIAL_CAPACITY
        self._front = 0
        self._rear = 0
        self._size = 0
    
    def to_list(self) -> List[Any]:
        """
        Convert to list (front to rear). O(n)
        
        Returns:
            List with front element first
        """
        return list(self)
    
    @classmethod
    def from_list(cls, items: List[Any]) -> 'Queue':
        """
        Create queue from list. O(n)
        
        First element of list becomes front of queue.
        
        Args:
            items: List of items
            
        Returns:
            New Queue instance
        """
        queue = cls(len(items) or cls.INITIAL_CAPACITY)
        for item in items:
            queue.enqueue(item)
        return queue


class Deque:
    """
    Double-ended queue (deque) implementation.
    
    Supports insertion and deletion at both ends in O(1) time.
    
    Applications:
        - Sliding window algorithms
        - Palindrome checking
        - Work stealing in parallel computing
    
    Time Complexity:
        All operations: O(1) amortized
    """
    
    INITIAL_CAPACITY = 8
    GROWTH_FACTOR = 2
    
    def __init__(self, capacity: int = None):
        """Initialize empty deque."""
        self._capacity = capacity or self.INITIAL_CAPACITY
        self._data: List[Any] = [None] * self._capacity
        self._front = 0
        self._rear = 0
        self._size = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __bool__(self) -> bool:
        return self._size > 0
    
    def __repr__(self) -> str:
        return f"Deque({self.to_list()})"
    
    def is_empty(self) -> bool:
        """Check if deque is empty."""
        return self._size == 0
    
    def _resize(self, new_capacity: int) -> None:
        """Resize internal array."""
        new_data = [None] * new_capacity
        idx = self._front
        for i in range(self._size):
            new_data[i] = self._data[idx]
            idx = (idx + 1) % self._capacity
        self._data = new_data
        self._capacity = new_capacity
        self._front = 0
        self._rear = self._size
    
    def push_front(self, value: Any) -> None:
        """Add element to front. O(1) amortized."""
        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)
        
        self._front = (self._front - 1 + self._capacity) % self._capacity
        self._data[self._front] = value
        self._size += 1
    
    def push_back(self, value: Any) -> None:
        """Add element to back. O(1) amortized."""
        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)
        
        self._data[self._rear] = value
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1
    
    def pop_front(self) -> Any:
        """Remove and return front element. O(1)"""
        if self.is_empty():
            raise IndexError("Pop from empty deque")
        
        value = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return value
    
    def pop_back(self) -> Any:
        """Remove and return back element. O(1)"""
        if self.is_empty():
            raise IndexError("Pop from empty deque")
        
        self._rear = (self._rear - 1 + self._capacity) % self._capacity
        value = self._data[self._rear]
        self._data[self._rear] = None
        self._size -= 1
        return value
    
    def front(self) -> Any:
        """Return front element. O(1)"""
        if self.is_empty():
            raise IndexError("Front of empty deque")
        return self._data[self._front]
    
    def back(self) -> Any:
        """Return back element. O(1)"""
        if self.is_empty():
            raise IndexError("Back of empty deque")
        rear_idx = (self._rear - 1 + self._capacity) % self._capacity
        return self._data[rear_idx]
    
    def to_list(self) -> List[Any]:
        """Convert to list."""
        result = []
        idx = self._front
        for _ in range(self._size):
            result.append(self._data[idx])
            idx = (idx + 1) % self._capacity
        return result
