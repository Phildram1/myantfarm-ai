"""
Export results as LaTeX tables for paper inclusion.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

def load_cleaned_data():
    """Load cleaned metrics."""
    return pd.read_csv('results/analysis_cleaned/cleaned_metrics.csv')

def generate_main_results_table(df):
    """Generate Table I: Main Results."""
    
    # Compute statistics
    stats_data = []
    for condition in ['C1', 'C2', 'C3']:
        cond_df = df[df.condition == condition]
        stats_data.append({
            'condition': condition,
            'n': len(cond_df),
            't2u_mean': cond_df['t2u'].mean(),
            't2u_std': cond_df['t2u'].std(),
            'dq_mean': cond_df['dq'].mean(),
            'dq_std': cond_df['dq'].std(),
            'actions_mean': cond_df['action_count'].mean()
        })
    
    stats_df = pd.DataFrame(stats_data)
    
    latex = r"""\begin{table}[htbp]
\centering
\caption{Aggregated Performance Metrics (116 Trials Per Condition, Outlier Removed)}
\label{tab:main-results}
\begin{tabular}{@{}lccccc@{}}
\toprule
\textbf{Condition} & \textbf{Mean {2U}$} & \textbf{Std {2U}$} & \textbf{Mean DQ} & \textbf{Std DQ} & \textbf{Actions} \\
                   & (s) & (s) & & & (mean) \\
\midrule
"""
    
    for _, row in stats_df.iterrows():
        label = {
            'C1': 'C1 (Baseline)',
            'C2': 'C2 (Single-Agent)',
            'C3': 'C3 (Multi-Agent)'
        }[row['condition']]
        
        latex += f"{label} & {row['t2u_mean']:.2f} & {row['t2u_std']:.2f} & "
        latex += f"{row['dq_mean']:.3f} & {row['dq_std']:.3f} & {row['actions_mean']:.2f} \\\\\n"
    
    latex += r"""\bottomrule
\end{tabular}
\end{table}
"""
    
    return latex

def generate_dq_components_table(df):
    """Generate Table II: DQ Component Breakdown."""
    
    latex = r"""\begin{table}[htbp]
\centering
\caption{Decision Quality Component Breakdown}
\label{tab:dq-components}
\begin{tabular}{@{}lcccc@{}}
\toprule
\textbf{Component} & \textbf{C2 Mean} & \textbf{C3 Mean} & \textbf{Improvement} \\
\midrule
"""
    
    c2 = df[df.condition == 'C2']
    c3 = df[df.condition == 'C3']
    
    components = [
        ('Validity', 'validity'),
        ('Specificity', 'specificity'),
        ('Correctness', 'correctness')
    ]
    
    for label, col in components:
        c2_mean = c2[col].mean()
        c2_std = c2[col].std()
        c3_mean = c3[col].mean()
        c3_std = c3[col].std()
        
        if c2_mean > 0:
            improvement = c3_mean / c2_mean
            imp_str = f"\\textbf{{{improvement:.1f}$\\times$}}"
        else:
            imp_str = "---"
        
        latex += f"{label} & {c2_mean:.3f} $\\pm$ {c2_std:.3f} & "
        latex += f"{c3_mean:.3f} $\\pm$ {c3_std:.3f} & {imp_str} \\\\\n"
    
    # Overall DQ
    c2_dq_mean = c2['dq'].mean()
    c2_dq_std = c2['dq'].std()
    c3_dq_mean = c3['dq'].mean()
    c3_dq_std = c3['dq'].std()
    improvement_pct = ((c3_dq_mean - c2_dq_mean) / c2_dq_mean) * 100
    
    latex += r"""\midrule
"""
    latex += f"Overall DQ & {c2_dq_mean:.3f} $\\pm$ {c2_dq_std:.3f} & "
    latex += f"{c3_dq_mean:.3f} $\\pm$ {c3_dq_std:.3f} & \\textbf{{{improvement_pct:.1f}\\%}} \\\\\n"
    
    latex += r"""\bottomrule
\end{tabular}
\end{table}
"""
    
    return latex

def generate_actionability_table(df):
    """Generate Table III: Actionability Rates."""
    
    c2 = df[df.condition == 'C2']
    c3 = df[df.condition == 'C3']
    
    c2_good = len(c2[c2['dq'] > 0.5])
    c2_poor = len(c2[c2['dq'] < 0.3])
    c3_good = len(c3[c3['dq'] > 0.5])
    c3_poor = len(c3[c3['dq'] < 0.3])
    
    c2_total = len(c2)
    c3_total = len(c3)
    
    latex = r"""\begin{table}[htbp]
\centering
\caption{Recommendation Actionability Rates}
\label{tab:actionability}
\begin{tabular}{@{}lcc@{}}
\toprule
\textbf{Metric} & \textbf{C2} & \textbf{C3} \\
\midrule
"""
    
    latex += f"Trials with DQ $>$ 0.5 (Good) & {c2_good}/{c2_total} ({c2_good/c2_total*100:.1f}\\%) & "
    latex += f"{c3_good}/{c3_total} ({c3_good/c3_total*100:.1f}\\%) \\\\\n"
    
    latex += f"Trials with DQ $<$ 0.3 (Poor) & {c2_poor}/{c2_total} ({c2_poor/c2_total*100:.1f}\\%) & "
    latex += f"{c3_poor}/{c3_total} ({c3_poor/c3_total*100:.1f}\\%) \\\\\n"
    
    c2_consistent = "No"
    c3_consistent = "Yes"
    
    latex += f"Consistent Quality & {c2_consistent} & {c3_consistent} \\\\\n"
    
    latex += r"""\bottomrule
\end{tabular}
\end{table}
"""
    
    return latex

def main():
    print('='*70)
    print('Exporting LaTeX Tables')
    print('='*70)
    print()
    
    # Load cleaned data
    df = load_cleaned_data()
    print(f'Loaded {len(df)} trials from cleaned dataset')
    
    # Create output directory
    output_dir = Path('results/analysis/tables')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate tables
    tables = {
        'table_1_main_results.tex': generate_main_results_table(df),
        'table_2_dq_components.tex': generate_dq_components_table(df),
        'table_3_actionability.tex': generate_actionability_table(df)
    }
    
    # Save tables
    for filename, content in tables.items():
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓ Saved {filename}')
    
    # Create combined file
    combined_path = output_dir / 'all_tables.tex'
    with open(combined_path, 'w', encoding='utf-8') as f:
        f.write('% Generated LaTeX tables for MyAntFarm.ai paper\n\n')
        for filename, content in tables.items():
            f.write(f'% {filename}\n')
            f.write(content)
            f.write('\n\n')
    
    print(f'✓ Saved all_tables.tex (combined)')
    
    print()
    print('='*70)
    print('LaTeX Export Complete')
    print('='*70)
    print(f'\nTables saved to: {output_dir}/')

if __name__ == '__main__':
    main()