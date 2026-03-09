"""
Matrix Implementation

A 2D array (matrix) implementation with basic operations.

Time Complexity Analysis:
    Access (get/set): O(1)
        - Direct index calculation: address = base + (row * cols + col) * element_size
        
    Row/Column access: O(n) where n is the dimension
        - Must copy n elements
        
    Matrix addition/subtraction: O(m*n)
        - Must visit every element
        
    Matrix multiplication: O(m*n*p)
        - For A(m×n) × B(n×p), each of m*p results needs n multiplications

Space Complexity: O(m*n) for an m×n matrix
"""

from typing import Any, List, Optional


class Matrix:
    """
    2D matrix implementation using a 1D array internally.
    
    Using 1D array provides:
    - Better cache locality (contiguous memory)
    - Simpler memory management
    - Same O(1) access time
    
    Attributes:
        _data: Internal 1D list storing elements in row-major order
        _rows: Number of rows
        _cols: Number of columns
    """
    
    def __init__(self, rows: int, cols: int, default: Any = 0):
        """
        Initialize matrix with given dimensions.
        
        Args:
            rows: Number of rows
            cols: Number of columns
            default: Default value for all elements
        """
        if rows <= 0 or cols <= 0:
            raise ValueError("Dimensions must be positive")
        
        self._rows = rows
        self._cols = cols
        self._data: List[Any] = [default] * (rows * cols)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Matrix({self._rows}×{self._cols})"
    
    def __str__(self) -> str:
        """Human-readable string showing matrix contents."""
        lines = []
        for i in range(self._rows):
            row = [self._data[i * self._cols + j] for j in range(self._cols)]
            lines.append(str(row))
        return '\n'.join(lines)
    
    @property
    def rows(self) -> int:
        """Number of rows."""
        return self._rows
    
    @property
    def cols(self) -> int:
        """Number of columns."""
        return self._cols
    
    @property
    def shape(self) -> tuple:
        """Matrix dimensions as (rows, cols)."""
        return (self._rows, self._cols)
    
    def _index(self, row: int, col: int) -> int:
        """
        Convert 2D indices to 1D index (row-major order).
        
        Formula: index = row * cols + col
        
        This is how 2D arrays are stored in memory in C/C++ and most languages.
        """
        return row * self._cols + col
    
    def _validate_indices(self, row: int, col: int) -> None:
        """Validate row and column indices."""
        if row < 0 or row >= self._rows:
            raise IndexError(f"Row {row} out of bounds [0, {self._rows})")
        if col < 0 or col >= self._cols:
            raise IndexError(f"Column {col} out of bounds [0, {self._cols})")
    
    def get(self, row: int, col: int) -> Any:
        """
        Get element at (row, col). O(1)
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            Element at position
            
        Raises:
            IndexError: If indices out of bounds
        """
        self._validate_indices(row, col)
        return self._data[self._index(row, col)]
    
    def set(self, row: int, col: int, value: Any) -> None:
        """
        Set element at (row, col). O(1)
        
        Args:
            row: Row index
            col: Column index
            value: Value to set
            
        Raises:
            IndexError: If indices out of bounds
        """
        self._validate_indices(row, col)
        self._data[self._index(row, col)] = value
    
    def __getitem__(self, key: tuple) -> Any:
        """Get element using matrix[row, col] syntax."""
        row, col = key
        return self.get(row, col)
    
    def __setitem__(self, key: tuple, value: Any) -> None:
        """Set element using matrix[row, col] = value syntax."""
        row, col = key
        self.set(row, col, value)
    
    def get_row(self, row: int) -> List[Any]:
        """
        Get entire row as list. O(cols)
        
        Args:
            row: Row index
            
        Returns:
            List of elements in row
        """
        if row < 0 or row >= self._rows:
            raise IndexError(f"Row {row} out of bounds")
        start = row * self._cols
        return self._data[start:start + self._cols]
    
    def get_col(self, col: int) -> List[Any]:
        """
        Get entire column as list. O(rows)
        
        Args:
            col: Column index
            
        Returns:
            List of elements in column
        """
        if col < 0 or col >= self._cols:
            raise IndexError(f"Column {col} out of bounds")
        return [self._data[i * self._cols + col] for i in range(self._rows)]
    
    def set_row(self, row: int, values: List[Any]) -> None:
        """
        Set entire row. O(cols)
        
        Args:
            row: Row index
            values: List of values (must match column count)
        """
        if len(values) != self._cols:
            raise ValueError(f"Expected {self._cols} values, got {len(values)}")
        if row < 0 or row >= self._rows:
            raise IndexError(f"Row {row} out of bounds")
        
        start = row * self._cols
        for j, v in enumerate(values):
            self._data[start + j] = v
    
    def set_col(self, col: int, values: List[Any]) -> None:
        """
        Set entire column. O(rows)
        
        Args:
            col: Column index
            values: List of values (must match row count)
        """
        if len(values) != self._rows:
            raise ValueError(f"Expected {self._rows} values, got {len(values)}")
        if col < 0 or col >= self._cols:
            raise IndexError(f"Column {col} out of bounds")
        
        for i, v in enumerate(values):
            self._data[i * self._cols + col] = v
    
    def transpose(self) -> 'Matrix':
        """
        Return transposed matrix. O(rows * cols)
        
        Returns:
            New matrix with dimensions swapped
        """
        result = Matrix(self._cols, self._rows)
        for i in range(self._rows):
            for j in range(self._cols):
                result[j, i] = self[i, j]
        return result
    
    def add(self, other: 'Matrix') -> 'Matrix':
        """
        Matrix addition. O(rows * cols)
        
        Args:
            other: Matrix to add (must have same dimensions)
            
        Returns:
            New matrix with sum
        """
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
        
        result = Matrix(self._rows, self._cols)
        for i in range(len(self._data)):
            result._data[i] = self._data[i] + other._data[i]
        return result
    
    def multiply(self, other: 'Matrix') -> 'Matrix':
        """
        Matrix multiplication. O(rows * cols * other.cols)
        
        Args:
            other: Matrix to multiply with (self.cols must equal other.rows)
            
        Returns:
            New matrix with product
        """
        if self._cols != other._rows:
            raise ValueError(f"Cannot multiply: {self.shape} × {other.shape}")
        
        result = Matrix(self._rows, other._cols)
        for i in range(self._rows):
            for j in range(other._cols):
                total = 0
                for k in range(self._cols):
                    total += self[i, k] * other[k, j]
                result[i, j] = total
        return result
    
    def to_list(self) -> List[List[Any]]:
        """Convert to 2D Python list."""
        return [self.get_row(i) for i in range(self._rows)]
    
    @classmethod
    def from_list(cls, data: List[List[Any]]) -> 'Matrix':
        """Create Matrix from 2D list."""
        if not data or not data[0]:
            raise ValueError("Empty data")
        
        rows = len(data)
        cols = len(data[0])
        
        matrix = cls(rows, cols)
        for i, row in enumerate(data):
            if len(row) != cols:
                raise ValueError(f"Inconsistent row lengths")
            matrix.set_row(i, row)
        
        return matrix
    
    @classmethod
    def identity(cls, n: int) -> 'Matrix':
        """Create n×n identity matrix."""
        matrix = cls(n, n, 0)
        for i in range(n):
            matrix[i, i] = 1
        return matrix
    
    @classmethod
    def zeros(cls, rows: int, cols: int) -> 'Matrix':
        """Create matrix filled with zeros."""
        return cls(rows, cols, 0)
    
    @classmethod
    def ones(cls, rows: int, cols: int) -> 'Matrix':
        """Create matrix filled with ones."""
        return cls(rows, cols, 1)
