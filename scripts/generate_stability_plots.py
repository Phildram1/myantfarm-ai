import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

def load_data(results_path, exclude_outliers=None):
    df = pd.read_csv(results_path / 'analysis_cleaned' / 'cleaned_metrics.csv')
    return df

def plot_variance_comparison(df, output_path):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    conditions = ['C1', 'C2', 'C3']
    colors = ['#e74c3c', '#3498db', '#2ecc71']
    
    data_to_plot = [df[df.condition == c]['t2u'].values for c in conditions]
    
    bp = ax.boxplot(data_to_plot, 
                    labels=['C1\n(Baseline)', 'C2\n(Single-Agent)', 'C3\n(Multi-Agent)'],
                    patch_artist=True,
                    widths=0.6)
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_ylabel('Time to Usable Understanding (seconds)', fontweight='bold')
    ax.set_xlabel('Condition', fontweight='bold')
    ax.set_title('T2U Variance Comparison', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path / 'variance_comparison_boxplot.png', dpi=300)
    plt.close()

def plot_dq_comparison(df, output_path):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    conditions = ['C2', 'C3']
    dq_means = [df[df.condition == c]['dq'].mean() for c in conditions]
    
    bars = ax.bar(conditions, dq_means, color=['#3498db', '#2ecc71'], alpha=0.7)
    
    ax.set_ylabel('Decision Quality', fontweight='bold')
    ax.set_xlabel('Condition', fontweight='bold')
    ax.set_title('Decision Quality Comparison', fontweight='bold')
    ax.set_ylim([0, 1.0])
    
    for bar, val in zip(bars, dq_means):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{val:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path / 'dq_comparison.png', dpi=300)
    plt.close()

def main():
    results_path = Path('results')
    output_path = results_path / 'analysis' / 'stability_plots'
    output_path.mkdir(parents=True, exist_ok=True)
    
    print('='*70)
    print('Generating Stability Analysis Plots')
    print('='*70)
    
    df = load_data(results_path)
    
    print('Creating plots...')
    plot_variance_comparison(df, output_path)
    print('✓ variance_comparison_boxplot.png')
    
    plot_dq_comparison(df, output_path)
    print('✓ dq_comparison.png')
    
    print()
    print('='*70)
    print('✅ All stability plots generated!')
    print('='*70)

if __name__ == '__main__':
    main()