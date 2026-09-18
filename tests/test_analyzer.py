from pathlib import Path

from aegistwin.analyzer import analyze
from aegistwin.models import Decision
from aegistwin.policy import load_promises


POLICIES = load_promises(Path("policies/twinshop.yml"))


def test_insecure_candidate_is_blocked_with_evidence():
    report = analyze(POLICIES, vulnerable=True)
    assert report.decision == Decision.block
    assert report.candidate_score < report.baseline_score
    assert len(report.findings) == 2
    assert all(finding.verified for finding in report.findings)


def test_fixed_candidate_passes():
    report = analyze(POLICIES, vulnerable=False)
    assert report.decision == Decision.passed
    assert report.findings == []
    assert report.security_dna_drift == 0

