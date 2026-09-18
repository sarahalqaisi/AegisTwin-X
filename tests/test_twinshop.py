from aegistwin.twinshop import approve_refund, read_invoice


def test_customer_can_read_own_invoice():
    status, body = read_invoice("customer-alex", "inv-1001")
    assert status == 200
    assert body["owner_id"] == "customer-alex"


def test_customer_cannot_read_another_invoice():
    status, _ = read_invoice("customer-alex", "inv-2001")
    assert status == 403


def test_support_cannot_approve_refund():
    status, _ = approve_refund("support-jordan", "ref-9001")
    assert status == 403


def test_disabled_user_is_rejected():
    status, _ = read_invoice("disabled-casey", "inv-1001")
    assert status == 401

