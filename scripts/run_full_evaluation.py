"""
Complete evaluation pipeline runner.
Coordinates all evaluation steps and generates final reports.
"""

import subprocess
import sys
from pathlib import Path
import time

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f'\n{"="*70}')
    print(f'{description}')
    print(f'{"="*70}\n')
    
    result = subprocess.run(cmd, shell=True, capture_output=False)
    
    if result.returncode != 0:
        print(f'\n❌ Error in: {description}')
        sys.exit(1)
    
    print(f'\n✓ {description} completed successfully\n')

def main():
    start_time = time.time()
    
    print('\n' + '='*70)
    print('MyAntFarm.ai Complete Evaluation Pipeline')
    print('='*70)
    
    # Step 1: Run outlier analysis
    run_command(
        'python scripts/remove_outlier_and_reanalyze.py',
        'Step 1: Outlier Removal and Statistical Analysis'
    )
    
    # Step 2: DQ detailed analysis
    run_command(
        'python scripts/analyze_dq_detail.py',
        'Step 2: Decision Quality Component Analysis'
    )
    
    # Step 3: Generate plots
    run_command(
        'python scripts/generate_stability_plots.py',
        'Step 3: Stability Visualization'
    )
    
    # Step 4: Generate LaTeX tables
    run_command(
        'python scripts/export_latex_tables.py',
        'Step 4: LaTeX Table Export'
    )
    
    elapsed = time.time() - start_time
    
    print('\n' + '='*70)
    print('✅ COMPLETE EVALUATION PIPELINE FINISHED')
    print('='*70)
    print(f'\nTotal time: {elapsed/60:.1f} minutes')
    print('\nGenerated outputs:')
    print('  - results/analysis_cleaned/          (cleaned metrics and stats)')
    print('  - results/analysis/stability_plots/  (publication figures)')
    print('  - results/analysis/tables/           (LaTeX tables)')
    print('\nNext steps:')
    print('  1. Review results in results/analysis_cleaned/summary_*_cleaned.csv')
    print('  2. View plots in results/analysis/stability_plots/')
    print('  3. Compile paper with: cd paper && pdflatex main.tex')

if __name__ == '__main__':
    main()