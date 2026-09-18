from __future__ import annotations

import argparse
from pathlib import Path

from aegistwin.analyzer import analyze
from aegistwin.policy import load_promises


def main() -> int:
    parser = argparse.ArgumentParser(description="AegisTwin X security gate")
    parser.add_argument("--variant", choices=["secure", "insecure"], default="secure")
    parser.add_argument("--output", default="aegistwin-report.md")
    args = parser.parse_args()
    policies = load_promises(Path("policies/twinshop.yml"))
    report = analyze(policies, vulnerable=args.variant == "insecure")
    lines = [
        "# AegisTwin X Security Report",
        "",
        f"- Decision: **{report.decision.value}**",
        f"- Baseline score: **{report.baseline_score}/100**",
        f"- Candidate score: **{report.candidate_score}/100**",
        f"- Security DNA drift: **{report.security_dna_drift}%**",
        "",
        report.summary,
        "",
    ]
    for finding in report.findings:
        lines += [
            f"## {finding.title}",
            "",
            f"**{finding.severity.value.upper()} · VERIFIED**",
            "",
            finding.business_summary,
            "",
            f"Path: `{' -> '.join(finding.attack_path)}`",
            "",
            f"Remediation: {finding.remediation}",
            "",
        ]
    Path(args.output).write_text("\n".join(lines), encoding="utf-8")
    print(f"AegisTwin decision: {report.decision.value} | report: {args.output}")
    return 1 if report.decision.value == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())

