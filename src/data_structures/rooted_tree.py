"""
Rooted Tree Implementation using Linked Representation

A rooted tree is a hierarchical data structure with:
    - One special node called the "root"
    - Each node (except root) has exactly one parent
    - Each node can have zero or more children

Linked Representation:
    Each node stores:
    - data: The node's value
    - parent: Reference to parent node (optional)
    - children: List of child nodes
    
    Alternative representations:
    - Left-child, right-sibling (LCRS): Memory efficient for many children
    - Array representation: For complete/nearly complete trees (heaps)

Real-World Applications:
    1. File system directories
    2. Organization hierarchies
    3. HTML/XML DOM trees
    4. Abstract Syntax Trees (AST) in compilers
    5. Decision trees in machine learning
    6. Game trees (minimax)
    7. Trie (prefix tree) for string matching

Time Complexity Analysis:
    insert_child():   O(1)
    find():           O(n) - must traverse tree
    height():         O(n) - visit all nodes
    depth():          O(h) where h is height
    traverse():       O(n) - visit all nodes
    
Space Complexity: O(n) for n nodes + pointer overhead
"""

from typing import Any, Optional, List, Iterator, Callable
from collections import deque


class TreeNode:
    """
    Node for rooted tree.
    
    Each node contains:
        - data: The stored value
        - parent: Reference to parent (None for root)
        - children: List of child nodes
        
    Visual representation:
              [parent]
                  |
              [  data  ]
             /    |    \
        [c1]   [c2]   [c3]
    """
    
    def __init__(self, data: Any, parent: 'TreeNode' = None):
        """
        Initialize tree node.
        
        Args:
            data: Value to store
            parent: Parent node reference
        """
        self.data = data
        self.parent = parent
        self.children: List['TreeNode'] = []
    
    def __repr__(self) -> str:
        return f"TreeNode({self.data})"
    
    def __str__(self) -> str:
        return str(self.data)
    
    def is_root(self) -> bool:
        """Check if this is the root node."""
        return self.parent is None
    
    def is_leaf(self) -> bool:
        """Check if this is a leaf node (no children)."""
        return len(self.children) == 0
    
    def degree(self) -> int:
        """Return number of children."""
        return len(self.children)
    
    def add_child(self, data: Any) -> 'TreeNode':
        """
        Add child node with given data. O(1)
        
        Args:
            data: Value for new child
            
        Returns:
            The new child node
        """
        child = TreeNode(data, parent=self)
        self.children.append(child)
        return child
    
    def remove_child(self, child: 'TreeNode') -> bool:
        """
        Remove child node. O(k) where k is number of children.
        
        Args:
            child: Child node to remove
            
        Returns:
            True if removed, False if not found
        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            return True
        return False
    
    def siblings(self) -> List['TreeNode']:
        """
        Get sibling nodes. O(k) where k is parent's children.
        
        Returns:
            List of sibling nodes (excluding self)
        """
        if self.parent is None:
            return []
        return [c for c in self.parent.children if c != self]
    
    def ancestors(self) -> List['TreeNode']:
        """
        Get all ancestors from parent to root. O(h)
        
        Returns:
            List of ancestors [parent, grandparent, ..., root]
        """
        result = []
        current = self.parent
        while current:
            result.append(current)
            current = current.parent
        return result
    
    def depth(self) -> int:
        """
        Get depth (distance from root). O(h)
        
        Root has depth 0.
        
        Returns:
            Depth of this node
        """
        d = 0
        current = self
        while current.parent:
            d += 1
            current = current.parent
        return d


class RootedTree:
    """
    Rooted tree implementation using linked representation.
    
    Supports:
        - Tree construction and modification
        - Various traversal methods
        - Tree metrics (height, depth, size)
        - Search operations
    
    Visual example:
                    [1]          <- root
                   / | \
                [2] [3] [4]
               / \     / | \
             [5] [6] [7][8][9]
    """
    
    def __init__(self, root_data: Any = None):
        """
        Initialize tree with optional root.
        
        Args:
            root_data: Value for root node (None creates empty tree)
        """
        self._root = TreeNode(root_data) if root_data is not None else None
        self._size = 1 if root_data is not None else 0
    
    def __len__(self) -> int:
        """Return number of nodes. O(1)"""
        return self._size
    
    def __bool__(self) -> bool:
        """Return True if tree has nodes. O(1)"""
        return self._root is not None
    
    def __repr__(self) -> str:
        return f"RootedTree(size={self._size}, root={self._root})"
    
    def __contains__(self, data: Any) -> bool:
        """Check if data exists in tree. O(n)"""
        return self.find(data) is not None
    
    @property
    def root(self) -> Optional[TreeNode]:
        """Get root node."""
        return self._root
    
    def is_empty(self) -> bool:
        """Check if tree is empty. O(1)"""
        return self._root is None
    
    def set_root(self, data: Any) -> TreeNode:
        """
        Set or replace root node. O(1)
        
        Args:
            data: Value for root
            
        Returns:
            The root node
        """
        if self._root is None:
            self._root = TreeNode(data)
            self._size = 1
        else:
            self._root.data = data
        return self._root
    
    def insert(self, parent_data: Any, child_data: Any) -> Optional[TreeNode]:
        """
        Insert child under node with given data. O(n)
        
        Must first find the parent node.
        
        Args:
            parent_data: Data of parent node
            child_data: Data for new child
            
        Returns:
            New child node, or None if parent not found
        """
        parent = self.find(parent_data)
        if parent is None:
            return None
        
        child = parent.add_child(child_data)
        self._size += 1
        return child
    
    def find(self, data: Any) -> Optional[TreeNode]:
        """
        Find node with given data. O(n)
        
        Uses BFS for level-order search.
        
        Args:
            data: Value to find
            
        Returns:
            Node with data, or None if not found
        """
        if self._root is None:
            return None
        
        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            if node.data == data:
                return node
            queue.extend(node.children)
        
        return None
    
    def delete(self, data: Any) -> bool:
        """
        Delete node and its subtree. O(n)
        
        Cannot delete root this way.
        
        Args:
            data: Data of node to delete
            
        Returns:
            True if deleted, False if not found
        """
        node = self.find(data)
        if node is None or node == self._root:
            return False
        
        # Count nodes in subtree to update size
        subtree_size = self._count_nodes(node)
        
        node.parent.remove_child(node)
        self._size -= subtree_size
        return True
    
    def _count_nodes(self, node: TreeNode) -> int:
        """Count nodes in subtree rooted at node."""
        count = 1
        for child in node.children:
            count += self._count_nodes(child)
        return count
    
    def height(self) -> int:
        """
        Get height of tree. O(n)
        
        Height = length of longest path from root to leaf.
        Empty tree has height -1, single node has height 0.
        
        Returns:
            Height of tree
        """
        if self._root is None:
            return -1
        return self._node_height(self._root)
    
    def _node_height(self, node: TreeNode) -> int:
        """Get height of subtree rooted at node."""
        if node.is_leaf():
            return 0
        return 1 + max(self._node_height(c) for c in node.children)
    
    def depth(self, data: Any) -> int:
        """
        Get depth of node with given data. O(n)
        
        Args:
            data: Data to find depth of
            
        Returns:
            Depth of node, or -1 if not found
        """
        node = self.find(data)
        if node is None:
            return -1
        return node.depth()
    
    def get_leaves(self) -> List[TreeNode]:
        """
        Get all leaf nodes. O(n)
        
        Returns:
            List of leaf nodes
        """
        leaves = []
        
        def collect_leaves(node):
            if node.is_leaf():
                leaves.append(node)
            for child in node.children:
                collect_leaves(child)
        
        if self._root:
            collect_leaves(self._root)
        
        return leaves
    
    def traverse_preorder(self) -> List[Any]:
        """
        Pre-order traversal: root, then children. O(n)
        
        Also called depth-first traversal.
        
        Returns:
            List of node data in pre-order
        """
        result = []
        
        def preorder(node):
            result.append(node.data)
            for child in node.children:
                preorder(child)
        
        if self._root:
            preorder(self._root)
        
        return result
    
    def traverse_postorder(self) -> List[Any]:
        """
        Post-order traversal: children, then root. O(n)
        
        Useful for deletion (delete children before parent).
        
        Returns:
            List of node data in post-order
        """
        result = []
        
        def postorder(node):
            for child in node.children:
                postorder(child)
            result.append(node.data)
        
        if self._root:
            postorder(self._root)
        
        return result
    
    def traverse_levelorder(self) -> List[Any]:
        """
        Level-order traversal (BFS). O(n)
        
        Visits nodes level by level, left to right.
        
        Returns:
            List of node data in level order
        """
        if self._root is None:
            return []
        
        result = []
        queue = deque([self._root])
        
        while queue:
            node = queue.popleft()
            result.append(node.data)
            queue.extend(node.children)
        
        return result
    
    def traverse_with_depth(self) -> List[tuple]:
        """
        Traverse with depth information. O(n)
        
        Returns:
            List of (data, depth) tuples
        """
        result = []
        
        def traverse(node, depth):
            result.append((node.data, depth))
            for child in node.children:
                traverse(child, depth + 1)
        
        if self._root:
            traverse(self._root, 0)
        
        return result
    
    def display(self, indent: str = "  ") -> None:
        """
        Pretty print tree structure. O(n)
        
        Args:
            indent: String to use for indentation
        """
        def print_node(node, prefix="", is_last=True):
            connector = "└── " if is_last else "├── "
            print(prefix + connector + str(node.data))
            
            children = node.children
            for i, child in enumerate(children):
                is_child_last = (i == len(children) - 1)
                new_prefix = prefix + ("    " if is_last else "│   ")
                print_node(child, new_prefix, is_child_last)
        
        if self._root:
            print(self._root.data)
            for i, child in enumerate(self._root.children):
                is_last = (i == len(self._root.children) - 1)
                print_node(child, "", is_last)
        else:
            print("(empty tree)")
    
    def clear(self) -> None:
        """Remove all nodes. O(1)"""
        self._root = None
        self._size = 0
    
    def to_dict(self) -> dict:
        """
        Convert to nested dictionary representation. O(n)
        
        Returns:
            Dict with 'data' and 'children' keys
        """
        def node_to_dict(node):
            return {
                'data': node.data,
                'children': [node_to_dict(c) for c in node.children]
            }
        
        if self._root:
            return node_to_dict(self._root)
        return {}
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RootedTree':
        """
        Create tree from nested dictionary. O(n)
        
        Args:
            data: Dict with 'data' and 'children' keys
            
        Returns:
            New RootedTree instance
        """
        if not data:
            return cls()
        
        tree = cls(data.get('data'))
        
        def build_children(parent_node, children_data):
            for child_data in children_data:
                child_node = parent_node.add_child(child_data.get('data'))
                tree._size += 1
                build_children(child_node, child_data.get('children', []))
        
        build_children(tree._root, data.get('children', []))
        
        return tree
