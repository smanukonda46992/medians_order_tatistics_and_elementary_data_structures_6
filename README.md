<p align="center">
  <h1 align="center">📊 Medians, Order Statistics & Elementary Data Structures</h1>
  <p align="center">
    <strong>Implementation, Analysis & Applications</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Algorithm-Selection%20%26%20Data%20Structures-green?style=flat" alt="Algorithm">
    <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat" alt="License">
  </p>
</p>

---

## 📑 Table of Contents

- [📋 Overview](#-overview)
- [🚀 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🔬 Part 1: Selection Algorithms](#-part-1-selection-algorithms)
- [🗃️ Part 2: Elementary Data Structures](#️-part-2-elementary-data-structures)
- [📊 Complexity Analysis](#-complexity-analysis)
- [📈 Performance Results](#-performance-results)
- [🔑 Key Findings](#-key-findings)
- [📚 Documentation](#-documentation)
- [🛠️ Tech Stack](#️-tech-stack)
- [📜 License](#-license)
- [📖 Analysis Results](docs/analysis_results.md)  <!-- Added navigation to detailed empirical analysis -->

---

## 📋 Overview

A comprehensive implementation of **Selection Algorithms** (Median of Medians, Randomized Quickselect) and **Elementary Data Structures** (Arrays, Stacks, Queues, Linked Lists) with detailed performance analysis across different input distributions.

> 📖 **[Read the Full Analysis Report →](docs/report.md)**

---

## 🚀 Quick Start

```bash
# Clone & setup
pip3 install -r requirements.txt

# Run demo
python3 main.py demo

# Run full analysis
python3 main.py all

# Run tests
python3 main.py tests
```

---

## 📁 Project Structure

```
📦 medians_order_tatistics_and_elementary_data_structures_6
 ┣ 📂 src/
 ┃ ┣ 📂 selection/
 ┃ ┃ ┣ 📄 __init__.py
 ┃ ┃ ┣ 📄 median_of_medians.py    # Deterministic O(n) selection
 ┃ ┃ ┣ 📄 randomized_select.py    # Randomized O(n) expected selection
 ┃ ┃ ┗ 📄 utils.py                # Helper functions
 ┃ ┣ 📂 data_structures/
 ┃ ┃ ┣ 📄 __init__.py
 ┃ ┃ ┣ 📄 dynamic_array.py        # Array with dynamic resizing
 ┃ ┃ ┣ 📄 matrix.py               # Matrix operations
 ┃ ┃ ┣ 📄 stack.py                # Array-based stack
 ┃ ┃ ┣ 📄 queue.py                # Array-based queue
 ┃ ┃ ┣ 📄 linked_list.py          # Singly linked list
 ┃ ┃ ┗ 📄 rooted_tree.py          # Tree using linked representation
 ┃ ┗ 📄 __init__.py
 ┣ 📂 experiments/
 ┃ ┣ 📄 run_selection_experiments.py
 ┃ ┣ 📄 run_data_structure_experiments.py
 ┃ ┣ 📄 input_generators.py
 ┃ ┣ 📄 timing_utils.py
 ┃ ┗ 📄 plot_results.py
 ┣ 📂 tests/
 ┃ ┣ 📄 test_selection.py
 ┃ ┗ 📄 test_data_structures.py
 ┣ 📂 docs/
 ┃ ┗ 📄 report.md                  # Comprehensive analysis report
 ┣ 📂 results/
 ┃ ┣ 📂 plots/
 ┃ ┗ 📂 raw_data/
 ┣ 📄 main.py                      # Main entry point
 ┣ 📄 requirements.txt
 ┣ 📄 LICENSE
 ┗ 📄 README.md
```

### Module Overview

| File | Purpose |
|------|---------|
| `median_of_medians.py` | Deterministic linear-time selection (worst-case O(n)) |
| `randomized_select.py` | Randomized selection (expected O(n)) |
| `dynamic_array.py` | Dynamic array with amortized O(1) append |
| `stack.py` | LIFO stack with O(1) push/pop |
| `queue.py` | FIFO queue with O(1) enqueue/dequeue |
| `linked_list.py` | Singly linked list with O(1) insert at head |
| `rooted_tree.py` | Tree structure using linked representation |

---

## 🔬 Part 1: Selection Algorithms

### Median of Medians (Deterministic)

The **Median of Medians** algorithm guarantees **O(n) worst-case** time complexity for selecting the k-th smallest element.

**Algorithm Steps:**
1. Divide array into groups of 5
2. Find median of each group
3. Recursively find median of medians
4. Use this as pivot for partitioning
5. Recurse on appropriate partition

```python
from src.selection import median_of_medians

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
k = 5
result = median_of_medians(arr, k)  # 5th smallest element
print(f"The {k}th smallest element is: {result}")
```

### Randomized Quickselect

**Randomized Quickselect** achieves **O(n) expected** time complexity with simpler implementation.

```python
from src.selection import randomized_select

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
k = 5
result = randomized_select(arr, k)  # 5th smallest element
print(f"The {k}th smallest element is: {result}")
```

---

## 🗃️ Part 2: Elementary Data Structures

### Dynamic Array

```python
from src.data_structures import DynamicArray

arr = DynamicArray()
arr.append(10)      # O(1) amortized
arr.insert(0, 5)    # O(n)
arr.delete(1)       # O(n)
print(arr[0])       # O(1) access
```

### Stack (LIFO)

```python
from src.data_structures import Stack

stack = Stack()
stack.push(1)       # O(1)
stack.push(2)       # O(1)
top = stack.pop()   # O(1) -> returns 2
peek = stack.peek() # O(1) -> returns 1
```

### Queue (FIFO)

```python
from src.data_structures import Queue

queue = Queue()
queue.enqueue(1)    # O(1)
queue.enqueue(2)    # O(1)
front = queue.dequeue()  # O(1) -> returns 1
```

### Singly Linked List

```python
from src.data_structures import LinkedList

ll = LinkedList()
ll.insert_front(1)  # O(1)
ll.insert_end(3)    # O(n)
ll.insert_after(1, 2)  # O(n)
ll.delete(2)        # O(n)
ll.traverse()       # O(n) -> prints all elements
```

---

## 📊 Complexity Analysis

### Selection Algorithms

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Median of Medians | O(n) | O(n) | **O(n)** | O(log n) |
| Randomized Select | O(n) | O(n) | O(n²) | O(log n) |

### Data Structures

| Operation | Array | Stack | Queue | Linked List |
|-----------|-------|-------|-------|-------------|
| Access | **O(1)** | O(n) | O(n) | O(n) |
| Insert (front) | O(n) | - | - | **O(1)** |
| Insert (end) | **O(1)*** | **O(1)** | **O(1)** | O(n) |
| Delete | O(n) | **O(1)** | **O(1)** | O(n) |
| Search | O(n) | O(n) | O(n) | O(n) |

*Amortized for dynamic array

---

## 📈 Performance Results

Performance plots and detailed empirical analysis are available in the [Analysis Results](docs/analysis_results.md).

---

## 🔑 Key Findings

1. **Median of Medians** guarantees O(n) worst-case but has higher constants than Randomized Select
2. **Randomized Select** is faster in practice for most inputs but has O(n²) worst-case
3. **Arrays** excel at random access but struggle with insertions/deletions
4. **Linked Lists** excel at insertions/deletions at known positions but struggle with random access
5. **Stacks and Queues** provide efficient O(1) operations for their intended use cases

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[📊 docs/report.md](docs/report.md)** | **⭐ MAIN REPORT - Comprehensive analysis** |
| [README.md](README.md) | This file - Quick start guide |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **matplotlib** - Visualization
- **numpy** - Numerical operations
- **unittest** - Testing framework

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---