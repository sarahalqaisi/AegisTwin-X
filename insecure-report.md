# AegisTwin X Security Report

- Decision: **BLOCK**
- Baseline score: **96/100**
- Candidate score: **32/100**
- Security DNA drift: **17%**

2 verified product-security regressions changed TwinShop's authorization model.

## Cross-account invoice access

**HIGH · VERIFIED**

One customer can view another customer's billing information.

Path: `Customer account -> Invoice API -> Missing ownership check -> Another customer's invoice`

Remediation: Restore the invoice.owner_id == authenticated_user.id check and retain the generated regression test.

## Support agent can approve a refund

**CRITICAL · VERIFIED**

A support account can authorize a financial action without managerial approval.

Path: `Support account -> Refund review -> Missing manager gate -> Refund approved`

Remediation: Enforce the manager role server-side and add a negative authorization test for support identities.
