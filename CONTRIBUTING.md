# Contributing to MyAntFarm.ai

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Ways to Contribute

### 1. Bug Reports

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Docker version, Python version)
- Relevant logs or error messages

### 2. Feature Requests

Have an idea? Open an issue describing:
- The problem it solves
- Proposed solution
- Alternative approaches considered
- Impact on existing functionality

### 3. Code Contributions

#### Setup Development Environment

\\\ash
# Clone repository
git clone https://github.com/Phildram1/myantfarm-ai
cd myantfarm-ai

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 src/ scripts/
black --check src/ scripts/
\\\

#### Contribution Workflow

1. **Fork the repository**
2. **Create a feature branch**: \git checkout -b feature/your-feature-name\
3. **Make changes** with clear, atomic commits
4. **Write tests** for new functionality
5. **Update documentation** as needed
6. **Run tests**: \pytest tests/\
7. **Submit pull request** with clear description

#### Code Style

- Follow PEP 8 for Python code
- Use Black for formatting: \lack src/ scripts/\
- Add type hints for function signatures
- Include docstrings for public functions
- Keep functions focused and under 50 lines

#### Commit Messages

Use clear, descriptive commit messages:

\\\
feat: add RAG integration for historical incidents
fix: handle empty action lists in DQ scorer
docs: update metrics specification with examples
test: add unit tests for statistical analyzer
\\\

### 4. Documentation Improvements

Documentation contributions are highly valued:
- Fix typos or unclear explanations
- Add examples or use cases
- Improve setup instructions
- Translate documentation (future)

### 5. New Incident Scenarios

To add new scenarios:

1. Create scenario file in \services/evaluator/scenarios/\
2. Define incident context and ground truth resolution
3. Run evaluation with new scenario
4. Document results in \docs/scenarios/\

Example structure:

\\\python
class DatabaseOutageScenario:
    def __init__(self):
        self.name = "database_connection_pool_exhausted"
        self.description = "Payment service unable to connect to database"
        self.telemetry = {
            "error_rate": "100%",
            "affected_services": ["payment-api", "checkout-service"],
            # ...
        }
        self.ground_truth_resolution = "increase connection pool max_connections scale database read replicas"
\\\

## Priority Areas for Contribution

### High Priority

- [ ] Additional incident scenarios (database, network, CDN)
- [ ] Human validation study with SRE practitioners
- [ ] RAG integration with historical incidents
- [ ] MCP connectors for live telemetry (Datadog, Jira, Slack)

### Medium Priority

- [ ] Larger model evaluation (Llama 3.1 70B, GPT-4)
- [ ] Web UI for result visualization
- [ ] CI/CD pipeline for automated testing
- [ ] Docker optimization for faster startup

### Low Priority

- [ ] Multi-language support for documentation
- [ ] Alternative LLM backends (vLLM, text-generation-inference)
- [ ] Prometheus metrics export

## Testing Guidelines

### Unit Tests

Place unit tests in \	ests/\ directory:

\\\python
# tests/test_dq_scorer.py
def test_validity_score():
    scorer = DQScorer("ground truth")
    actions = ["valid action"]
    result = scorer.score_trial(actions)
    assert result['validity'] == 1.0
\\\

### Integration Tests

Test end-to-end workflows:

\\\python
# tests/integration/test_evaluation.py
def test_c2_evaluation():
    # Test single-agent condition
    trial = run_c2_trial(incident_context)
    assert len(trial['actions']) > 0
    assert 'summary' in trial
\\\

### Running Tests

\\\ash
# All tests
pytest

# Specific test file
pytest tests/test_dq_scorer.py

# With coverage
pytest --cov=src tests/
\\\

## Pull Request Process

1. **Update documentation** if adding features
2. **Add tests** for new functionality
3. **Ensure all tests pass**: \pytest\
4. **Update CHANGELOG.md** with changes
5. **Request review** from maintainers
6. **Address review feedback** promptly
7. **Squash commits** before merge if requested

## Code Review Criteria

Reviewers will check:
- [ ] Code follows style guidelines
- [ ] Tests are comprehensive and pass
- [ ] Documentation is updated
- [ ] Changes are backwards compatible (or properly versioned)
- [ ] No security vulnerabilities introduced
- [ ] Performance impact is acceptable

## Community Guidelines

- Be respectful and constructive
- Assume good intentions
- Focus on the work, not the person
- Seek to understand before being understood
- Welcome newcomers and help them contribute

## Questions?

- Open a GitHub Discussion for general questions
- Email philip.drammeh@gmail.com for private inquiries
- Check existing issues before opening new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping improve MyAntFarm.ai! 🐜