"""
Re-score all existing trial results with corrected DQ formula.
This script reads original trial outputs and applies DQScorer v2.0.
"""

import json
import pandas as pd
from pathlib import Path
import sys
from typing import Dict, List

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scoring.dq_scorer_v2 import DQScorer
from analysis.statistical_tests import StatisticalAnalyzer


def load_trial_results(results_dir: Path) -> List[Dict]:
    """Load all trial JSON files from results directory."""
    trials = []
    
    for trial_file in results_dir.glob("trial_*.json"):
        with open(trial_file, 'r') as f:
            trial_data = json.load(f)
            trials.append(trial_data)
    
    return trials


def rescore_trials(trials: List[Dict], 
                   ground_truth: str) -> pd.DataFrame:
    """
    Re-score all trials with corrected DQ formula.
    
    Args:
        trials: List of trial result dictionaries
        ground_truth: Known correct resolution for the incident
    
    Returns:
        DataFrame with original and re-scored metrics
    """
    scorer = DQScorer(ground_truth)
    
    rescored_data = []
    
    for trial in trials:
        trial_id = trial['trial_id']
        condition = trial['condition']
        
        # Original metrics
        original_t2u = trial.get('t2u', 0)
        original_dq = trial.get('dq', 0)
        
        # Extract actions from trial output
        actions = trial.get('actions', [])
        
        # Re-score with corrected formula
        scores = scorer.score_trial(actions)
        
        rescored_data.append({
            'trial_id': trial_id,
            'condition': condition,
            
            # Original metrics (for comparison)
            'original_dq': original_dq,
            
            # Re-scored metrics
            't2u': original_t2u,  # T2U measurement unchanged
            'dq': scores['dq'],
            'validity': scores['validity'],
            'specificity': scores['specificity'],
            'correctness': scores['correctness'],
            'action_count': scores['action_count'],
            
            # Change delta
            'dq_change': scores['dq'] - original_dq
        })
    
    return pd.DataFrame(rescored_data)


def generate_comparison_report(df: pd.DataFrame, output_path: Path):
    """Generate report comparing original vs. re-scored metrics."""
    
    report = ["# Re-scoring Analysis Report\n"]
    report.append("## Summary of Changes\n")
    
    # Overall statistics
    report.append(f"Total trials re-scored: {len(df)}\n")
    report.append(f"Mean DQ change: {df['dq_change'].mean():.4f}")
    report.append(f"Std DQ change: {df['dq_change'].std():.4f}")
    report.append(f"Max positive change: {df['dq_change'].max():.4f}")
    report.append(f"Max negative change: {df['dq_change'].min():.4f}\n")
    
    # Per-condition comparison
    report.append("## Condition-Level Comparison\n")
    
    for condition in sorted(df['condition'].unique()):
        cond_df = df[df['condition'] == condition]
        
        report.append(f"### {condition}")
        report.append(f"- Trials: {len(cond_df)}")
        report.append(f"- Original DQ: {cond_df['original_dq'].mean():.4f} ± {cond_df['original_dq'].std():.4f}")
        report.append(f"- Re-scored DQ: {cond_df['dq'].mean():.4f} ± {cond_df['dq'].std():.4f}")
        report.append(f"- Mean change: {cond_df['dq_change'].mean():.4f}")
        report.append("")
    
    # Component breakdown
    report.append("## Re-scored DQ Components\n")
    
    component_summary = df.groupby('condition').agg({
        'validity': ['mean', 'std'],
        'specificity': ['mean', 'std'],
        'correctness': ['mean', 'std'],
        'action_count': ['mean', 'std']
    }).round(4)
    
    report.append(component_summary.to_markdown())
    report.append("")
    
    # Save report
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"✓ Comparison report saved to {output_path}")


def main():
    """Main re-scoring pipeline."""
    
    # Configuration
    results_dir = Path("results/trials")
    output_dir = Path("results/rescored")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Ground truth for auth service incident
    ground_truth = "rollback auth-service deployment to v2.3.0 verify database connection pool"
    
    print("Loading trial results...")
    trials = load_trial_results(results_dir)
    print(f"✓ Loaded {len(trials)} trials")
    
    print("\nRe-scoring with corrected DQ formula...")
    rescored_df = rescore_trials(trials, ground_truth)
    print(f"✓ Re-scored {len(rescored_df)} trials")
    
    # Save re-scored data
    rescored_df.to_csv(output_dir / "rescored_metrics.csv", index=False)
    print(f"✓ Saved to {output_dir / 'rescored_metrics.csv'}")
    
    # Generate comparison report
    generate_comparison_report(rescored_df, output_dir / "rescoring_report.md")
    
    # Run statistical analysis on re-scored data
    print("\nRunning statistical analysis...")
    analyzer = StatisticalAnalyzer(alpha=0.05)
    
    # T2U analysis
    anova_t2u = analyzer.one_way_anova(rescored_df, 't2u')
    pairwise_t2u = analyzer.pairwise_ttests(rescored_df, 't2u')
    
    # DQ analysis
    anova_dq = analyzer.one_way_anova(rescored_df, 'dq')
    pairwise_dq = analyzer.pairwise_ttests(rescored_df, 'dq')
    
    # Save statistical report
    with open(output_dir / "statistical_analysis.md", 'w') as f:
        f.write(analyzer.generate_report())
    print(f"✓ Statistical report saved to {output_dir / 'statistical_analysis.md'}")
    
    # Generate updated summary table
    summary = analyzer.condition_summary(rescored_df, 't2u')
    summary.to_csv(output_dir / "summary_t2u.csv", index=False)
    
    summary_dq = analyzer.condition_summary(rescored_df, 'dq')
    summary_dq.to_csv(output_dir / "summary_dq.csv", index=False)
    
    print("\n✅ Re-scoring complete!")
    print(f"\nOutputs saved to: {output_dir}")
    print("  - rescored_metrics.csv")
    print("  - rescoring_report.md")
    print("  - statistical_analysis.md")
    print("  - summary_t2u.csv")
    print("  - summary_dq.csv")


if __name__ == "__main__":
    main()