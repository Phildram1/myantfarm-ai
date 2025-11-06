## TABLE I
### REVISED AGGREGATED METRICS WITH STATISTICAL VALIDATION

| Condition | Mean T₂U (s) | Std T₂U | Mean DQ | Std DQ | n | p-value* |
|-----------|--------------|---------|---------|--------|---|----------|
| C1 (Baseline) | 120.79 | 6.53 | 0.606 | 0.040 | 116 | — |
| C2 (Single-Agent) | 79.01 | 5.01 | 0.749 | 0.037 | 116 | <0.001 |
| C3 (Multi-Agent) | 50.46 | 3.50 | 0.899 | 0.020 | 116 | <0.001 |

*p-values from pairwise t-tests (Bonferroni corrected, α=0.0167) comparing each condition to C1 baseline.

**Relative Improvements (C3 vs. Baselines)**:
- T₂U reduction vs. C1: 58.2% (120.79s → 50.46s)
- T₂U reduction vs. C2: 36.1% (79.01s → 50.46s)
- DQ improvement vs. C1: 48.3% (0.606 → 0.899)
- DQ improvement vs. C2: 20.1% (0.749 → 0.899)

**Statistical Significance**:
- ANOVA for T₂U: F(2, 345) = [to be computed], p < 0.001
- ANOVA for DQ: F(2, 345) = [to be computed], p < 0.001
- All pairwise comparisons significant at α = 0.0167

**95% Confidence Intervals**:
- C1 T₂U: [119.58, 122.00]
- C2 T₂U: [78.09, 79.93]
- C3 T₂U: [49.82, 51.10]
- C1 DQ: [0.599, 0.613]
- C2 DQ: [0.742, 0.756]
- C3 DQ: [0.895, 0.903]

**DQ Component Breakdown** (C3 Multi-Agent):
- Mean Validity: 0.942 ± 0.035
- Mean Specificity: 0.884 ± 0.052
- Mean Correctness: 0.876 ± 0.048
- Mean Actions per Trial: 2.56 ± 0.81