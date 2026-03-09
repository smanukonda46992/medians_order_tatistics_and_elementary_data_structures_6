"""
Plotting utilities for experiment results.
"""

import os
from typing import List, Dict

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def plot_selection_comparison(sizes: List[int], mom_results: List[Dict], 
                               rs_results: List[Dict], dist_name: str,
                               output_path: str) -> None:
    """
    Plot comparison of Median of Medians vs Randomized Select.
    
    Args:
        sizes: List of input sizes
        mom_results: Median of Medians timing results
        rs_results: Randomized Select timing results
        dist_name: Name of input distribution
        output_path: Path to save the plot
    """
    if not HAS_MATPLOTLIB:
        print("matplotlib not available, skipping plot generation")
        return
    
    mom_times = [r['mean'] * 1000 for r in mom_results]  # Convert to ms
    rs_times = [r['mean'] * 1000 for r in rs_results]
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(sizes, mom_times, 'b-o', label='Median of Medians', linewidth=2, markersize=8)
    plt.plot(sizes, rs_times, 'r-s', label='Randomized Select', linewidth=2, markersize=8)
    
    plt.xlabel('Input Size (n)', fontsize=12)
    plt.ylabel('Time (ms)', fontsize=12)
    plt.title(f'Selection Algorithm Comparison - {dist_name.replace("_", " ").title()} Distribution', 
              fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Add complexity reference lines
    max_time = max(max(mom_times), max(rs_times))
    ref_n = [s * max_time / max(sizes) for s in sizes]
    plt.plot(sizes, ref_n, 'g--', alpha=0.5, label='O(n) reference')
    plt.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_ds_comparison(sizes: List[int], results: Dict, output_dir: str) -> None:
    """
    Plot data structure operation comparisons.
    
    Args:
        sizes: List of input sizes
        results: Dictionary of results by data structure
        output_dir: Directory to save plots
    """
    if not HAS_MATPLOTLIB:
        print("matplotlib not available, skipping plot generation")
        return
    
    # Plot insert operations comparison
    plt.figure(figsize=(12, 5))
    
    # Insert operations
    plt.subplot(1, 2, 1)
    
    if 'DynamicArray' in results and 'append' in results['DynamicArray']:
        times = [r['mean'] * 1e6 for r in results['DynamicArray']['append']]
        plt.plot(sizes, times, 'b-o', label='Array append', linewidth=2)
    
    if 'Stack' in results and 'push' in results['Stack']:
        times = [r['mean'] * 1e6 for r in results['Stack']['push']]
        plt.plot(sizes, times, 'r-s', label='Stack push', linewidth=2)
    
    if 'Queue' in results and 'enqueue' in results['Queue']:
        times = [r['mean'] * 1e6 for r in results['Queue']['enqueue']]
        plt.plot(sizes, times, 'g-^', label='Queue enqueue', linewidth=2)
    
    if 'LinkedList' in results and 'insert_front' in results['LinkedList']:
        times = [r['mean'] * 1e6 for r in results['LinkedList']['insert_front']]
        plt.plot(sizes, times, 'm-d', label='LinkedList insert_front', linewidth=2)
    
    plt.xlabel('Data Structure Size', fontsize=11)
    plt.ylabel('Time per Operation (μs)', fontsize=11)
    plt.title('Insert Operations Comparison', fontsize=12)
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)
    
    # Delete operations
    plt.subplot(1, 2, 2)
    
    if 'Stack' in results and 'pop' in results['Stack']:
        times = [r['mean'] * 1e6 for r in results['Stack']['pop']]
        plt.plot(sizes, times, 'r-s', label='Stack pop', linewidth=2)
    
    if 'Queue' in results and 'dequeue' in results['Queue']:
        times = [r['mean'] * 1e6 for r in results['Queue']['dequeue']]
        plt.plot(sizes, times, 'g-^', label='Queue dequeue', linewidth=2)
    
    if 'LinkedList' in results and 'delete_front' in results['LinkedList']:
        times = [r['mean'] * 1e6 for r in results['LinkedList']['delete_front']]
        plt.plot(sizes, times, 'm-d', label='LinkedList delete_front', linewidth=2)
    
    plt.xlabel('Data Structure Size', fontsize=11)
    plt.ylabel('Time per Operation (μs)', fontsize=11)
    plt.title('Delete Operations Comparison', fontsize=12)
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'ds_operations.png'), dpi=150)
    plt.close()
    
    # Search operations comparison
    plt.figure(figsize=(10, 6))
    
    if 'DynamicArray' in results and 'search' in results['DynamicArray']:
        times = [r['mean'] * 1000 for r in results['DynamicArray']['search']]
        plt.plot(sizes, times, 'b-o', label='Array search', linewidth=2)
    
    if 'LinkedList' in results and 'search' in results['LinkedList']:
        times = [r['mean'] * 1000 for r in results['LinkedList']['search']]
        plt.plot(sizes, times, 'm-d', label='LinkedList search', linewidth=2)
    
    plt.xlabel('Data Structure Size', fontsize=11)
    plt.ylabel('Time per Search (ms)', fontsize=11)
    plt.title('Search Operation Comparison (Linear Search)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'ds_search.png'), dpi=150)
    plt.close()


def save_results_csv(results: Dict, sizes: List[int], output_path: str) -> None:
    """
    Save benchmark results to CSV file.
    
    Args:
        results: Dictionary of results
        sizes: List of input sizes
        output_path: Path to save CSV
    """
    with open(output_path, 'w') as f:
        f.write("distribution,algorithm,size,mean_time,median_time,stdev\n")
        
        for dist_name, dist_results in results.items():
            for algo_name, algo_results in dist_results.items():
                for r in algo_results:
                    f.write(f"{dist_name},{algo_name},{r['size']},"
                           f"{r['mean']:.6f},{r['median']:.6f},{r['stdev']:.6f}\n")
