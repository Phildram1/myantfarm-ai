# Incident Scenarios

This directory contains incident scenarios used for evaluation.

## Main Scenario

**auth_service_outage.json**: The authentication service outage scenario used for all 348 trials in the paper.

- **Root Cause**: Database connection pool exhaustion in v2.4.0
- **Solution**: Rollback to v2.3.0, verify pool settings
- **Complexity**: Medium
- **Used in**: All C1, C2, C3 trials

## Adding New Scenarios

To add a new scenario:

1. Create a JSON file with the structure shown in `auth_service_outage.json`
2. Include: scenario metadata, context, symptoms, timeline, ground truth
3. Update the evaluator to reference the new scenario
4. Run trials to evaluate performance