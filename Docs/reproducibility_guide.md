# Complete Reproducibility Guide

This guide provides step-by-step instructions for reproducing the paper results from scratch.

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL2
- **RAM**: 16GB minimum, 32GB recommended
- **Disk Space**: 20GB free space
- **CPU**: Multi-core processor recommended (4+ cores)
- **GPU**: Optional (speeds up inference 3-5x)

### Software Requirements
```bash
# Check versions
docker --version          # Requires 24.0+
docker-compose --version  # Requires 2.21+
python --version          # Requires 3.11+
```

## Step-by-Step Reproduction

### 1. Clone Repository
```bash
git clone https://github.com/Phildram1/myantfarm-assets
cd myantfarm-assets
```

### 2. Verify Environment
```bash
make check

# Expected output:
# ✓ Docker: Docker version 24.0.6
# ✓ Docker Compose: Docker Compose version 2.21.0
# ✓ Python: Python 3.11.4
# ✓ Environment OK
```

### 3. Option A: Complete Automated Reproduction
```bash
make full

# This will:
# 1. Build all Docker containers (~5-10 minutes)
# 2. Download Llama 3.2 model (~5-15 minutes, 5GB)
# 3. Run 348 trials (~45-60 minutes)
# 4. Generate analysis and plots (~2-3 minutes)
# 5. Export LaTeX tables (~1 minute)
# 6. Verify results match paper

# Total time: 1-2 hours
```

### 4. Option B: Step-by-Step Reproduction
```bash
# Step 1: Build containers
make setup

# Step 2: Download model
make pull-model

# Step 3: Run evaluation
make run-evaluation

# Step 4: Analyze results
make analyze

# Step 5: Generate plots
make plots

# Step 6: Export LaTeX tables
make latex

# Step 7: Verify results
make verify
```

### 5. Quick Test (Optional)

Before running the full evaluation, test with 10 trials per condition:
```bash
make quick-test

# Expected time: ~5-10 minutes
# Results will be approximate but verify the pipeline works
```

## Expected Timeline

| Phase | Duration | Output |
|-------|----------|--------|
| Setup & Build | 5-10 min | Docker images |
| Model Download | 5-15 min | Llama 3.2 model (5GB) |
| Evaluation (348 trials) | 45-60 min | Trial JSON files |
| Analysis | 2-3 min | Statistical reports, metrics |
| Plots | 1-2 min | PNG figures |
| LaTeX Export | <1 min | TeX tables |
| Verification | <1 min | Pass/fail report |
| **TOTAL** | **60-90 min** | Complete reproduction |

## Verification Checklist

After running `make verify`, you should see:
```
✓ Total trials: 348
✓ C1 trials: 116
✓ C2 trials: 116
✓ C3 trials: 116
✓ C1 T2U mean: 120.79±6.53 (matches paper)
✓ C2 T2U mean: 79.01±5.01 (matches paper)
✓ C3 T2U mean: 50.46±3.50 (matches paper)
✓ C1 DQ mean: 0.606±0.040 (matches paper)
✓ C2 DQ mean: 0.749±0.037 (matches paper)
✓ C3 DQ mean: 0.899±0.020 (matches paper)
✓ T2U improvement (C1→C3): 58.2%
✓ DQ improvement (C1→C3): 48.3%
✓ Statistical tests significant

✅ ALL CHECKS PASSED - Results match paper!
```

## Output Structure
```
results/
├── all_trials.json              # All 348 trial results
├── trials/                      # Individual trial files
│   ├── trial_C1_000.json
│   ├── trial_C1_001.json
│   └── ... (348 total)
├── analysis/
│   ├── summary_t2u.csv          # T2U statistics
│   ├── summary_dq.csv           # DQ statistics
│   ├── statistical_analysis.md  # ANOVA, t-tests, CIs
│   ├── t2u_comparison.png       # Figure 1
│   ├── dq_comparison.png        # Figure 2
│   ├── convergence_analysis.png # Figure 3
│   ├── action_distribution.png  # Figure 4
│   └── tables/
│       ├── table_1_main_results.tex
│       ├── table_2_improvements.tex
│       ├── table_3_confidence_intervals.tex
│       └── table_4_action_counts.tex
```

## Common Issues

### Issue: Model Download Fails
```bash
# Solution: Manual download
docker exec -it myantfarm_ollama bash
ollama pull llama3.2:8b-instruct-q4
exit
```

### Issue: Out of Memory
```bash
# Solution: Use smaller model
docker exec myantfarm_ollama ollama pull llama3.2:3b-instruct-q4

# Edit docker-compose.yml:
# Change MODEL_NAME to llama3.2:3b-instruct-q4
```

### Issue: Services Not Starting
```bash
# Check logs
make logs

# Restart services
docker-compose restart

# Hard reset
make clean-all
make setup
```

### Issue: Results Don't Match

Common causes:
1. Different random seed → Check `RANDOM_SEED=42` in .env
2. Different model version → Verify model SHA256
3. Modified code → Re-clone repository
4. Docker version mismatch → Update Docker to 24.0+
```bash
# Verify configuration
docker-compose config | grep -E "(RANDOM_SEED|MODEL_NAME|TRIALS)"
```

## Re-scoring Existing Results

If you have results from the original paper formula:
```bash
make rescore

# This will:
# 1. Load existing trial outputs
# 2. Re-compute DQ with corrected formula
# 3. Generate comparison report
# 4. Run statistical tests on re-scored data
```

## Troubleshooting

See `docs/troubleshooting.md` for detailed troubleshooting guide.

## Contact

If you encounter issues not covered in this guide:

1. Check GitHub Issues: https://github.com/Phildram1/myantfarm-assets/issues
2. Email: philip.drammeh@gmail.com
3. Include:
   - Error messages
   - Output of `make check`
   - Docker logs (`make logs`)

## Next Steps

After successful reproduction:

- **Extend scenarios**: See `docs/adding_scenarios.md`
- **Add agent roles**: See `docs/extending_agents.md`
- **Integrate RAG**: Coming in Phase 2
- **Deploy to production**: See `docs/deployment_guide.md` (future)