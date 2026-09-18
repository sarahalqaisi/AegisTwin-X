from __future__ import annotations

from uuid import uuid4

from .graph import build_security_graph
from .models import AnalysisReport, Decision, Evidence, Finding, Severity
from .twinshop import approve_refund, read_invoice


SEVERITY_PENALTY = {Severity.low: 5, Severity.medium: 12, Severity.high: 24, Severity.critical: 40}


def _invoice_finding() -> Finding | None:
    status, body = read_invoice("customer-alex", "inv-2001", vulnerable=True)
    if status == 403:
        return None
    return Finding(
        id="ATX-INV-001",
        promise_id="INV-OWNERSHIP-001",
        title="Cross-account invoice access",
        severity=Severity.high,
        verified=status == 200 and body.get("owner_id") == "customer-sam",
        engineering_summary="The candidate removed object-level authorization from GET /invoices/{invoice_id}.",
        business_summary="One customer can view another customer's billing information.",
        attack_path=["Customer account", "Invoice API", "Missing ownership check", "Another customer's invoice"],
        evidence=Evidence(
            expected_status=403,
            observed_status=status,
            subject="customer-alex",
            target="inv-2001 owned by customer-sam",
            sanitized_response={"id": body.get("id"), "owner_id": body.get("owner_id"), "status": body.get("status")},
        ),
        remediation="Restore the invoice.owner_id == authenticated_user.id check and retain the generated regression test.",
    )


def _refund_finding() -> Finding | None:
    status, body = approve_refund("support-jordan", "ref-9001", vulnerable=True)
    if status == 403:
        return None
    return Finding(
        id="ATX-REF-001",
        promise_id="REF-MANAGER-001",
        title="Support agent can approve a refund",
        severity=Severity.critical,
        verified=status == 200 and body.get("status") == "approved",
        engineering_summary="The candidate accepts a support identity on the manager-only refund approval action.",
        business_summary="A support account can authorize a financial action without managerial approval.",
        attack_path=["Support account", "Refund review", "Missing manager gate", "Refund approved"],
        evidence=Evidence(
            expected_status=403,
            observed_status=status,
            subject="support-jordan",
            target="ref-9001",
            sanitized_response={"id": body.get("id"), "status": body.get("status"), "amount": body.get("amount")},
        ),
        remediation="Enforce the manager role server-side and add a negative authorization test for support identities.",
    )


def analyze(promises, vulnerable: bool = True) -> AnalysisReport:
    findings = [item for item in (_invoice_finding(), _refund_finding()) if item] if vulnerable else []
    verified = [finding for finding in findings if finding.verified]
    penalty = sum(SEVERITY_PENALTY[finding.severity] for finding in verified)
    score = max(0, 96 - penalty)
    decision = Decision.block if any(f.severity in {Severity.high, Severity.critical} for f in verified) else Decision.passed
    relationships = (
        ["customer -> any invoice (added)", "support -> approve refund (added)"] if vulnerable else []
    )
    return AnalysisReport(
        analysis_id=f"atx-{uuid4().hex[:8]}",
        project="TwinShop",
        baseline_score=96,
        candidate_score=score,
        security_dna_drift=17 if vulnerable else 0,
        decision=decision,
        changed_relationships=relationships,
        findings=verified,
        graph=build_security_graph(promises, vulnerable),
        summary=(
            f"{len(verified)} verified product-security regressions changed TwinShop's authorization model."
            if verified else "No verified security-promise regression was detected."
        ),
    )

