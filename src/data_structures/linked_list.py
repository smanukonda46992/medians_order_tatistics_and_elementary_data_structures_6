"""
Singly Linked List Implementation

A linked list is a linear data structure where elements are stored in nodes,
with each node containing data and a reference (pointer) to the next node.

Key Characteristics:
    - Non-contiguous memory allocation
    - Dynamic size (no fixed capacity)
    - Efficient insertion/deletion at known positions

Comparison with Arrays:
    
    Operation           | Array   | Linked List
    --------------------|---------|-------------
    Access by index     | O(1)    | O(n)
    Insert at beginning | O(n)    | O(1)
    Insert at end       | O(1)*   | O(n)**
    Insert at middle    | O(n)    | O(1)***
    Delete at beginning | O(n)    | O(1)
    Delete at middle    | O(n)    | O(1)***
    Memory overhead     | Low     | High (pointers)
    Cache performance   | Good    | Poor
    
    * Amortized for dynamic array
    ** O(1) if we maintain tail pointer
    *** After finding the position (which is O(n))

Real-World Applications:
    1. Implementation of other data structures (stack, queue, hash table chains)
    2. Memory management (free list in allocators)
    3. Polynomial representation and manipulation
    4. Music playlist (next song)
    5. Undo functionality (singly: undo only)
    6. Symbol tables in compilers

Time Complexity Analysis:
    insert_front():   O(1)
    insert_end():     O(n) - O(1) with tail pointer
    insert_after():   O(n) to find node, O(1) to insert
    delete():         O(n)
    search():         O(n)
    traverse():       O(n)
    reverse():        O(n)
    get_length():     O(1) with size tracking

Space Complexity: O(n) + pointer overhead per node
"""

from typing import Any, Optional, Iterator, List


class Node:
    """
    Node for singly linked list.
    
    Each node contains:
        - data: The stored value
        - next: Reference to the next node (or None)
    
    Memory Layout:
        +------+------+
        | data | next |---> next Node or None
        +------+------+
    """
    
    __slots__ = ['data', 'next']  # Memory optimization
    
    def __init__(self, data: Any, next_node: 'Node' = None):
        """
        Initialize node with data.
        
        Args:
            data: Value to store
            next_node: Reference to next node
        """
        self.data = data
        self.next = next_node
    
    def __repr__(self) -> str:
        return f"Node({self.data})"
    
    def __str__(self) -> str:
        return str(self.data)


class LinkedList:
    """
    Singly linked list implementation.
    
    Maintains:
        - head: Reference to first node
        - tail: Reference to last node (for O(1) append)
        - size: Number of elements
    
    Visual representation:
        head                                    tail
          |                                       |
          v                                       v
        +---+    +---+    +---+    +---+    +---+
        | 1 |--->| 2 |--->| 3 |--->| 4 |--->| 5 |---> None
        +---+    +---+    +---+    +---+    +---+
    """
    
    def __init__(self):
        """Initialize empty linked list."""
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._size: int = 0
    
    def __len__(self) -> int:
        """Return number of elements. O(1)"""
        return self._size
    
    def __bool__(self) -> bool:
        """Return True if list has elements. O(1)"""
        return self._size > 0
    
    def __repr__(self) -> str:
        """String representation."""
        elements = self.to_list()
        return f"LinkedList({elements})"
    
    def __str__(self) -> str:
        """Human-readable string."""
        if self.is_empty():
            return "LinkedList(empty)"
        elements = " -> ".join(str(x) for x in self)
        return elements + " -> None"
    
    def __iter__(self) -> Iterator[Any]:
        """Iterate over elements. O(n)"""
        current = self._head
        while current:
            yield current.data
            current = current.next
    
    def __contains__(self, value: Any) -> bool:
        """Check if value exists. O(n)"""
        return self.search(value)
    
    def __getitem__(self, index: int) -> Any:
        """
        Get element at index. O(n)
        
        Note: This is O(n) unlike arrays which are O(1).
        Linked lists trade random access for efficient insertion.
        """
        node = self._get_node(index)
        return node.data
    
    def _get_node(self, index: int) -> Node:
        """
        Get node at index. O(n)
        
        Args:
            index: Index of node (supports negative indexing)
            
        Returns:
            Node at index
            
        Raises:
            IndexError: If index out of bounds
        """
        if index < 0:
            index = self._size + index
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds for size {self._size}")
        
        current = self._head
        for _ in range(index):
            current = current.next
        return current
    
    def is_empty(self) -> bool:
        """Check if list is empty. O(1)"""
        return self._head is None
    
    @property
    def head(self) -> Optional[Node]:
        """Get head node."""
        return self._head
    
    @property
    def tail(self) -> Optional[Node]:
        """Get tail node."""
        return self._tail
    
    def insert_front(self, data: Any) -> None:
        """
        Insert at beginning of list. O(1)
        
        This is the primary advantage of linked lists over arrays.
        No shifting required - just update pointers.
        
        Before: head -> [A] -> [B] -> None
        After:  head -> [NEW] -> [A] -> [B] -> None
        
        Args:
            data: Value to insert
        """
        new_node = Node(data, self._head)
        self._head = new_node
        
        if self._tail is None:
            self._tail = new_node
        
        self._size += 1
    
    def insert_end(self, data: Any) -> None:
        """
        Insert at end of list. O(1) with tail pointer.
        
        Without tail pointer this would be O(n).
        
        Before: ... -> [Z] -> None, tail -> [Z]
        After:  ... -> [Z] -> [NEW] -> None, tail -> [NEW]
        
        Args:
            data: Value to insert
        """
        new_node = Node(data)
        
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        
        self._size += 1
    
    def insert_after(self, target: Any, data: Any) -> bool:
        """
        Insert after first occurrence of target. O(n)
        
        Must traverse to find target node first.
        
        Args:
            target: Value to find
            data: Value to insert
            
        Returns:
            True if inserted, False if target not found
        """
        current = self._head
        while current:
            if current.data == target:
                new_node = Node(data, current.next)
                current.next = new_node
                
                if current == self._tail:
                    self._tail = new_node
                
                self._size += 1
                return True
            current = current.next
        
        return False
    
    def insert_at(self, index: int, data: Any) -> None:
        """
        Insert at specific index. O(n)
        
        Args:
            index: Position to insert at
            data: Value to insert
            
        Raises:
            IndexError: If index out of bounds
        """
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of bounds")
        
        if index == 0:
            self.insert_front(data)
            return
        
        if index == self._size:
            self.insert_end(data)
            return
        
        prev = self._get_node(index - 1)
        new_node = Node(data, prev.next)
        prev.next = new_node
        self._size += 1
    
    def delete(self, data: Any) -> bool:
        """
        Delete first occurrence of data. O(n)
        
        Must traverse to find the node and its predecessor.
        
        Args:
            data: Value to delete
            
        Returns:
            True if deleted, False if not found
        """
        if self.is_empty():
            return False
        
        # Special case: delete head
        if self._head.data == data:
            self._head = self._head.next
            self._size -= 1
            
            if self._head is None:
                self._tail = None
            
            return True
        
        # Find predecessor of node to delete
        current = self._head
        while current.next:
            if current.next.data == data:
                # Delete current.next
                if current.next == self._tail:
                    self._tail = current
                
                current.next = current.next.next
                self._size -= 1
                return True
            
            current = current.next
        
        return False
    
    def delete_front(self) -> Any:
        """
        Delete and return first element. O(1)
        
        Returns:
            Data from deleted node
            
        Raises:
            IndexError: If list is empty
        """
        if self.is_empty():
            raise IndexError("Delete from empty list")
        
        data = self._head.data
        self._head = self._head.next
        self._size -= 1
        
        if self._head is None:
            self._tail = None
        
        return data
    
    def delete_end(self) -> Any:
        """
        Delete and return last element. O(n)
        
        Must traverse to find predecessor of tail.
        (Would be O(1) with doubly linked list)
        
        Returns:
            Data from deleted node
            
        Raises:
            IndexError: If list is empty
        """
        if self.is_empty():
            raise IndexError("Delete from empty list")
        
        if self._size == 1:
            data = self._head.data
            self._head = None
            self._tail = None
            self._size = 0
            return data
        
        # Find predecessor of tail
        current = self._head
        while current.next != self._tail:
            current = current.next
        
        data = self._tail.data
        current.next = None
        self._tail = current
        self._size -= 1
        
        return data
    
    def delete_at(self, index: int) -> Any:
        """
        Delete at specific index. O(n)
        
        Args:
            index: Position to delete
            
        Returns:
            Data from deleted node
            
        Raises:
            IndexError: If index out of bounds
        """
        if index < 0:
            index = self._size + index
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds")
        
        if index == 0:
            return self.delete_front()
        
        if index == self._size - 1:
            return self.delete_end()
        
        prev = self._get_node(index - 1)
        data = prev.next.data
        prev.next = prev.next.next
        self._size -= 1
        
        return data
    
    def search(self, data: Any) -> bool:
        """
        Check if data exists in list. O(n)
        
        Args:
            data: Value to search for
            
        Returns:
            True if found, False otherwise
        """
        current = self._head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def find(self, data: Any) -> int:
        """
        Find index of first occurrence. O(n)
        
        Args:
            data: Value to find
            
        Returns:
            Index of element, or -1 if not found
        """
        index = 0
        current = self._head
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1
    
    def display(self) -> None:
        """Print all elements. O(n)"""
        print(str(self))
    
    def traverse(self) -> List[Any]:
        """
        Return all elements as list. O(n)
        
        Returns:
            List of all elements
        """
        return list(self)
    
    def reverse(self) -> None:
        """
        Reverse list in-place. O(n)
        
        Uses three-pointer technique:
        - prev: previously processed node
        - curr: current node
        - next: next node to process
        
        Before: head -> [1] -> [2] -> [3] -> None
        After:  head -> [3] -> [2] -> [1] -> None
        """
        self._tail = self._head
        
        prev = None
        curr = self._head
        
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        
        self._head = prev
    
    def get_middle(self) -> Optional[Any]:
        """
        Get middle element using slow/fast pointer technique. O(n)
        
        Uses two pointers:
        - slow moves one step at a time
        - fast moves two steps at a time
        When fast reaches end, slow is at middle.
        
        Returns:
            Middle element data, or None if empty
        """
        if self.is_empty():
            return None
        
        slow = self._head
        fast = self._head
        
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        
        return slow.data
    
    def has_cycle(self) -> bool:
        """
        Detect if list has a cycle (Floyd's algorithm). O(n)
        
        Uses slow/fast pointer technique.
        If there's a cycle, fast will eventually catch up to slow.
        
        Returns:
            True if cycle exists
        """
        if self.is_empty():
            return False
        
        slow = self._head
        fast = self._head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                return True
        
        return False
    
    def clear(self) -> None:
        """Remove all elements. O(1)"""
        self._head = None
        self._tail = None
        self._size = 0
    
    def to_list(self) -> List[Any]:
        """Convert to Python list. O(n)"""
        return list(self)
    
    @classmethod
    def from_list(cls, items: List[Any]) -> 'LinkedList':
        """Create LinkedList from Python list. O(n)"""
        ll = cls()
        for item in items:
            ll.insert_end(item)
        return ll
