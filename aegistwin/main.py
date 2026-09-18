from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .analyzer import analyze
from .mutation import evaluate_mutations
from .policy import load_promises
from .store import ReportStore
from .twinshop import USERS, approve_refund, read_invoice


ROOT = Path(__file__).resolve().parents[1]
PROMISES = load_promises(ROOT / "policies" / "twinshop.yml")
STORE = ReportStore(ROOT / "data" / "aegistwin.db")

app = FastAPI(
    title="AegisTwin X",
    version="0.1.0",
    description="Product-security intelligence and deterministic business-logic verification.",
)
app.mount("/static", StaticFiles(directory=ROOT / "web"), name="static")


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(ROOT / "web" / "index.html")


@app.get("/health")
def health():
    return {"status": "healthy", "service": "AegisTwin X", "version": "0.1.0"}


@app.get("/api/promises")
def promises():
    return PROMISES


@app.post("/api/analyses/demo")
def run_demo(variant: str = Query(default="insecure", pattern="^(secure|insecure)$")):
    report = analyze(PROMISES, vulnerable=variant == "insecure")
    STORE.save(report)
    return report


@app.get("/api/analyses")
def recent_analyses():
    return STORE.recent()


@app.post("/api/mutations/demo")
def run_mutation_demo():
    """Run defensive mutations only against the bundled synthetic lab."""
    return [result.__dict__ for result in evaluate_mutations()]


@app.get("/api/twinshop/invoices/{invoice_id}")
def invoice(invoice_id: str, x_demo_user: str = Header(default="customer-alex"), vulnerable: bool = False):
    status, body = read_invoice(x_demo_user, invoice_id, vulnerable=vulnerable)
    if status != 200:
        raise HTTPException(status_code=status, detail=body["detail"])
    return body


@app.post("/api/twinshop/refunds/{refund_id}/approve")
def refund(refund_id: str, x_demo_user: str = Header(default="support-jordan"), vulnerable: bool = False):
    status, body = approve_refund(x_demo_user, refund_id, vulnerable=vulnerable)
    if status != 200:
        raise HTTPException(status_code=status, detail=body["detail"])
    return body


@app.get("/api/twinshop/users")
def users():
    return [{"id": u.id, "name": u.name, "role": u.role, "active": u.active} for u in USERS.values()]
