def test_dq_scorer():
    from src.scoring.dq_scorer_v2 import DQScorer
    scorer = DQScorer("test ground truth")
    result = scorer.score_trial(["test action"])
    assert 'dq' in result
    assert 0 <= result['dq'] <= 1
