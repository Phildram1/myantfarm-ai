# Changelog

All notable changes to MyAntFarm.ai will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [v2] - 2026-01-07

### Added
- Comprehensive threats to validity analysis (Section V.J)
- Reproducibility notes section with hardware requirements and common issues (Section VII)
- Clarification on "agent" definition to distinguish from autonomous agent frameworks
- Practical implications subsection for AIOps tool builders (Section V.E)
- Prompt engineering confound discussion (Section V.G.6)

### Changed
- Expanded limitations section with deeper analysis of each constraint
- Updated all model references to latest versions (GPT-5.2, Claude Sonnet 4.5, Llama 3.3 70B)
- Updated Phase 2 timeline with current experiment status
- Enhanced Future Work section with concrete timelines and status indicators

### Fixed
- Regex pattern formatting to prevent column overflow
- Model name consistency throughout the paper

### Documentation
- Added version update notes box at top of paper
- Improved abstract with production-readiness framing
- Added "Scope and Limitations" paragraph in introduction

**Paper**: [arXiv:2511.15755v2](https://arxiv.org/abs/2511.15755v2)

---

## [v1] - 2025-11-19

### Added
- Initial release with 348-trial evaluation
- Decision Quality (DQ) metric framework
- Reproducible Docker-based experimental framework
- Single-agent vs multi-agent comparison
- Statistical validation with ANOVA and pairwise t-tests
- Complete source code and trial data

### Core Findings
- 100% actionable recommendation rate (multi-agent) vs 1.7% (single-agent)
- 80× improvement in action specificity
- 140× improvement in solution correctness
- Zero quality variance in multi-agent systems

**Paper**: [arXiv:2511.15755v1](https://arxiv.org/abs/2511.15755v1)

---

## Experimental Results

**No changes to experimental results between v1 and v2.** Version 2 updates focus on:
- Clarifications and additional context
- Expanded discussion of limitations
- Updated future work timeline
- Current model references

The core findings (100% actionability, 80× specificity, 140× correctness) remain unchanged.
