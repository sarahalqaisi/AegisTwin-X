from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class User:
    id: str
    name: str
    role: str
    active: bool = True


USERS = {
    "customer-alex": User("customer-alex", "Alex Morgan", "customer"),
    "customer-sam": User("customer-sam", "Sam Rivera", "customer"),
    "support-jordan": User("support-jordan", "Jordan Lee", "support"),
    "manager-riley": User("manager-riley", "Riley Chen", "manager"),
    "disabled-casey": User("disabled-casey", "Casey Quinn", "customer", False),
}

INVOICES = {
    "inv-1001": {"id": "inv-1001", "owner_id": "customer-alex", "total": 89.50, "status": "paid"},
    "inv-2001": {"id": "inv-2001", "owner_id": "customer-sam", "total": 245.00, "status": "paid"},
}

REFUNDS = {
    "ref-9001": {
        "id": "ref-9001",
        "owner_id": "customer-alex",
        "created_by": "support-jordan",
        "amount": 89.50,
        "status": "reviewed",
        "approvals": [],
    }
}


def read_invoice(user_id: str, invoice_id: str, *, vulnerable: bool = False) -> tuple[int, dict[str, Any]]:
    user = USERS.get(user_id)
    invoice = INVOICES.get(invoice_id)
    if not user or not user.active:
        return 401, {"detail": "Inactive or unknown identity"}
    if not invoice:
        return 404, {"detail": "Invoice not found"}
    allowed = user.role in {"support", "manager"} or invoice["owner_id"] == user.id
    if not vulnerable and not allowed:
        return 403, {"detail": "Resource ownership check failed"}
    return 200, invoice


def approve_refund(user_id: str, refund_id: str, *, vulnerable: bool = False) -> tuple[int, dict[str, Any]]:
    user = USERS.get(user_id)
    refund = REFUNDS.get(refund_id)
    if not user or not user.active:
        return 401, {"detail": "Inactive or unknown identity"}
    if not refund:
        return 404, {"detail": "Refund not found"}
    if not vulnerable and user.role != "manager":
        return 403, {"detail": "Manager role required"}
    if not vulnerable and refund["created_by"] == user.id:
        return 403, {"detail": "Separation of duties violation"}
    snapshot = {**refund, "approvals": [*refund["approvals"], user.id], "status": "approved"}
    return 200, snapshot

