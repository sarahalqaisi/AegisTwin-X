from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Decision(str, Enum):
    passed = "PASS"
    warn = "WARN"
    block = "BLOCK"


class SecurityPromise(BaseModel):
    id: str
    title: str
    description: str
    subject_role: str
    action: str
    resource: str
    condition: str
    endpoint: str
    expected_on_failure: int = 403
    severity: Severity
    approved: bool = True


class Evidence(BaseModel):
    expected_status: int
    observed_status: int
    subject: str
    target: str
    sanitized_response: dict[str, Any] = Field(default_factory=dict)


class Finding(BaseModel):
    id: str
    promise_id: str
    title: str
    severity: Severity
    verified: bool
    engineering_summary: str
    business_summary: str
    attack_path: list[str]
    evidence: Evidence
    remediation: str


class GraphPayload(BaseModel):
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]


class AnalysisReport(BaseModel):
    analysis_id: str
    project: str
    baseline_score: int
    candidate_score: int
    security_dna_drift: int
    decision: Decision
    changed_relationships: list[str]
    findings: list[Finding]
    graph: GraphPayload
    summary: str

