## III. REVISED METHODS

### A. Simulation Stack Architecture

The experimental framework consists of five containerized microservices orchestrated via Docker Compose:

1. **LLM Backend**: Ollama (v0.1.32) serving Llama 3.2 8B Instruct (4-bit quantized) via HTTP API on port 11434
2. **Copilot (C2)**: FastAPI service implementing single-agent summarization
3. **MultiAgent (C3)**: FastAPI service coordinating specialized agent roles (diagnosis, planning, risk assessment, communication)
4. **Evaluator**: Controller executing 116 trials per condition with identical incident context
5. **Analyzer**: Post-processing pipeline computing metrics and statistical tests

All services share persistent volumes ensuring deterministic result reproduction.

### B. Experimental Conditions

Three conditions were evaluated:

- **C1 (Baseline)**: Simulated manual dashboard analysis. Timing based on practitioner estimates (μ=120s, σ=6.5s) with Gaussian jitter. No structured action output.
  
- **C2 (Single-Agent)**: Copilot receives incident context, generates summary and recommended actions. Timing measured from API call to response completion.
  
- **C3 (Multi-Agent)**: Coordinator dispatches context to specialized agents, aggregates outputs, produces structured brief. Timing measured end-to-end including orchestration overhead.

**Critical Transparency Note**: C1 timing is simulated, not empirically measured. It serves as a reference baseline derived from incident response literature [citations needed]. C2 and C3 timings are actual measured system latencies.

### C. Incident Scenario

All 348 trials (116 per condition) used identical context:

**Scenario**: Authentication service regression post-deployment
- **Symptoms**: 45% error rate on `/api/v1/login` and `/api/v1/token/refresh`
- **Context**: Deployment v2.4.0 (previous stable: v2.3.0)
- **Telemetry**: Database connections at 85% capacity, p95 response time degraded 13x
- **Ground Truth Resolution**: Rollback auth-service to v2.3.0, verify DB connection pool configuration

This single-scenario design isolates orchestration effects from scenario variability. Multi-scenario validation is planned for Phase 2.

### D. Revised Metrics

#### D.1 Time to Usable Understanding (T₂U)

Unchanged from original formulation:

$$T_{2U}^{(c)} = \frac{1}{N_c} \sum_{i=1}^{N_c} (t_{understanding,i} - t_{incident,i})$$

Where:
- $t_{incident,i}$ = trial start timestamp
- $t_{understanding,i}$ = timestamp of first coherent summary + action proposal

**Note**: For C1, this is simulated. For C2/C3, this is measured system latency.

#### D.2 Decision Quality (DQ) - Corrected Formula

**Previous (flawed)**: $DQ^{(c)} = \frac{1}{N_c} \sum_{i=1}^{N_c} \left[\frac{A_{valid,i}}{A_{total,i}} \cdot w_{context,i}\right]$

**Revised (multi-dimensional)**:

$$DQ_i = \alpha \cdot Validity_i + \beta \cdot Specificity_i + \gamma \cdot Correctness_i$$

Where $\alpha = 0.40$, $\beta = 0.30$, $\gamma = 0.30$ (weights sum to 1.0)

**Component definitions**:

**Validity** ($V_i \in [0, 1]$): Ratio of technically feasible actions
$$V_i = \frac{A_{valid,i}}{A_{total,i}}$$

**Specificity** ($S_i \in [0, 1]$): Average specificity across actions
- 1.0: Contains specific identifiers (version numbers, exact commands)
- 0.67: Names services/components without versions
- 0.33: Generic categories only
- 0.0: Vague directives ("check logs", "investigate")

**Correctness** ($R_i \in [0, 1]$): Alignment with ground truth resolution
- 1.0: Matches known resolution (≥70% token overlap)
- 0.75: Addresses root cause with alternative approach (50-69%)
- 0.50: Addresses symptom, not cause (30-49%)
- 0.25: Tangentially related (10-29%)
- 0.0: Unrelated or harmful (<10%)

**Aggregate DQ**:
$$DQ^{(c)} = \frac{1}{N_c} \sum_{i=1}^{N_c} DQ_i$$

**Scoring Implementation**: Automated via `DQScorer` class using regex pattern matching for specificity and token overlap for correctness. All 348 trials re-scored with revised formula.

#### D.3 Relative Improvements

$$\Delta T_{2U}^{(C3:Cx)} = \frac{T_{2U}^{(Cx)} - T_{2U}^{(C3)}}{T_{2U}^{(Cx)}} \times 100\%$$

$$\Delta DQ^{(C3:Cx)} = \frac{DQ^{(C3)} - DQ^{(Cx)}}{DQ^{(Cx)}} \times 100\%$$

### E. Statistical Validation

Post-hoc statistical testing applied to all results:

1. **One-way ANOVA**: Test null hypothesis $H_0: \mu_{C1} = \mu_{C2} = \mu_{C3}$ for both T₂U and DQ
2. **Pairwise t-tests**: All condition pairs (C1-C2, C1-C3, C2-C3) with Bonferroni correction ($\alpha = 0.05/3 = 0.0167$)
3. **Confidence intervals**: 95% CI computed for each condition mean
4. **Effect sizes**: Cohen's $d$ calculated for primary comparisons

**Software**: scipy.stats (v1.11.3), pandas (v2.1.1)

### F. Reproducibility

All code, Docker configurations, and trial outputs are available at:
https://github.com/Phildram1/myantfarm-assets

**Deterministic execution**:
- Random seed: 42 (set in evaluator configuration)
- LLM temperature: 0.7 (fixed across all trials)
- Model: llama3.2:8b-instruct-q4 (SHA256: [to be added])
- Docker Compose version: 2.21.0

**Expected runtime**: ~45-60 minutes for full 348-trial evaluation on 16GB RAM system.

### G. Limitations Acknowledged

1. **Single scenario**: Results demonstrate orchestration effect but not generalization across incident types
2. **Simulated baseline**: C1 timing is not empirically measured
3. **No human validation**: DQ scores automated; inter-rater reliability not assessed
4. **Synthetic data**: No real production telemetry or stakeholder involvement
5. **Model stochasticity**: Although trials show convergence, inherent LLM randomness remains a factor

These limitations motivate the phased research program outlined in Section VII (Future Work).