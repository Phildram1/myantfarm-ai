# Metrics Specification v2.0

Complete definition of evaluation metrics used in MyAntFarm.ai.

## Time to Usable Understanding (T₂U)

### Definition

Time elapsed from incident detection to generation of actionable output (summary + recommended actions).

\\\
T₂U = t_understanding - t_incident
\\\

### Measurement

- **C1 (Baseline)**: Simulated based on practitioner estimates (μ=120s, σ=6.5s)
- **C2 (Single-Agent)**: Measured from API call start to response completion
- **C3 (Multi-Agent)**: Measured from orchestration start to aggregated output completion

### Interpretation

- Lower T₂U indicates faster comprehension
- Measured in seconds
- Includes LLM inference + orchestration overhead (for C3)

---

## Decision Quality (DQ)

### Definition

Multi-dimensional score measuring actionability of generated recommendations.

\\\
DQ = 0.40 × Validity + 0.30 × Specificity + 0.30 × Correctness
\\\

### Components

#### 1. Validity (Weight: 0.40)

**Definition**: Ratio of technically feasible actions to total actions proposed.

\\\
Validity = A_valid / A_total
\\\

**Scoring Rules**:
- Actions are marked invalid if they contain:
  - Impossible values (e.g., "CPU at 500%")
  - Contradictory directives (e.g., "restart and rollback")
  - Syntactically malformed commands

**Examples**:
- ✅ Valid: \"Rollback auth-service to v2.3.0"\
- ❌ Invalid: \"Set memory usage to 300%"\

#### 2. Specificity (Weight: 0.30)

**Definition**: Presence of concrete identifiers enabling immediate execution.

**Scoring Scale** (per action):

| Score | Criteria | Example |
|-------|----------|---------|
| 1.0 | Version numbers + service/command | \"Rollback auth-service to v2.3.0 using kubectl"\ |
| 0.67 | Service/command without version | \"Rollback the authentication service"\ |
| 0.33 | Generic category only | \"Rollback recent deployment"\ |
| 0.0 | Vague directive | \"Investigate the issue"\ |

**Pattern Matching** (automated via regex):
- Version numbers: \?\d+\.\d+\.\d+\
- Commands: \kubectl|docker|systemctl|aws|gcloud\
- Services: \uth|payment|api|database\-specific names

**Final Score**: Average specificity across all actions in trial.

#### 3. Correctness (Weight: 0.30)

**Definition**: Alignment with ground truth incident resolution.

**Scoring Method**: Token overlap between action text and ground truth solution.

**Ground Truth Example**:
\\\
"rollback auth-service deployment to v2.3.0 verify database connection pool"
\\\

**Scoring Scale**:

| Overlap | Score | Interpretation |
|---------|-------|----------------|
| ≥70% | 1.0 | Matches known solution |
| 50-69% | 0.75 | Addresses root cause (alternative approach) |
| 30-49% | 0.50 | Addresses symptom, not cause |
| 10-29% | 0.25 | Tangentially related |
| <10% | 0.0 | Unrelated or harmful |

**Calculation**:
\\\python
ground_truth_tokens = set(ground_truth.lower().split())
action_tokens = set(action.lower().split())
overlap = len(ground_truth_tokens & action_tokens)
overlap_ratio = overlap / len(ground_truth_tokens)
\\\

**Final Score**: Average correctness across all actions in trial.

---

## Aggregate Metrics

### Condition-Level DQ

\\\
DQ^(c) = (1/N_c) × Σ DQ_i
\\\

Where:
- \N_c\ = number of trials in condition c
- \DQ_i\ = decision quality score for trial i

### Relative Improvement

\\\
ΔDQ(C3:C2) = [(DQ_C3 - DQ_C2) / DQ_C2] × 100%
\\\

---

## Example Calculations

### Trial Example: C2_045

**Actions Generated**:
1. \"Investigate recent changes"\
2. \"Review system metrics"\

**Scoring**:

| Component | Calculation | Score |
|-----------|-------------|-------|
| **Validity** | 2 valid / 2 total | 1.000 |
| **Specificity** | (0.0 + 0.0) / 2 | 0.000 |
| **Correctness** | (0.0 + 0.0) / 2 | 0.000 |
| **Overall DQ** | 0.40×1.0 + 0.30×0.0 + 0.30×0.0 | **0.400** |

**Interpretation**: Valid but vague actions with no ground truth alignment.

---

### Trial Example: C3_045

**Actions Generated**:
1. \"Rollback auth-service to v2.3.0 using kubectl rollout undo"\
2. \"Verify database connection pool max_connections setting"\
3. \"Monitor error rates for 5 minutes post-rollback"\

**Scoring**:

| Component | Calculation | Score |
|-----------|-------------|-------|
| **Validity** | 3 valid / 3 total | 1.000 |
| **Specificity** | (1.0 + 0.67 + 1.0) / 3 | 0.890 |
| **Correctness** | (1.0 + 1.0 + 0.25) / 3 | 0.750 |
| **Overall DQ** | 0.40×1.0 + 0.30×0.890 + 0.30×0.750 | **0.892** |

**Interpretation**: Highly actionable recommendations with strong ground truth alignment.

---

## Quality Thresholds

| DQ Range | Category | Actionability |
|----------|----------|---------------|
| 0.7 - 1.0 | **Excellent** | Immediately executable |
| 0.5 - 0.7 | **Good** | Actionable with minor clarification |
| 0.3 - 0.5 | **Mediocre** | Requires significant interpretation |
| 0.0 - 0.3 | **Poor** | Not actionable |

**Production Threshold**: DQ > 0.5 considered actionable for operator use.

---

## Implementation

See \src/scoring/dq_scorer_v2.py\ for automated scorer implementation.

### Usage Example

\\\python
from src.scoring.dq_scorer_v2 import DQScorer

ground_truth = "rollback auth-service to v2.3.0 verify database pool"
scorer = DQScorer(ground_truth)

actions = [
    "Rollback auth-service to v2.3.0",
    "Check database connection pool"
]

result = scorer.score_trial(actions)
print(result)
# {'validity': 1.0, 'specificity': 0.835, 'correctness': 0.75, 'dq': 0.876}
\\\

---

## Validation

### Inter-Rater Reliability (Planned Phase 2)

- 10-15 SRE practitioners rate 50 trials independently
- Krippendorff's α calculated for each component
- Target: α > 0.70 (acceptable agreement)

### Sensitivity Analysis

Varying component weights (α, β, γ) shows robust rank ordering:
- Primary driver: Specificity (distinguishes vague vs. concrete actions)
- Secondary: Correctness (ensures solution alignment)
- Baseline: Validity (eliminates nonsensical actions)

---

**Version**: 2.0  
**Last Updated**: November 2025  
**Contact**: philip.drammeh@gmail.com