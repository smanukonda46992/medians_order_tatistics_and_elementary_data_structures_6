"""
Stack Implementation (LIFO - Last In, First Out)

A stack is a linear data structure that follows the Last-In-First-Out principle.
Elements are added and removed from the same end (the "top").

Real-World Applications:
    1. Function call stack (recursion management)
    2. Undo/Redo operations in editors
    3. Expression evaluation (postfix, infix conversion)
    4. Backtracking algorithms (maze solving, DFS)
    5. Browser history (back button)
    6. Syntax parsing (matching parentheses)

Implementation Choice: Array-Based vs Linked List
    
    Array-Based (this implementation):
        + O(1) push/pop (amortized for dynamic array)
        + Better cache locality
        + Less memory overhead (no pointers)
        - May waste space if capacity >> size
        
    Linked List-Based:
        + No wasted capacity
        + O(1) push/pop (always, not amortized)
        - More memory per element (pointer overhead)
        - Poor cache locality

Time Complexity Analysis:
    push():     O(1) amortized (O(n) worst case during resize)
    pop():      O(1)
    peek():     O(1)
    is_empty(): O(1)
    size():     O(1)
    search():   O(n)

Space Complexity: O(n) where n is the number of elements
"""

from typing import Any, List, Optional


class Stack:
    """
    Array-based stack implementation.
    
    Uses Python list with append/pop for O(1) operations at the end.
    The "top" of the stack is the last element in the list.
    
    Attributes:
        _data: Internal list storing elements
        _max_size: Maximum size limit (None for unlimited)
    """
    
    def __init__(self, max_size: int = None):
        """
        Initialize empty stack.
        
        Args:
            max_size: Maximum number of elements (None for unlimited)
        """
        self._data: List[Any] = []
        self._max_size = max_size
    
    def __len__(self) -> int:
        """Return number of elements. O(1)"""
        return len(self._data)
    
    def __bool__(self) -> bool:
        """Return True if stack has elements. O(1)"""
        return len(self._data) > 0
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Stack({self._data})"
    
    def __str__(self) -> str:
        """Human-readable string showing top element."""
        if self.is_empty():
            return "Stack(empty)"
        return f"Stack(size={len(self)}, top={self.peek()})"
    
    def __contains__(self, value: Any) -> bool:
        """Check if value exists in stack. O(n)"""
        return value in self._data
    
    def is_empty(self) -> bool:
        """
        Check if stack is empty. O(1)
        
        Returns:
            True if stack has no elements
        """
        return len(self._data) == 0
    
    def is_full(self) -> bool:
        """
        Check if stack is full. O(1)
        
        Returns:
            True if stack reached max_size (always False if no max_size)
        """
        if self._max_size is None:
            return False
        return len(self._data) >= self._max_size
    
    def push(self, value: Any) -> bool:
        """
        Add element to top of stack. O(1) amortized.
        
        Stack grows at one end only, making push O(1).
        
        Args:
            value: Element to push
            
        Returns:
            True if successful, False if stack is full
            
        Raises:
            OverflowError: If stack is full (when max_size is set)
        """
        if self.is_full():
            raise OverflowError("Stack is full")
        
        self._data.append(value)
        return True
    
    def pop(self) -> Any:
        """
        Remove and return top element. O(1)
        
        Returns:
            The top element
            
        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        
        return self._data.pop()
    
    def peek(self) -> Any:
        """
        Return top element without removing. O(1)
        
        Also called 'top' in some implementations.
        
        Returns:
            The top element
            
        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        
        return self._data[-1]
    
    def top(self) -> Any:
        """Alias for peek(). O(1)"""
        return self.peek()
    
    def size(self) -> int:
        """Return number of elements. O(1)"""
        return len(self._data)
    
    def clear(self) -> None:
        """Remove all elements. O(1)"""
        self._data = []
    
    def search(self, value: Any) -> int:
        """
        Find distance from top to element. O(n)
        
        Args:
            value: Element to search for
            
        Returns:
            1-based distance from top (1 = top element), or -1 if not found
            
        Note:
            This follows Java's Stack.search() convention where:
            - Top element has distance 1
            - Element below top has distance 2
            - etc.
        """
        for i in range(len(self._data) - 1, -1, -1):
            if self._data[i] == value:
                return len(self._data) - i
        return -1
    
    def to_list(self) -> List[Any]:
        """
        Convert to list (bottom to top). O(n)
        
        Returns:
            List copy with bottom element first, top element last
        """
        return self._data.copy()
    
    @classmethod
    def from_list(cls, items: List[Any], max_size: int = None) -> 'Stack':
        """
        Create stack from list. O(n)
        
        First element of list becomes bottom of stack.
        Last element of list becomes top of stack.
        
        Args:
            items: List of items
            max_size: Maximum size limit
            
        Returns:
            New Stack instance
        """
        stack = cls(max_size)
        for item in items:
            stack.push(item)
        return stack


class MinStack(Stack):
    """
    Stack that supports O(1) minimum element retrieval.
    
    Uses auxiliary stack to track minimums.
    
    Time Complexity:
        push(): O(1)
        pop(): O(1)
        get_min(): O(1)
        
    Space Complexity: O(n) auxiliary for min tracking
    """
    
    def __init__(self, max_size: int = None):
        """Initialize MinStack with auxiliary min stack."""
        super().__init__(max_size)
        self._min_stack: List[Any] = []
    
    def push(self, value: Any) -> bool:
        """Push and update minimum tracking. O(1)"""
        if self.is_full():
            raise OverflowError("Stack is full")
        
        self._data.append(value)
        
        # Update min stack
        if not self._min_stack or value <= self._min_stack[-1]:
            self._min_stack.append(value)
        
        return True
    
    def pop(self) -> Any:
        """Pop and update minimum tracking. O(1)"""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        
        value = self._data.pop()
        
        # Update min stack
        if value == self._min_stack[-1]:
            self._min_stack.pop()
        
        return value
    
    def get_min(self) -> Any:
        """
        Return minimum element in stack. O(1)
        
        Returns:
            Minimum element
            
        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Min of empty stack")
        
        return self._min_stack[-1]
    
    def clear(self) -> None:
        """Clear both stacks. O(1)"""
        super().clear()
        self._min_stack = []
