import json
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.append('/app')

# Simple inline DQ scorer since we can't import from src
class SimpleDQScorer:
    def __init__(self, ground_truth):
        self.ground_truth = ground_truth.lower()
    
    def score_trial(self, actions):
        if not actions:
            return {
                'validity': 0.0,
                'specificity': 0.0,
                'correctness': 0.0,
                'dq': 0.0,
                'action_count': 0
            }
        
        # Validity: assume all are valid
        validity = 1.0
        
        # Specificity: check for version numbers, service names
        specificities = []
        for action in actions:
            action_lower = action.lower()
            score = 0.0
            if 'v2.' in action_lower or 'version' in action_lower:
                score = 1.0
            elif 'rollback' in action_lower or 'auth' in action_lower or 'database' in action_lower:
                score = 0.67
            elif 'deployment' in action_lower or 'service' in action_lower:
                score = 0.33
            specificities.append(score)
        
        specificity = sum(specificities) / len(specificities) if specificities else 0.0
        
        # Correctness: token overlap with ground truth
        correctness_scores = []
        gt_tokens = set(self.ground_truth.split())
        for action in actions:
            action_tokens = set(action.lower().split())
            overlap = len(gt_tokens & action_tokens)
            overlap_ratio = overlap / len(gt_tokens) if gt_tokens else 0
            
            if overlap_ratio >= 0.7:
                correctness_scores.append(1.0)
            elif overlap_ratio >= 0.5:
                correctness_scores.append(0.75)
            elif overlap_ratio >= 0.3:
                correctness_scores.append(0.50)
            elif overlap_ratio >= 0.1:
                correctness_scores.append(0.25)
            else:
                correctness_scores.append(0.0)
        
        correctness = sum(correctness_scores) / len(correctness_scores) if correctness_scores else 0.0
        
        # Combined DQ
        dq = 0.40 * validity + 0.30 * specificity + 0.30 * correctness
        
        return {
            'validity': round(validity, 4),
            'specificity': round(specificity, 4),
            'correctness': round(correctness, 4),
            'dq': round(dq, 4),
            'action_count': len(actions)
        }


def main():
    results_dir = Path("/app/results")
    
    print("=" * 70)
    print("MyAntFarm.ai Results Analysis")
    print("=" * 70)
    
    results_file = results_dir / "all_trials.json"
    if not results_file.exists():
        print(f"❌ Results file not found: {results_file}")
        print("Run evaluator first!")
        return
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    trials = data['trials']
    print(f"✓ Loaded {len(trials)} trials\n")
    
    print("Re-scoring trials with corrected DQ formula...")
    ground_truth = "rollback auth-service deployment to v2.3.0 verify database connection pool"
    scorer = SimpleDQScorer(ground_truth)
    
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
    print(f"✓ Re-scored {len(df)} trials\n")
    
    output_dir = results_dir / "analysis"
    output_dir.mkdir(exist_ok=True)
    
    df.to_csv(output_dir / "rescored_metrics.csv", index=False)
    print(f"✓ Saved rescored metrics\n")
    
    # Summary statistics
    print("Computing summary statistics...")
    
    summary_data = []
    for condition in ['C1', 'C2', 'C3']:
        cond_df = df[df.condition == condition]
        
        summary_data.append({
            'Condition': condition,
            'N': len(cond_df),
            'Mean_T2U': cond_df['t2u'].mean(),
            'Std_T2U': cond_df['t2u'].std(),
            'Mean_DQ': cond_df['dq'].mean(),
            'Std_DQ': cond_df['dq'].std(),
            'Mean_Actions': cond_df['action_count'].mean(),
            'Std_Actions': cond_df['action_count'].std()
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(output_dir / "summary_statistics.csv", index=False)
    
    print("\nSUMMARY STATISTICS:")
    print(summary_df.to_string(index=False))
    
    # Calculate improvements
    c1_t2u = summary_df[summary_df.Condition == 'C1']['Mean_T2U'].values[0]
    c3_t2u = summary_df[summary_df.Condition == 'C3']['Mean_T2U'].values[0]
    t2u_improvement = ((c1_t2u - c3_t2u) / c1_t2u) * 100
    
    c1_dq = summary_df[summary_df.Condition == 'C1']['Mean_DQ'].values[0]
    c3_dq = summary_df[summary_df.Condition == 'C3']['Mean_DQ'].values[0]
    dq_improvement = ((c3_dq - c1_dq) / c1_dq) * 100
    
    print(f"\nIMPROVEMENTS (C3 vs C1):")
    print(f"  T2U reduction: {t2u_improvement:.1f}%")
    print(f"  DQ improvement: {dq_improvement:.1f}%")
    
    print("\n" + "=" * 70)
    print("✅ Analysis Complete!")
    print("=" * 70)
    print(f"\nOutputs saved to: {output_dir}")


if __name__ == "__main__":
    main()
