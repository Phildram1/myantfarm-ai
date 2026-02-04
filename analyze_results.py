"""
Analyze MyAntFarm.ai trial results.

This script loads trial data, computes statistics, and displays results
comparing C1 (Baseline), C2 (Single-Agent), and C3 (Multi-Agent) conditions.

Usage:
    python analyze_results.py
    python analyze_results.py --results-file path/to/all_trials.json
"""

import json
import argparse
from pathlib import Path
import sys

try:
    import numpy as np
    from scipy import stats
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install: pip install pandas numpy scipy")
    sys.exit(1)


def load_results(results_file):
    """Load trial results from JSON file."""
    if not Path(results_file).exists():
        print(f"Error: Results file not found: {results_file}")
        print("\nMake sure you've run the evaluation first:")
        print("  docker exec -it myantfarm_evaluator python run_evaluation.py")
        sys.exit(1)
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    return data


def extract_dq_scores(trials, condition):
    """Extract DQ scores for a specific condition."""
    scores = []
    for trial in trials:
        if trial['condition'] == condition:
            dq_score = trial.get('dq_score', 0.0)
            scores.append(dq_score)
    return np.array(scores)


def calculate_statistics(scores):
    """Calculate statistics for a set of scores."""
    return {
        'mean': np.mean(scores),
        'std': np.std(scores, ddof=1),
        'min': np.min(scores),
        'max': np.max(scores),
        'median': np.median(scores),
        'count': len(scores),
        'actionable': np.sum(scores > 0.5),
        'actionable_pct': (np.sum(scores > 0.5) / len(scores)) * 100
    }


def mann_whitney_u_test(group1, group2):
    """Perform Mann-Whitney U test."""
    statistic, p_value = stats.mannwhitneyu(group1, group2, alternative='two-sided')
    return {'statistic': statistic, 'p_value': p_value}


def cohens_d(group1, group2):
    """Calculate Cohen's d effect size."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    if pooled_std == 0:
        return float('inf') if np.mean(group1) != np.mean(group2) else 0
    
    return (np.mean(group1) - np.mean(group2)) / pooled_std


def display_results(data):
    """Display formatted results."""
    trials = data['trials']
    
    # Extract scores by condition
    c1_scores = extract_dq_scores(trials, 'C1')
    c2_scores = extract_dq_scores(trials, 'C2')
    c3_scores = extract_dq_scores(trials, 'C3')
    
    # Calculate statistics
    c1_stats = calculate_statistics(c1_scores)
    c2_stats = calculate_statistics(c2_scores)
    c3_stats = calculate_statistics(c3_scores)
    
    # Statistical tests
    c2_c3_test = mann_whitney_u_test(c2_scores, c3_scores)
    c2_c3_effect = cohens_d(c2_scores, c3_scores)
    
    # Display results
    print("\n" + "=" * 70)
    print("MYANTFARM.AI EVALUATION RESULTS")
    print("=" * 70)
    
    print("\n" + "-" * 70)
    print("C1 (Baseline - No LLM):")
    print("-" * 70)
    print(f"  Trials:           {c1_stats['count']}")
    print(f"  Mean DQ:          {c1_stats['mean']:.3f}")
    print(f"  Std DQ:           {c1_stats['std']:.3f}")
    print(f"  Range:            [{c1_stats['min']:.3f}, {c1_stats['max']:.3f}]")
    print(f"  Actionable:       {c1_stats['actionable']}/{c1_stats['count']} ({c1_stats['actionable_pct']:.1f}%)")
    
    print("\n" + "-" * 70)
    print("C2 (Single-Agent):")
    print("-" * 70)
    print(f"  Trials:           {c2_stats['count']}")
    print(f"  Mean DQ:          {c2_stats['mean']:.3f}")
    print(f"  Std DQ:           {c2_stats['std']:.3f}")
    print(f"  Range:            [{c2_stats['min']:.3f}, {c2_stats['max']:.3f}]")
    print(f"  Actionable:       {c2_stats['actionable']}/{c2_stats['count']} ({c2_stats['actionable_pct']:.1f}%)")
    
    print("\n" + "-" * 70)
    print("C3 (Multi-Agent):")
    print("-" * 70)
    print(f"  Trials:           {c3_stats['count']}")
    print(f"  Mean DQ:          {c3_stats['mean']:.3f}")
    print(f"  Std DQ:           {c3_stats['std']:.3f}")
    print(f"  Range:            [{c3_stats['min']:.3f}, {c3_stats['max']:.3f}]")
    print(f"  Actionable:       {c3_stats['actionable']}/{c3_stats['count']} ({c3_stats['actionable_pct']:.1f}%)")
    
    print("\n" + "=" * 70)
    print("STATISTICAL COMPARISON (C2 vs C3)")
    print("=" * 70)
    print(f"  DQ Improvement:   {((c3_stats['mean'] - c2_stats['mean']) / c2_stats['mean'] * 100):.1f}%")
    print(f"  Mann-Whitney U:   U={c2_c3_test['statistic']:.1f}, p={c2_c3_test['p_value']:.4e}")
    print(f"  Cohen's d:        {c2_c3_effect:.2f}")
    
    if c2_c3_test['p_value'] < 0.001:
        print(f"  Significance:     *** p < 0.001 (highly significant)")
    elif c2_c3_test['p_value'] < 0.01:
        print(f"  Significance:     ** p < 0.01 (very significant)")
    elif c2_c3_test['p_value'] < 0.05:
        print(f"  Significance:     * p < 0.05 (significant)")
    else:
        print(f"  Significance:     Not significant (p >= 0.05)")
    
    print("\n" + "=" * 70)
    print("KEY FINDINGS")
    print("=" * 70)
    
    # Determine if results match expected
    c2_mean_ok = 0.39 <= c2_stats['mean'] <= 0.42
    c3_mean_ok = 0.68 <= c3_stats['mean'] <= 0.71
    c3_variance_ok = c3_stats['std'] < 0.01
    c3_actionable_ok = c3_stats['actionable_pct'] >= 95
    
    if c2_mean_ok and c3_mean_ok and c3_variance_ok and c3_actionable_ok:
        print("✓ Results match expected values from paper!")
        print(f"  • C2 Mean DQ: {c2_stats['mean']:.3f} (expected: ~0.403)")
        print(f"  • C3 Mean DQ: {c3_stats['mean']:.3f} (expected: ~0.692)")
        print(f"  • C3 Std DQ:  {c3_stats['std']:.3f} (expected: 0.000)")
        print(f"  • C3 Actionable: {c3_stats['actionable_pct']:.1f}% (expected: 100%)")
    else:
        print("⚠ Results differ from expected values:")
        if not c2_mean_ok:
            print(f"  • C2 Mean DQ: {c2_stats['mean']:.3f} (expected: ~0.403)")
        if not c3_mean_ok:
            print(f"  • C3 Mean DQ: {c3_stats['mean']:.3f} (expected: ~0.692)")
        if not c3_variance_ok:
            print(f"  • C3 Std DQ:  {c3_stats['std']:.3f} (expected: 0.000)")
        if not c3_actionable_ok:
            print(f"  • C3 Actionable: {c3_stats['actionable_pct']:.1f}% (expected: 100%)")
        print("\nSee Troubleshooting section in README for common issues.")
    
    print("\n" + "=" * 70)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Analyze MyAntFarm.ai trial results",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--results-file',
        default='data/results/all_trials.json',
        help='Path to results JSON file (default: data/results/all_trials.json)'
    )
    
    args = parser.parse_args()
    
    # Try multiple possible locations
    possible_paths = [
        args.results_file,
        'data/results/all_trials.json',
        'results/all_trials.json',
        '/app/results/all_trials.json'
    ]
    
    results_file = None
    for path in possible_paths:
        if Path(path).exists():
            results_file = path
            break
    
    if not results_file:
        print("Error: Could not find results file in any of these locations:")
        for path in possible_paths:
            print(f"  - {path}")
        print("\nMake sure you've completed the evaluation and scoring steps.")
        sys.exit(1)
    
    print(f"Loading results from: {results_file}")
    data = load_results(results_file)
    
    display_results(data)


if __name__ == "__main__":
    main()
