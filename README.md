# MyAntFarm.ai - Multi-Agent LLM Orchestration for Incident Response

[![arXiv](https://img.shields.io/badge/arXiv-2511.15755-b31b1b.svg)](https://arxiv.org/abs/2511.15755)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Publication**: "Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response"  
**Author**: Philip Drammeh, M.Eng.  
**arXiv**: [2511.15755v2](https://arxiv.org/abs/2511.15755v2)

## Overview

MyAntFarm.ai is a reproducible experimental framework demonstrating that multi-agent LLM orchestration achieves **100% actionable recommendation quality** compared to 1.7% for single-agent approaches in incident response scenarios.

### Key Findings

- **100% actionability** (multi-agent) vs 1.7% (single-agent)
- **80× improvement** in action specificity
- **140× improvement** in solution correctness
- **Zero quality variance** across all trials (production-ready)
- **Similar latency** (~40s) - quality, not speed, is the differentiator

## What's New in v2 (January 2026)

**Version 2 updates** (no changes to experimental results):
- ✅ Expanded limitations section with deeper analysis
- ✅ Added comprehensive threats to validity analysis
- ✅ Clarified "agent" definition (vs autonomous agent frameworks)
- ✅ Added reproducibility notes for researchers
- ✅ Updated Phase 2 timeline with current status (experiments in progress)
- ✅ Updated model references to latest versions (GPT-5.2, Claude Sonnet 4.5, Llama 3.3 70B)
- ✅ Strengthened practical implications for AIOps tool builders

## Quick Start

### Prerequisites
- Docker and Docker Compose
- 16GB RAM minimum (32GB recommended)
- 4-core CPU
- No GPU required (TinyLlama runs efficiently on CPU)

### Installation

```bash
git clone https://github.com/Phildram1/myantfarm-ai.git
cd myantfarm-ai
docker-compose up -d
```

### Run Evaluation

```bash
# Full 348-trial evaluation (25-30 minutes)
python src/evaluator/run_trials.py

# Analyze results
python src/analysis/statistical_tests.py
```

## Architecture

MyAntFarm.ai consists of five containerized microservices:

1. **LLM Backend**: Ollama (v0.1.32) serving TinyLlama (1B parameters, 4-bit quantized)
2. **Copilot (C2)**: Single-agent summarization
3. **MultiAgent (C3)**: Coordinator dispatching to specialized agents:
   - Diagnosis Specialist
   - Remediation Planner
   - Risk Assessor
4. **Evaluator**: Controller executing trials with rate limiting
5. **Analyzer**: Statistical analysis pipeline

## Decision Quality (DQ) Metric

Novel evaluation framework measuring:
- **Validity** (40%): Technical feasibility
- **Specificity** (30%): Presence of concrete identifiers (versions, commands)
- **Correctness** (30%): Alignment with ground truth solutions

**Actionability threshold**: DQ > 0.5

## Reproducibility

All experiments are fully deterministic:
- Random seed: 42
- LLM temperature: 0.7
- Model: TinyLlama 1.1B (4-bit quantization)
- Expected runtime: 25-30 minutes on 16GB RAM system

### Common Issues

1. **Ollama connection errors**: Ensure service running on port 11434
2. **Docker network conflicts**: Use `docker-compose down -v` to reset
3. **Memory exhaustion**: Reduce concurrent trials in evaluator config

## Results Summary

| Condition | Mean T2U (s) | Mean DQ | Actionable Rate |
|-----------|--------------|---------|-----------------|
| C1 (Baseline) | 120.39 | 0.000 | N/A |
| C2 (Single-Agent) | 41.61 | 0.403 | 1.7% |
| C3 (Multi-Agent) | 40.31 | **0.692** | **100%** |

**Statistical significance**: All comparisons p < 0.001, Cohen's d > 18

## Phase 2 Status (Q1-Q2 2026)

Currently in progress:
- ✅ **Multi-scenario validation**: 5 diverse incident types
- ✅ **Model scaling study**: Llama 3.3 70B, GPT-5.2, Claude Sonnet 4.5
- 🔄 **Human validation study**: 10-15 SRE practitioners (recruitment underway)
- 📅 **RAG integration**: Q2 2026
- 📅 **MCP integration**: Q2 2026

## Citation

```bibtex
@article{drammeh2025multiagent,
  title={Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response},
  author={Drammeh, Philip},
  journal={arXiv preprint arXiv:2511.15755},
  year={2025}
}
```

## Project Structure

```
myantfarm-ai/
├── src/
│   ├── llm_backend/      # Ollama service
│   ├── copilot/          # Single-agent (C2)
│   ├── multiagent/       # Multi-agent orchestrator (C3)
│   ├── evaluator/        # Trial controller
│   ├── analyzer/         # Statistical analysis
│   └── scoring/          # DQ scorer implementation
├── docker-compose.yml
├── data/
│   ├── scenarios/        # Incident scenarios
│   └── results/          # Trial outputs
├── paper/
│   ├── paper_v2.pdf      # Latest arXiv version
│   └── references.bib    # Bibliography
└── README.md
```

## Practical Applications

1. **Incident Response Automation**: Deploy in shadow mode alongside human operators
2. **Runbook Generation**: Generate version-specific remediation steps
3. **Junior Engineer Onboarding**: Teaching tool validated by senior engineers
4. **Decision Support**: Human-in-the-loop recommendations with confidence scores

## Deployment Checklist

Before production use:
- [ ] Validate on 3-5 incident types from your domain
- [ ] Conduct human evaluation with 5-10 SRE practitioners
- [ ] Test with your LLM backend (GPT-5.2, Claude Sonnet 4.5, Llama 3.3 70B)
- [ ] Integrate with observability platform (Datadog, Splunk, Prometheus)
- [ ] Define rollback criteria (e.g., DQ < 0.5 → escalate to human)

## License

MIT License - see LICENSE file for details

## Contact

**Philip Drammeh**  
Email: philip.drammeh@gmail.com  
GitHub: [@Phildram1](https://github.com/Phildram1)

For reproduction support or questions about the research, please open an issue or email directly.

## Acknowledgments

Thanks to the open-source communities behind:
- Ollama
- TinyLlama
- Python/Docker ecosystems
- SRE practitioners who provided domain insights

---

**Research conducted independently without institutional affiliation or funding.**
