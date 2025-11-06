import json
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import warnings

warnings.filterwarnings('ignore')

sys.path.append(str(Path(__file__).parent.parent))

from src.scoring.dq_scorer_v2 import DQScorer
from src.analysis.statistical_tests import StatisticalAnalyzer


def load_trials(results_dir, exclude_trials=None):
    results_file = results_dir / 'all_trials.json'
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    trials = data['trials']
    
    if exclude_trials:
        trials = [t for t in trials if t['trial_id'] not in exclude_trials]
    
    return trials


def create_cleaned_dataset(results_dir, outliers):
    print('=' * 70)
    print('Outlier Removal and Re-analysis')
    print('=' * 70)
    print('Excluding outliers:', outliers)
    print('=' * 70)
    print()
    
    trials = load_trials(results_dir, exclude_trials=outliers)
    print('Loaded', len(trials), 'trials (after exclusion)')
    print()
    
    print('Re-scoring trials with corrected DQ formula...')
    ground_truth = 'rollback auth-service deployment to v2.3.0 verify database connection pool'
    scorer = DQScorer(ground_truth)
    
    records = []
    for trial in trials:
        if trial.get('error'):
            continue
        
        actions = trial.get('actions', [])
        scores = scorer.score_trial(actions)
        
        records.append({
            'trial_id': trial['trial_id'],
            'condition': trial['condition'],
            't2u': trial['t2u'],
            'dq': scores['dq'],
            'validity': scores['validity'],
            'specificity': scores['specificity'],
            'correctness': scores['correctness'],
            'action_count': scores['action_count']
        })
    
    df = pd.DataFrame(records)
    print('Re-scored', len(df), 'trials')
    print()
    
    return df


def compare_with_and_without_outliers(results_dir, outliers):
    print()
    print('=== ORIGINAL DATA (with outliers) ===')
    print()
    
    trials_original = load_trials(results_dir, exclude_trials=None)
    ground_truth = 'rollback auth-service deployment to v2.3.0 verify database connection pool'
    scorer = DQScorer(ground_truth)
    
    records_orig = []
    for trial in trials_original:
        if trial.get('error'):
            continue
        actions = trial.get('actions', [])
        scores = scorer.score_trial(actions)
        records_orig.append({
            'condition': trial['condition'],
            't2u': trial['t2u'],
            'dq': scores['dq']
        })
    
    df_orig = pd.DataFrame(records_orig)
    
    orig_stats = df_orig.groupby('condition').agg({
        't2u': ['count', 'mean', 'std', 'min', 'max'],
        'dq': ['mean', 'std']
    }).round(2)
    
    print(orig_stats)
    
    print()
    print()
    print('=== CLEANED DATA (outliers removed) ===')
    print()
    
    df_clean = create_cleaned_dataset(results_dir, outliers)
    
    clean_stats = df_clean.groupby('condition').agg({
        't2u': ['count', 'mean', 'std', 'min', 'max'],
        'dq': ['mean', 'std']
    }).round(2)
    
    print(clean_stats)
    
    print()
    print()
    print('=== IMPACT OF OUTLIER REMOVAL ===')
    print()
    
    for condition in ['C1', 'C2', 'C3']:
        orig_c = df_orig[df_orig.condition == condition]
        clean_c = df_clean[df_clean.condition == condition]
        
        orig_mean = orig_c['t2u'].mean()
        clean_mean = clean_c['t2u'].mean()
        orig_std = orig_c['t2u'].std()
        clean_std = clean_c['t2u'].std()
        
        print(condition + ':')
        print('  Mean T2U:', round(orig_mean, 2), 's ->', round(clean_mean, 2), 's (change', round(clean_mean - orig_mean, 2), 's)')
        print('  Std T2U: ', round(orig_std, 2), 's ->', round(clean_std, 2), 's (change', round(clean_std - orig_std, 2), 's)')
        if orig_std > 0:
            print('  Reduction in variance:', round(((orig_std - clean_std) / orig_std * 100), 1), '%')
        print()
    
    c2_orig_std = df_orig[df_orig.condition == 'C2']['t2u'].std()
    c3_orig_std = df_orig[df_orig.condition == 'C3']['t2u'].std()
    variance_ratio_orig = c2_orig_std / c3_orig_std
    
    c2_clean_std = df_clean[df_clean.condition == 'C2']['t2u'].std()
    c3_clean_std = df_clean[df_clean.condition == 'C3']['t2u'].std()
    variance_ratio_clean = c2_clean_std / c3_clean_std
    
    print('C2/C3 Variance Ratio:')
    print('  Original:', round(variance_ratio_orig, 1), 'x')
    print('  Cleaned: ', round(variance_ratio_clean, 1), 'x')
    
    return df_clean


def save_cleaned_results(df, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(str(output_dir / 'cleaned_metrics.csv'), index=False, encoding='utf-8')
    print()
    print('Saved cleaned metrics to cleaned_metrics.csv')
    
    analyzer = StatisticalAnalyzer(alpha=0.05)
    
    try:
        analyzer.one_way_anova(df, 't2u')
        analyzer.pairwise_ttests(df, 't2u')
    except Exception as e:
        print('Warning: T2U statistical tests failed:', str(e))
    
    try:
        analyzer.one_way_anova(df, 'dq')
        analyzer.pairwise_ttests(df, 'dq')
    except Exception as e:
        print('Warning: DQ statistical tests failed:', str(e))
    
    # Generate report with ASCII only
    report = analyzer.generate_report()
    report_ascii = report.encode('ascii', errors='ignore').decode('ascii')
    
    with open(str(output_dir / 'statistical_analysis_cleaned.md'), 'w', encoding='utf-8') as f:
        f.write(report_ascii)
    
    print('Statistical report saved')
    
    summary_t2u = analyzer.condition_summary(df, 't2u')
    summary_t2u.to_csv(str(output_dir / 'summary_t2u_cleaned.csv'), index=False)
    
    summary_dq = analyzer.condition_summary(df, 'dq')
    summary_dq.to_csv(str(output_dir / 'summary_dq_cleaned.csv'), index=False)
    
    print('Summary statistics saved')


def main():
    results_dir = Path('results')
    output_dir = results_dir / 'analysis_cleaned'
    
    outliers = ['C2_028']
    
    df_clean = compare_with_and_without_outliers(results_dir, outliers)
    
    save_cleaned_results(df_clean, output_dir)
    
    print()
    print('=' * 70)
    print('ANALYSIS COMPLETE!')
    print('=' * 70)
    print()
    print('Cleaned data saved to: results/analysis_cleaned/')


if __name__ == '__main__':
    main()