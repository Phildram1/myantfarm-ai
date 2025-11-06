# MyAntFarm.ai: Multi-Agent Orchestration for High-Quality Incident Response

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://www.docker.com/)

> **Reproducible framework demonstrating that multi-agent LLM orchestration achieves 100% actionable recommendation quality compared to 1.7% for single-agent systems, with 81× improvement in specificity and 126× improvement in correctness.**

## 📄 Paper

**Title**: Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response

**Authors**: Philip Drammeh, M.Eng.

**Abstract**: This study demonstrates that multi-agent orchestration fundamentally transforms LLM-based incident response from generating vague suggestions to producing specific, actionable recommendations. Through 348 controlled trials, we show that multi-agent systems achieve 100% actionable recommendation quality (DQ > 0.5) compared to 1.7% for single-agent approaches, with 81× higher specificity and 126× higher correctness. Critically, multi-agent systems exhibit zero quality variance, making them production-ready, while single-agent systems produce inconsistent, largely unusable outputs.

**Key Findings**:
- ✅ **100% vs 1.7%** actionable recommendation rate
- ✅ **81× improvement** in action specificity  
- ✅ **126× improvement** in solution correctness
- ✅ **Zero quality variance** - deterministic, reliable outputs
- ✅ **71.7% overall DQ improvement** (0.692 vs 0.403)

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (with 10GB+ RAM allocation)
- Python 3.11+
- 20GB free disk space

### Run Complete Evaluation (30 minutes)

\\\ash
# Clone repository
git clone https://github.com/Phildram1/myantfarm-ai
cd myantfarm-ai

# Start Ollama and download model (~5GB, one-time)
docker-compose up -d ollama
sleep 60
docker exec myantfarm_ollama ollama pull tinyllama

# Run full evaluation (348 trials)
docker-compose up evaluator

# Analyze results
docker-compose up analyzer

# View results
cat results/analysis/summary_statistics.csv
\\\

### Expected Results

After completion, you should see:

\\\
Condition | Mean T2U | Std T2U | Mean DQ | Std DQ    | Actions
----------|----------|---------|---------|-----------|--------
C1        | 120.39s  | 5.92s   | 0.000   | 0.000     | 0.00
C2        | 41.61s   | 17.31s  | 0.403   | 0.023     | 2.01
C3        | 40.31s   | 17.32s  | 0.692   | 0.000     | 3.00
\\\

**Key takeaway**: C2 and C3 have similar speed (~40s), but C3 produces 71.7% higher quality recommendations with zero variance.

## 📊 Results Summary

### Decision Quality Component Breakdown

| Component | C2 (Single-Agent) | C3 (Multi-Agent) | Improvement |
|-----------|-------------------|------------------|-------------|
| **Validity** | 1.000 ± 0.000 | 1.000 ± 0.000 | ≈ |
| **Specificity** | 0.007 ± 0.052 | 0.557 ± 0.000 | **81.8×** ⬆️ |
| **Correctness** | 0.003 ± 0.026 | 0.417 ± 0.000 | **126.3×** ⬆️ |
| **Overall DQ** | 0.403 ± 0.023 | 0.692 ± 0.000 | **71.7%** ⬆️ |

### Quality Distribution

| Metric | C2 (Single-Agent) | C3 (Multi-Agent) |
|--------|-------------------|------------------|
| Trials with DQ > 0.5 (Good) | 2/115 (1.7%) | 116/116 (100%) |
| Trials with DQ < 0.3 (Poor) | 0/115 (0%) | 0/116 (0%) |
| Consistent Quality | ❌ No | ✅ Yes |

### Example Outputs

**C2 (Single-Agent) - Vague, Unusable:**
`
- "Investigate recent changes"
- "Review system metrics"
`

**C3 (Multi-Agent) - Specific, Actionable:**
`
- "Rollback auth-service to v2.3.0 using kubectl rollout undo"
- "Verify database connection pool max_connections setting"  
- "Monitor error rates for 5 minutes post-rollback"
`
## 🏗️ Architecture
``````
┌─────────────────────────────────────────────┐
│         Evaluator (Controller)              │
│  • Runs 116 trials per condition            │
│  • Measures T₂U and extracts actions        │
│  • Rate limits to prevent service overload  │
└────────────┬────────────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
┌─────▼─────┐  ┌────▼────────┐
│  Copilot  │  │ Multi-Agent │
│    (C2)   │  │    (C3)     │
│  Single   │  │  Diagnosis  │
│  Agent    │  │  Planner    │
│           │  │  Risk       │
└─────┬─────┘  └────┬────────┘
      │             │
      └──────┬──────┘
             │
      ┌──────▼──────┐
      │   Ollama    │
      │  TinyLlama  │
      │   (1B)      │
      └─────────────┘
``````

## 📁 Repository Structure
``````
myantfarm-ai/
├── paper/                      # LaTeX paper source
│   ├── main.tex
│   ├── sections/
│   ├── figures/
│   └── tables/
├── services/                   # Docker microservices
│   ├── copilot/               # C2: Single-agent
│   ├── multiagent/            # C3: Multi-agent
│   ├── evaluator/             # Trial controller
│   └── analyzer/              # Post-processing
├── src/                       # Python modules
│   ├── scoring/               # DQ scorer
│   ├── analysis/              # Statistical tests
│   └── evaluation/            # Trial orchestration
├── scripts/                   # Analysis scripts
├── results/                   # Generated results
├── docker-compose.yml
├── README.md
└── LICENSE
``````

## 🔬 Reproducing Results

### Step-by-Step Reproduction

1. **Environment Setup** (5 min)
   \\\bash
   docker-compose build
   docker-compose up -d ollama
   sleep 60
   docker exec myantfarm_ollama ollama pull tinyllama
   \\\

2. **Run Evaluation** (25-30 min)
   \\\bash
   docker-compose up evaluator
   \\\

3. **Analyze Results** (1 min)
   \\\bash
   docker-compose up analyzer
   python scripts/remove_outlier_and_reanalyze.py
   python scripts/analyze_dq_detail.py
   python scripts/generate_stability_plots.py
   \\\

4. **Verify Results** (1 min)
   \\\bash
   # Check summary statistics
   cat results/analysis_cleaned/summary_t2u_cleaned.csv
   cat results/analysis_cleaned/summary_dq_cleaned.csv
   
   # View plots
   open results/analysis/stability_plots/*.png
   \\\

### Configuration Options

Edit \docker-compose.yml\ to customize:

\\\yaml
environment:
  - TRIALS_PER_CONDITION=116    # Number of trials (default: 116)
  - RANDOM_SEED=42              # Reproducibility seed
  - MODEL_NAME=tinyllama        # LLM model
\\\

## 📊 Metrics Definition

### Time to Usable Understanding (T₂U)

\\\
T₂U = t_understanding - t_incident
\\\

Where:
- \	_incident\: Trial start timestamp
- \	_understanding\: First actionable output timestamp

### Decision Quality (DQ) - Multi-Dimensional

\\\
DQ = 0.40 × Validity + 0.30 × Specificity + 0.30 × Correctness
\\\

**Components**:
- **Validity** (0-1): Ratio of technically feasible actions
- **Specificity** (0-1): Presence of concrete identifiers (versions, commands, services)
- **Correctness** (0-1): Alignment with ground truth solution

See \docs/metrics_specification.md\ for detailed scoring rubric.

## 🧪 Testing

\\\ash
# Quick test (3 trials per condition, ~5 min)
TRIALS_PER_CONDITION=3 docker-compose up evaluator

# Unit tests
pytest tests/

# Verify DQ scorer
python src/scoring/dq_scorer_v2.py
\\\

## 📈 Analysis Scripts

### Outlier Removal Analysis
\\\ash
python scripts/remove_outlier_and_reanalyze.py
# Output: results/analysis_cleaned/
\\\

### DQ Component Breakdown
\\\ash
python scripts/analyze_dq_detail.py
# Shows specificity and correctness breakdown
\\\

### Stability Visualization
\\\ash
python scripts/generate_stability_plots.py
# Output: results/analysis/stability_plots/
\\\

## 🎓 Citation

If you use this work, please cite:

\\\ibtex
@article{drammeh2025myantfarm,
  title={Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response},
  author={Drammeh, Philip},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025}
}
\\\

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

- Additional incident scenarios (database outages, network issues)
- Human validation studies with SRE practitioners
- RAG integration for historical incident retrieval
- MCP connectors for live telemetry
- Larger models (Llama 3.1 70B, GPT-4)

See \CONTRIBUTING.md\ for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Ollama team for local LLM serving
- Meta AI for TinyLlama model
- Open-source Python/Docker communities

## 📞 Contact

**Author**: Philip Drammeh, M.Eng.  
**Email**: philip.drammeh@gmail.com  
**GitHub**: [@Phildram1](https://github.com/Phildram1)

## 🗺️ Roadmap

### Phase 1 (MVP - Complete) ✅
- Single scenario evaluation
- Automated DQ scoring
- Statistical validation
- Complete reproducibility

### Phase 2 (Planned - Q1 2026)
- 5+ diverse incident scenarios
- Human validation (n=10-15 SRE experts)
- Inter-rater reliability study
- Failure mode taxonomy

### Phase 3 (Future - Q2 2026)
- RAG with historical incidents
- MCP connectors for live telemetry  
- Production deployment guide
- Longitudinal evaluation

---

**Last Updated**: November 2025  
**Version**: 2.0.0 (Quality-Focused)
