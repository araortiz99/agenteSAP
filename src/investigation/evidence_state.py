"""Semantic state model for investigation evidence.

States are explicit and never collapse missing evidence into a negative fact.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

EVIDENCE_STATES = frozenset(
    {
        "AVAILABLE",
        "MISSING",
        "INSUFFICIENT",
        "CONFLICTING",
        "INVALID",
        "NOT_APPLICABLE",
    }
)


@dataclass(frozen=True)
class EvidenceState:
    evidence_id: str | None
    state: str
    reason: str

    def __post_init__(self) -> None:
        if self.state not in EVIDENCE_STATES:
            raise ValueError(f"unsupported evidence state: {self.state}")


def assess_investigation_evidence_state(
    evidence_id: str | None,
    *,
    available: bool,
    valid: bool = True,
    sufficient: bool = True,
    conflicting: bool = False,
    applicable: bool = True,
    reason: str = "",
) -> EvidenceState:
    """Apply a deterministic precedence order to one evidence state."""
    if not applicable:
        state = "NOT_APPLICABLE"
    elif not valid:
        state = "INVALID"
    elif conflicting:
        state = "CONFLICTING"
    elif not available:
        state = "MISSING"
    elif not sufficient:
        state = "INSUFFICIENT"
    else:
        state = "AVAILABLE"
    return EvidenceState(evidence_id, state, reason)


def summarize_states(states: Iterable[EvidenceState]) -> dict[str, int]:
    summary = {state: 0 for state in sorted(EVIDENCE_STATES)}
    for item in states:
        summary[item.state] += 1
    return summary
