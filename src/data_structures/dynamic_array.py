"""
Dynamic Array Implementation

A dynamic array (also known as a growable array, resizable array, or vector)
is an array that can resize itself when elements are added or removed.

Key Features:
    - Random access in O(1) time
    - Amortized O(1) append operation
    - Automatic resizing when capacity is exceeded

Implementation Details:
    - Uses a Python list internally, but demonstrates the concepts
    - Doubles capacity when full (growth factor = 2)
    - Shrinks when load factor drops below 25% (optional optimization)

Time Complexity Analysis:
    Access (get/set by index): O(1)
        - Direct memory address calculation
        
    Append: O(1) amortized
        - Without resize: O(1)
        - With resize: O(n) but happens infrequently
        - Amortized analysis: Total cost for n appends = O(n), so O(1) per operation
        
    Insert at index i: O(n)
        - Must shift all elements from index i to end
        - Average case: O(n/2) = O(n)
        
    Delete at index i: O(n)
        - Must shift all elements after index i
        - Average case: O(n/2) = O(n)
        
    Search: O(n)
        - Linear search through array

Space Complexity: O(n) where n is the number of elements
    Note: Actual allocated space may be up to 2n due to capacity buffer
"""

from typing import Any, List, Optional, Iterator


class DynamicArray:
    """
    A dynamic array implementation with automatic resizing.
    
    This class demonstrates the core concepts of dynamic arrays:
    - Capacity management (doubling strategy)
    - Amortized O(1) append
    - O(n) insert/delete with element shifting
    
    Attributes:
        _data: Internal list storing elements
        _size: Number of elements currently stored
        _capacity: Current allocated capacity
    """
    
    INITIAL_CAPACITY = 4
    GROWTH_FACTOR = 2
    SHRINK_THRESHOLD = 0.25  # Shrink when size < capacity * threshold
    
    def __init__(self, initial_capacity: int = None):
        """
        Initialize empty dynamic array.
        
        Args:
            initial_capacity: Initial capacity (default: 4)
        """
        self._capacity = initial_capacity or self.INITIAL_CAPACITY
        self._data: List[Any] = [None] * self._capacity
        self._size = 0
    
    def __len__(self) -> int:
        """Return number of elements. O(1)"""
        return self._size
    
    def __bool__(self) -> bool:
        """Return True if array has elements. O(1)"""
        return self._size > 0
    
    def __repr__(self) -> str:
        """String representation."""
        elements = [self._data[i] for i in range(self._size)]
        return f"DynamicArray({elements})"
    
    def __str__(self) -> str:
        """Human-readable string."""
        elements = [self._data[i] for i in range(self._size)]
        return str(elements)
    
    def __iter__(self) -> Iterator[Any]:
        """Iterate over elements. O(n) total."""
        for i in range(self._size):
            yield self._data[i]
    
    def __getitem__(self, index: int) -> Any:
        """
        Get element at index. O(1)
        
        Args:
            index: Index to access (supports negative indexing)
            
        Returns:
            Element at index
            
        Raises:
            IndexError: If index out of bounds
        """
        if index < 0:
            index = self._size + index
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")
        return self._data[index]
    
    def __setitem__(self, index: int, value: Any) -> None:
        """
        Set element at index. O(1)
        
        Args:
            index: Index to set
            value: Value to store
            
        Raises:
            IndexError: If index out of bounds
        """
        if index < 0:
            index = self._size + index
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")
        self._data[index] = value
    
    def __contains__(self, value: Any) -> bool:
        """Check if value exists. O(n)"""
        return self.search(value) != -1
    
    @property
    def capacity(self) -> int:
        """Current capacity of the array."""
        return self._capacity
    
    @property
    def load_factor(self) -> float:
        """Ratio of size to capacity."""
        return self._size / self._capacity if self._capacity > 0 else 0
    
    def is_empty(self) -> bool:
        """Check if array is empty. O(1)"""
        return self._size == 0
    
    def _resize(self, new_capacity: int) -> None:
        """
        Resize internal array to new capacity.
        
        This is an O(n) operation, but occurs infrequently enough
        that amortized cost per operation is O(1).
        
        Args:
            new_capacity: New capacity (must be >= current size)
        """
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity
    
    def append(self, value: Any) -> None:
        """
        Add element to end of array. O(1) amortized.
        
        Amortized Analysis:
            Using the accounting method:
            - Charge 3 units per append: 1 for the operation, 2 for future copying
            - When array doubles, we have n/2 elements that paid 2 extra
            - This covers the n copies needed during resize
            - Total cost for n appends: 3n = O(n), so O(1) per operation
        
        Args:
            value: Value to append
        """
        # Check if resize needed
        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)
        
        self._data[self._size] = value
        self._size += 1
    
    def insert(self, index: int, value: Any) -> None:
        """
        Insert element at index. O(n)
        
        Must shift all elements from index to end right by one position.
        
        Args:
            index: Position to insert at (0 to size inclusive)
            value: Value to insert
            
        Raises:
            IndexError: If index < 0 or index > size
        """
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of bounds for insertion")
        
        # Resize if needed
        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)
        
        # Shift elements right
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        
        self._data[index] = value
        self._size += 1
    
    def delete(self, index: int) -> Any:
        """
        Remove and return element at index. O(n)
        
        Must shift all elements after index left by one position.
        
        Args:
            index: Index to delete
            
        Returns:
            Deleted element
            
        Raises:
            IndexError: If index out of bounds
        """
        if index < 0:
            index = self._size + index
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")
        
        value = self._data[index]
        
        # Shift elements left
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        
        self._data[self._size - 1] = None
        self._size -= 1
        
        # Optionally shrink if too sparse
        if self._size > 0 and self._size < self._capacity * self.SHRINK_THRESHOLD:
            self._resize(max(self.INITIAL_CAPACITY, self._capacity // 2))
        
        return value
    
    def remove(self, value: Any) -> bool:
        """
        Remove first occurrence of value. O(n)
        
        Args:
            value: Value to remove
            
        Returns:
            True if removed, False if not found
        """
        index = self.search(value)
        if index == -1:
            return False
        self.delete(index)
        return True
    
    def search(self, value: Any) -> int:
        """
        Find index of value using linear search. O(n)
        
        Args:
            value: Value to find
            
        Returns:
            Index of first occurrence, or -1 if not found
        """
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1
    
    def get(self, index: int, default: Any = None) -> Any:
        """
        Get element at index with default value. O(1)
        
        Args:
            index: Index to access
            default: Value to return if index out of bounds
            
        Returns:
            Element at index or default
        """
        try:
            return self[index]
        except IndexError:
            return default
    
    def clear(self) -> None:
        """Remove all elements. O(1)"""
        self._data = [None] * self.INITIAL_CAPACITY
        self._size = 0
        self._capacity = self.INITIAL_CAPACITY
    
    def to_list(self) -> List[Any]:
        """Convert to standard Python list. O(n)"""
        return [self._data[i] for i in range(self._size)]
    
    @classmethod
    def from_list(cls, items: List[Any]) -> 'DynamicArray':
        """Create DynamicArray from list. O(n)"""
        arr = cls(len(items) or cls.INITIAL_CAPACITY)
        for item in items:
            arr.append(item)
        return arr
