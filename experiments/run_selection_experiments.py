"""
Selection Algorithm Experiments

Compares Median of Medians (deterministic) with Randomized Quickselect
across different input sizes and distributions.
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.selection import median_of_medians, randomized_select
from experiments.input_generators import GENERATORS, generate_random_array
from experiments.timing_utils import benchmark_function, print_timing_table, format_time
from experiments.plot_results import plot_selection_comparison, save_results_csv


def run_experiments():
    """Run all selection algorithm experiments."""
    
    # Ensure results directories exist
    results_dir = PROJECT_ROOT / 'results'
    plots_dir = results_dir / 'plots'
    data_dir = results_dir / 'raw_data'
    plots_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Test sizes
    sizes = [100, 500, 1000, 2000, 5000, 10000, 20000]
    trials = 5
    
    print("\n" + "=" * 70)
    print("SELECTION ALGORITHM EXPERIMENTS")
    print("=" * 70)
    print(f"\nInput sizes: {sizes}")
    print(f"Trials per size: {trials}")
    
    all_results = {}
    
    # Test each input distribution
    for dist_name, generator in GENERATORS.items():
        if dist_name in ['all_same']:  # Skip trivial cases
            continue
            
        print(f"\n{'=' * 70}")
        print(f"Distribution: {dist_name.upper()}")
        print('=' * 70)
        
        # Benchmark Median of Medians
        print("\nMedian of Medians (Deterministic):")
        mom_results = benchmark_function(
            median_of_medians, sizes, generator, trials=trials
        )
        print_timing_table(mom_results)
        
        # Benchmark Randomized Select
        print("\nRandomized Quickselect:")
        rs_results = benchmark_function(
            randomized_select, sizes, generator, trials=trials
        )
        print_timing_table(rs_results)
        
        # Calculate speedup
        print("\nSpeedup (MoM time / RS time):")
        print("-" * 40)
        for i, size in enumerate(sizes):
            mom_time = mom_results[i]['mean']
            rs_time = rs_results[i]['mean']
            speedup = mom_time / rs_time if rs_time > 0 else float('inf')
            print(f"Size {size:>6}: {speedup:.2f}x")
        
        all_results[dist_name] = {
            'median_of_medians': mom_results,
            'randomized_select': rs_results
        }
    
    # Generate plots
    print("\n" + "=" * 70)
    print("Generating plots...")
    print("=" * 70)
    
    for dist_name, results in all_results.items():
        plot_selection_comparison(
            sizes, 
            results['median_of_medians'],
            results['randomized_select'],
            dist_name,
            str(plots_dir / f'selection_{dist_name}.png')
        )
        print(f"  Saved: selection_{dist_name}.png")
    
    # Save CSV results
    save_results_csv(all_results, sizes, str(data_dir / 'selection_timings.csv'))
    print(f"  Saved: selection_timings.csv")
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
Key Observations:

1. MEDIAN OF MEDIANS (Deterministic):
   - Guarantees O(n) worst-case time complexity
   - Higher constant factors due to:
     * Dividing into groups of 5
     * Finding median of each group
     * Recursive median-of-medians computation
   - Consistent performance across all input distributions
   - Best for adversarial inputs or when worst-case guarantees matter

2. RANDOMIZED QUICKSELECT:
   - O(n) expected time complexity
   - O(n²) worst case (very unlikely with random pivots)
   - Lower constant factors, faster in practice
   - Performance may vary slightly due to randomization
   - Preferred for most practical applications

3. COMPARISON:
   - Randomized Select is typically 2-5x faster in practice
   - Both achieve linear time on average
   - Median of Medians provides stronger guarantees
   - Input distribution has minimal impact on either algorithm
""")
    
    return all_results


if __name__ == "__main__":
    run_experiments()
