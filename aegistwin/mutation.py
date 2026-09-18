from __future__ import annotations

from dataclasses import dataclass

from .twinshop import approve_refund, read_invoice


@dataclass(frozen=True)
class MutationResult:
    id: str
    control: str
    survived: bool
    expected_status: int
    observed_status: int
    generated_test: str


def evaluate_mutations() -> list[MutationResult]:
    """Evaluate safe control removals against the isolated in-memory TwinShop lab."""
    invoice_status, _ = read_invoice("customer-alex", "inv-2001", vulnerable=True)
    refund_status, _ = approve_refund("support-jordan", "ref-9001", vulnerable=True)
    return [
        MutationResult(
            id="MUT-OWNERSHIP-001",
            control="Invoice ownership validation removed",
            survived=invoice_status == 200,
            expected_status=403,
            observed_status=invoice_status,
            generated_test="Customer A requesting Customer B's invoice must receive HTTP 403.",
        ),
        MutationResult(
            id="MUT-ROLE-001",
            control="Manager-only refund gate removed",
            survived=refund_status == 200,
            expected_status=403,
            observed_status=refund_status,
            generated_test="A support identity approving a refund must receive HTTP 403.",
        ),
    ]

