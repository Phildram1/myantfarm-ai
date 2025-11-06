import re
from typing import List, Dict


class DQScorer:
    def __init__(self, ground_truth: str):
        self.ground_truth = ground_truth.lower()
        self.alpha = 0.40
        self.beta = 0.30
        self.gamma = 0.30
    
    def score_trial(self, actions: List[str]) -> Dict[str, float]:
        if not actions:
            return {
                'validity': 0.0,
                'specificity': 0.0,
                'correctness': 0.0,
                'dq': 0.0,
                'action_count': 0
            }
        
        validity = 1.0
        
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
        
        dq = self.alpha * validity + self.beta * specificity + self.gamma * correctness
        
        return {
            'validity': round(validity, 4),
            'specificity': round(specificity, 4),
            'correctness': round(correctness, 4),
            'dq': round(dq, 4),
            'action_count': len(actions)
        }