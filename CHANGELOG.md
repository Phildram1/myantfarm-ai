# Changelog

All notable changes to MyAntFarm.ai will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-05

### Major Changes - Quality-Focused Reframing

This release fundamentally reframes the project from speed-focused to quality-focused based on empirical findings.

### Added

- **Decision Quality (DQ) metric v2.0**: Multi-dimensional scoring (Validity, Specificity, Correctness)
- **Determinism analysis**: Zero-variance quality in multi-agent systems
- **Outlier removal pipeline**: Automated cleaning of catastrophic failures
- **Component breakdown analysis**: Detailed specificity and correctness metrics
- **Actionability thresholds**: DQ > 0.5 definition with distribution analysis
- **LaTeX paper**: Complete IEEE-format paper with revised findings
- **Stability visualization**: 4 publication-quality plots
- **Complete documentation**: Metrics specification, contributing guide, API docs
- **CI/CD pipeline**: GitHub Actions for automated testing

### Changed

- **Primary contribution**: From "58% latency reduction" to "100% actionability rate vs. 1.7%"
- **Paper title**: From latency-focused to quality-focused
- **Evaluation focus**: From T₂U to DQ as primary metric
- **Architectural value**: From speed optimization to production-readiness requirement

### Key Findings (New)

- Multi-agent achieves 100% actionable recommendations vs. 1.7% for single-agent
- 81× improvement in action specificity
- 126× improvement in solution correctness
- Zero quality variance (DQ Std ≈ 0) enables SLA commitments
- Speed parity after outlier removal (40.31s vs. 41.61s, 3.2% difference)

### Fixed

- DQ formula: Corrected from multiplicative context weight to additive components
- Statistical tests: Now actually executed (not hypothetical)
- C1 timing transparency: Clearly labeled as simulated baseline
- Unicode handling in LaTeX export

### Deprecated

- Speed-focused messaging in paper abstract and title
- Variance ratio as primary metric (replaced with quality distribution)

## [1.0.0] - 2025-11-01

### Initial Release

- Basic simulation framework with C1/C2/C3 conditions
- Original DQ formula (flawed)
- Preliminary T₂U measurements
- Docker-based evaluation stack
- TinyLlama (1B) backend

---

## Roadmap

### [2.1.0] - Planned Q1 2026

- [ ] Multiple incident scenarios (database, network, CDN)
- [ ] Human validation study (n=10-15 SRE experts)
- [ ] Inter-rater reliability analysis
- [ ] Larger model evaluation (Llama 3.1 70B)

### [3.0.0] - Planned Q2 2026

- [ ] RAG integration with historical incidents
- [ ] MCP connectors for live telemetry
- [ ] Production deployment guide
- [ ] Longitudinal evaluation over weeks

---

**Version**: 2.0.0 (Quality-Focused)  
**Date**: November 5, 2025  
**Author**: Philip Drammeh