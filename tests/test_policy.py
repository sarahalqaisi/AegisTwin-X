from pathlib import Path

from aegistwin.policy import load_promises


def test_loads_five_approved_promises():
    policies = load_promises(Path("policies/twinshop.yml"))
    assert len(policies) == 5
    assert all(policy.approved for policy in policies)
    assert {policy.id for policy in policies} >= {"INV-OWNERSHIP-001", "REF-MANAGER-001"}

