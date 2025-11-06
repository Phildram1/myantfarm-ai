"""
Package checker - validates all required files are present.
"""

from pathlib import Path
import sys

REQUIRED_FILES = [
    'README.md',
    'LICENSE',
    'CONTRIBUTING.md',
    '.gitignore',
    'docker-compose.yml',
    'requirements.txt',
    'requirements-dev.txt',
    'paper/main.tex',
    'scripts/run_full_evaluation.py',
    'scripts/remove_outlier_and_reanalyze.py',
    'scripts/analyze_dq_detail.py',
    'scripts/generate_stability_plots.py',
    'scripts/export_latex_tables.py',
    'src/scoring/dq_scorer_v2.py',
    'src/analysis/statistical_tests.py',
    'services/copilot/Dockerfile',
    'services/copilot/main.py',
    'services/multiagent/Dockerfile',
    'services/multiagent/main.py',
    'services/evaluator/Dockerfile',
    'services/evaluator/run_evaluation.py',
    'services/analyzer/Dockerfile',
    'services/analyzer/analyze_results.py',
    'docs/metrics_specification.md',
    '.github/workflows/ci.yml'
]

def check_package():
    print('='*70)
    print('MyAntFarm.ai Package Validation')
    print('='*70)
    print()
    
    missing = []
    present = []
    
    for filepath in REQUIRED_FILES:
        path = Path(filepath)
        if path.exists():
            present.append(filepath)
        else:
            missing.append(filepath)
    
    print(f'Files present: {len(present)}/{len(REQUIRED_FILES)}')
    
    if missing:
        print()
        print('❌ Missing files:')
        for filepath in missing:
            print(f'   - {filepath}')
        print()
        print('Run setup scripts to create missing files.')
        return False
    else:
        print()
        print('✅ All required files present!')
        print()
        print('Package is ready for GitHub publication.')
        print()
        print('Next steps:')
        print('  1. git init')
        print('  2. git add .')
        print('  3. git commit -m "Initial commit: MyAntFarm.ai v2.0.0"')
        print('  4. git remote add origin https://github.com/Phildram1/myantfarm-ai')
        print('  5. git push -u origin main')
        return True

if __name__ == '__main__':
    success = check_package()
    sys.exit(0 if success else 1)