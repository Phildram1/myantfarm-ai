# Paper - Multi-Agent LLM Orchestration for Incident Response

This directory contains the academic paper and supporting materials.

## Files

- `paper_v2.pdf` - Latest version (arXiv v2, January 2026)
- `paper_v2.tex` - LaTeX source for v2
- `references.bib` - Bibliography file
- `paper_v1.pdf` - Original version (arXiv v1, November 2025)

## Version History

### Version 2 (January 2026)
**arXiv**: [2511.15755v2](https://arxiv.org/abs/2511.15755v2)

**Changes from v1**:
- Expanded limitations section (Section V.G)
- Added threats to validity analysis (Section V.J)
- Clarified "agent" definition vs autonomous agent frameworks
- Added reproducibility notes (Section VII)
- Updated Phase 2 timeline with current status
- Updated model references (GPT-5.2, Claude Sonnet 4.5, Llama 3.3 70B)
- Strengthened practical implications for AIOps tool builders

**No changes to experimental results** - core findings remain identical.

### Version 1 (November 2025)
**arXiv**: [2511.15755v1](https://arxiv.org/abs/2511.15755v1)

**Original submission** with 348-trial evaluation demonstrating:
- 100% actionable recommendation rate (multi-agent) vs 1.7% (single-agent)
- 80× improvement in action specificity
- 140× improvement in solution correctness

## Citation

```bibtex
@article{drammeh2025multiagent,
  title={Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response},
  author={Drammeh, Philip},
  journal={arXiv preprint arXiv:2511.15755},
  year={2025}
}
```

## Building from Source

To compile the LaTeX source:

```bash
pdflatex paper_v2.tex
bibtex paper_v2
pdflatex paper_v2.tex
pdflatex paper_v2.tex
```

Or use the single-pass compilation:
```bash
pdflatex paper_v2.tex
```

## Contact

For questions about the paper:
- Email: philip.drammeh@gmail.com
- Open an issue in the main repository
