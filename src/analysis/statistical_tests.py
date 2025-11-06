import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class StatisticalResult:
    metric_name: str
    test_type: str
    statistic: float
    p_value: float
    significant: bool
    alpha: float
    notes: str = ''


class StatisticalAnalyzer:
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
        self.results: List[StatisticalResult] = []
    
    def one_way_anova(self, data: pd.DataFrame, metric_col: str, condition_col: str = 'condition'):
        conditions = data[condition_col].unique()
        groups = [data[data[condition_col] == c][metric_col].values for c in conditions]
        
        f_stat, p_value = stats.f_oneway(*groups)
        
        result = StatisticalResult(
            metric_name=metric_col,
            test_type='One-Way ANOVA',
            statistic=f_stat,
            p_value=p_value,
            significant=(p_value < self.alpha),
            alpha=self.alpha,
            notes=f'Comparing {len(conditions)} conditions'
        )
        
        self.results.append(result)
        return result
    
    def pairwise_ttests(self, data: pd.DataFrame, metric_col: str, condition_col: str = 'condition', bonferroni: bool = True):
        from itertools import combinations
        
        conditions = sorted(data[condition_col].unique())
        n_comparisons = len(list(combinations(conditions, 2)))
        adjusted_alpha = self.alpha / n_comparisons if bonferroni else self.alpha
        
        pairwise_results = []
        
        for c1, c2 in combinations(conditions, 2):
            group1 = data[data[condition_col] == c1][metric_col].values
            group2 = data[data[condition_col] == c2][metric_col].values
            
            t_stat, p_value = stats.ttest_ind(group1, group2)
            
            result = StatisticalResult(
                metric_name=metric_col,
                test_type=f'Two-Sample t-test ({c1} vs {c2})',
                statistic=t_stat,
                p_value=p_value,
                significant=(p_value < adjusted_alpha),
                alpha=adjusted_alpha,
                notes=f'Bonferroni corrected'
            )
            
            pairwise_results.append(result)
            self.results.append(result)
        
        return pairwise_results
    
    def condition_summary(self, data: pd.DataFrame, metric_col: str, condition_col: str = 'condition'):
        conditions = sorted(data[condition_col].unique())
        
        summary_data = []
        for condition in conditions:
            values = data[data[condition_col] == condition][metric_col].values
            
            mean = np.mean(values)
            sem = stats.sem(values)
            ci = stats.t.interval(0.95, len(values) - 1, loc=mean, scale=sem)
            
            summary_data.append({
                'Condition': condition,
                'N': len(values),
                'Mean': mean,
                'Std': np.std(values, ddof=1),
                'CI_95_Lower': ci[0],
                'CI_95_Upper': ci[1],
                'Median': np.median(values),
                'Min': np.min(values),
                'Max': np.max(values)
            })
        
        return pd.DataFrame(summary_data)
    
    def generate_report(self) -> str:
        report = ['# Statistical Analysis Report\n']
        report.append(f'Significance level: α = {self.alpha}\n')
        
        for result in self.results:
            sig_symbol = '***' if result.significant else 'ns'
            report.append(f'## {result.test_type}')
            report.append(f'- Metric: {result.metric_name}')
            report.append(f'- Statistic: {result.statistic:.4f}')
            report.append(f'- p-value: {result.p_value:.6f} {sig_symbol}')
            report.append(f'- Significant: {result.significant}\n')
        
        return '\n'.join(report)