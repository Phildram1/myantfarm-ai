import pandas as pd
import json
from pathlib import Path

# Load cleaned data
df = pd.read_csv('results/analysis_cleaned/cleaned_metrics.csv')

print('=' * 70)
print('DECISION QUALITY (DQ) DEEP DIVE')
print('=' * 70)
print()

# Overall statistics
print('=== DQ Statistics (Cleaned Data) ===')
print()
for condition in ['C1', 'C2', 'C3']:
    cond_df = df[df.condition == condition]
    print(condition + ':')
    print('  Mean DQ:    ', round(cond_df['dq'].mean(), 4))
    print('  Std DQ:     ', round(cond_df['dq'].std(), 4))
    print('  Min DQ:     ', round(cond_df['dq'].min(), 4))
    print('  Max DQ:     ', round(cond_df['dq'].max(), 4))
    print('  Median DQ:  ', round(cond_df['dq'].median(), 4))
    print()

# Component breakdown
print('=== DQ Component Breakdown (C2 vs C3) ===')
print()

for condition in ['C2', 'C3']:
    cond_df = df[df.condition == condition]
    print(condition + ':')
    print('  Validity:   ', round(cond_df['validity'].mean(), 4), '+-', round(cond_df['validity'].std(), 4))
    print('  Specificity:', round(cond_df['specificity'].mean(), 4), '+-', round(cond_df['specificity'].std(), 4))
    print('  Correctness:', round(cond_df['correctness'].mean(), 4), '+-', round(cond_df['correctness'].std(), 4))
    print('  Actions:    ', round(cond_df['action_count'].mean(), 2), '+-', round(cond_df['action_count'].std(), 2))
    print()

# Improvement calculation
c2_dq = df[df.condition == 'C2']['dq'].mean()
c3_dq = df[df.condition == 'C3']['dq'].mean()
improvement = ((c3_dq - c2_dq) / c2_dq) * 100

print('=== C3 vs C2 Improvement ===')
print()
print('DQ Improvement:', round(improvement, 1), '%')
print('Absolute gain: ', round(c3_dq - c2_dq, 4), 'points')
print()

# Check how many C2 trials had poor DQ
c2_df = df[df.condition == 'C2']
poor_dq = len(c2_df[c2_df['dq'] < 0.3])
good_dq = len(c2_df[c2_df['dq'] > 0.5])

print('C2 DQ Distribution:')
print('  Poor quality (DQ < 0.3):', poor_dq, '/', len(c2_df), '(', round(poor_dq/len(c2_df)*100, 1), '%)')
print('  Good quality (DQ > 0.5):', good_dq, '/', len(c2_df), '(', round(good_dq/len(c2_df)*100, 1), '%)')
print()

# Check C3
c3_df = df[df.condition == 'C3']
poor_dq_c3 = len(c3_df[c3_df['dq'] < 0.3])
good_dq_c3 = len(c3_df[c3_df['dq'] > 0.5])

print('C3 DQ Distribution:')
print('  Poor quality (DQ < 0.3):', poor_dq_c3, '/', len(c3_df), '(', round(poor_dq_c3/len(c3_df)*100, 1), '%)')
print('  Good quality (DQ > 0.5):', good_dq_c3, '/', len(c3_df), '(', round(good_dq_c3/len(c3_df)*100, 1), '%)')
print()

# Sample a few trials to show quality difference
print('=== Sample Trials (First 3 of each) ===')
print()

print('C2 Samples:')
for idx, row in c2_df.head(3).iterrows():
    print('  Trial', row['trial_id'], ': DQ=', round(row['dq'], 3), 
          'Validity=', round(row['validity'], 2),
          'Specificity=', round(row['specificity'], 2),
          'Correctness=', round(row['correctness'], 2),
          'Actions=', int(row['action_count']))

print()
print('C3 Samples:')
for idx, row in c3_df.head(3).iterrows():
    print('  Trial', row['trial_id'], ': DQ=', round(row['dq'], 3),
          'Validity=', round(row['validity'], 2),
          'Specificity=', round(row['specificity'], 2),
          'Correctness=', round(row['correctness'], 2),
          'Actions=', int(row['action_count']))

print()
print('=' * 70)