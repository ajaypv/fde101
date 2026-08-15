"""Route conflicting loan-agent findings without letting an LLM decide credit."""

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import json
from math import isfinite


@dataclass(frozen=True)
class Evidence:
    """A normalized record returned by a trusted source adapter."""

    evidence_id: str
    application_id: str
    kind: str
    source: str
    observed_at: datetime
    verified: bool
    signal: str


@dataclass(frozen=True)
class AgentFinding:
    """A specialist's proposal, not an authorization or credit decision."""

    role: str
    proposed_outcome: str
    confidence: float
    reason_codes: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    model_version: str
    prompt_version: str


@dataclass(frozen=True)
class Resolution:
    review_queue: str
    reason_codes: tuple[str, ...]
    validated_evidence_ids: tuple[str, ...]
    agent_conflict: bool
    credit_decision: str = "not_made"
    requires_human_review: bool = True
    policy_version: str = "loan-review-routing-v1"


# Trusted source + evidence kind -> maximum allowed age.
SOURCE_RULES: dict[tuple[str, str], timedelta] = {
    ("payroll_api", "income_verification"): timedelta(days=30),
    ("credit_bureau", "credit_report"): timedelta(days=30),
    ("transaction_monitor", "fraud_signal"): timedelta(days=1),
    ("compliance_system", "compliance_signal"): timedelta(days=1),
}
REQUIRED_ROLES = {"eligibility_agent", "fraud_agent"}
ALLOWED_ROLES = REQUIRED_ROLES | {"compliance_agent"}
ALLOWED_PROPOSALS = {"approve", "reject"}
ROLE_EVIDENCE_KINDS = {
    "eligibility_agent": frozenset({"income_verification", "credit_report"}),
    "fraud_agent": frozenset({"fraud_signal"}),
    "compliance_agent": frozenset({"compliance_signal"}),
}
REASON_SIGNALS = {
    "INCOME_VERIFIED": "income_verified",
    "CREDIT_POLICY_PASSED": "credit_policy_passed",
    "UNUSUAL_RECENT_TRANSACTION": "unusual_recent_transaction",
    "CONFIRMED_COMPLIANCE_VIOLATION": "confirmed_compliance_violation",
}


def evidence_issue(
    item: Evidence, *, application_id: str, now: datetime
) -> str | None:
    """Return a reason code when evidence is unusable for this application."""
    if item.application_id != application_id:
        return f"WRONG_APPLICATION:{item.evidence_id}"
    max_age = SOURCE_RULES.get((item.source, item.kind))
    if max_age is None:
        return f"UNTRUSTED_SOURCE_OR_KIND:{item.evidence_id}"
    if not item.verified:
        return f"UNVERIFIED_EVIDENCE:{item.evidence_id}"
    if item.observed_at.tzinfo is None:
        return f"TIMEZONE_MISSING:{item.evidence_id}"
    if item.observed_at > now + timedelta(minutes=5):
        return f"FUTURE_TIMESTAMP:{item.evidence_id}"
    if now - item.observed_at > max_age:
        return f"STALE_EVIDENCE:{item.evidence_id}"
    return None


def resolve_for_review(
    application_id: str,
    findings: tuple[AgentFinding, ...],
    evidence_records: tuple[Evidence, ...],
    *,
    now: datetime,
) -> Resolution:
    """Choose a human review queue; never return a loan approval or denial."""
    issues: list[str] = []
    by_role: dict[str, AgentFinding] = {}

    for finding in findings:
        if finding.role in by_role:
            issues.append(f"DUPLICATE_ROLE:{finding.role}")
        by_role[finding.role] = finding
        if finding.role not in ALLOWED_ROLES:
            issues.append(f"UNEXPECTED_ROLE:{finding.role}")
        if finding.proposed_outcome not in ALLOWED_PROPOSALS:
            issues.append(f"INVALID_PROPOSAL:{finding.role}")
        if not isfinite(finding.confidence) or not 0 <= finding.confidence <= 1:
            issues.append(f"INVALID_CONFIDENCE:{finding.role}")
        if not finding.reason_codes:
            issues.append(f"MISSING_REASON_CODE:{finding.role}")
        if not finding.evidence_ids:
            issues.append(f"MISSING_EVIDENCE_REFERENCE:{finding.role}")

    for role in sorted(REQUIRED_ROLES - by_role.keys()):
        issues.append(f"MISSING_ROLE:{role}")

    evidence_by_id: dict[str, Evidence] = {}
    for item in evidence_records:
        if item.evidence_id in evidence_by_id:
            issues.append(f"DUPLICATE_EVIDENCE:{item.evidence_id}")
        evidence_by_id[item.evidence_id] = item

    requested_ids = sorted(
        {item for finding in findings for item in finding.evidence_ids}
    )
    validated_ids: list[str] = []
    for evidence_id in requested_ids:
        item = evidence_by_id.get(evidence_id)
        if item is None:
            issues.append(f"MISSING_EVIDENCE:{evidence_id}")
            continue
        issue = evidence_issue(item, application_id=application_id, now=now)
        if issue:
            issues.append(issue)
        else:
            validated_ids.append(evidence_id)

    validated_id_set = set(validated_ids)
    for finding in findings:
        allowed_kinds = ROLE_EVIDENCE_KINDS.get(finding.role, frozenset())
        supporting_signals: set[str] = set()

        for evidence_id in finding.evidence_ids:
            item = evidence_by_id.get(evidence_id)
            if item is None or evidence_id not in validated_id_set:
                continue
            if item.kind not in allowed_kinds:
                issues.append(f"ROLE_EVIDENCE_MISMATCH:{finding.role}:{evidence_id}")
            supporting_signals.add(item.signal)

        for reason_code in finding.reason_codes:
            expected_signal = REASON_SIGNALS.get(reason_code)
            if expected_signal is None:
                issues.append(f"UNKNOWN_REASON_CODE:{finding.role}:{reason_code}")
            elif expected_signal not in supporting_signals:
                issues.append(f"UNSUPPORTED_REASON:{finding.role}:{reason_code}")

    proposals = {finding.proposed_outcome for finding in findings}
    has_conflict = len(proposals) > 1

    if issues:
        return Resolution(
            "data_validation", tuple(sorted(set(issues))), tuple(validated_ids), has_conflict
        )

    signals = {evidence_by_id[item].signal for item in validated_ids}

    # Reviewed policy outranks model confidence and majority vote.
    if "confirmed_compliance_violation" in signals:
        queue, reasons = "compliance_review", ("VERIFIED_COMPLIANCE_SIGNAL",)
    elif "unusual_recent_transaction" in signals:
        queue, reasons = "fraud_review", ("VERIFIED_FRAUD_SIGNAL",)
    elif has_conflict:
        queue, reasons = "conflict_review", ("AGENT_OUTCOMES_DISAGREE",)
    else:
        queue, reasons = "underwriter_review", ("AGENT_FINDINGS_ALIGNED",)

    return Resolution(queue, reasons, tuple(validated_ids), has_conflict)


def make_audit_record(
    application_id: str,
    findings: tuple[AgentFinding, ...],
    resolution: Resolution,
    *,
    recorded_at: datetime,
) -> dict[str, object]:
    """Record traceable pointers and versions, not raw applicant data."""
    return {
        "application_id": application_id,
        "recorded_at": recorded_at.isoformat(),
        **asdict(resolution),
        "agent_findings": [asdict(finding) for finding in findings],
    }


def demo() -> None:
    now = datetime(2026, 8, 15, 9, 0, tzinfo=timezone.utc)
    application_id = "synthetic-application-1042"
    evidence = (
        Evidence("ev-income-17", application_id, "income_verification", "payroll_api",
                 now - timedelta(days=3), True, "income_verified"),
        Evidence("ev-credit-24", application_id, "credit_report", "credit_bureau",
                 now - timedelta(hours=8), True, "credit_policy_passed"),
        Evidence("ev-fraud-09", application_id, "fraud_signal", "transaction_monitor",
                 now - timedelta(hours=2), True, "unusual_recent_transaction"),
    )
    findings = (
        AgentFinding(
            "eligibility_agent", "approve", 0.91,
            ("INCOME_VERIFIED", "CREDIT_POLICY_PASSED"),
            ("ev-income-17", "ev-credit-24"), "eligibility-model-3", "prompt-8"
        ),
        AgentFinding(
            "fraud_agent", "reject", 0.78,
            ("UNUSUAL_RECENT_TRANSACTION",),
            ("ev-fraud-09",), "fraud-model-5", "prompt-4"
        ),
    )

    resolution = resolve_for_review(application_id, findings, evidence, now=now)

    # Fraud evidence activates policy even though its agent reported less confidence.
    assert resolution.review_queue == "fraud_review"
    assert resolution.credit_decision == "not_made"
    assert resolution.requires_human_review

    # An optional compliance specialist can activate the higher-priority route.
    compliance_evidence = evidence + (
        Evidence(
            "ev-compliance-03", application_id, "compliance_signal",
            "compliance_system", now - timedelta(hours=1), True,
            "confirmed_compliance_violation"
        ),
    )
    compliance_findings = findings + (
        AgentFinding(
            "compliance_agent", "reject", 0.84,
            ("CONFIRMED_COMPLIANCE_VIOLATION",),
            ("ev-compliance-03",), "compliance-model-2", "prompt-2"
        ),
    )
    compliance_resolution = resolve_for_review(
        application_id, compliance_findings, compliance_evidence, now=now
    )
    assert compliance_resolution.review_queue == "compliance_review"

    record = make_audit_record(
        application_id, findings, resolution, recorded_at=now
    )
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    demo()
