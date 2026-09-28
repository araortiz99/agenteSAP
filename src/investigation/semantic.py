"""Shared semantic normalization for the consultative vertical."""

from __future__ import annotations

import hashlib

from src.investigation.contracts import InvestigationEvidence
from src.tools.search_unified import UnifiedResult


def unified_to_investigation_evidence(result: UnifiedResult) -> InvestigationEvidence:
    raw = "|".join(
        (
            result.source_layer,
            result.path,
            result.source_id or "",
            result.knowledge_type,
            result.certainty,
            result.content,
        )
    )
    evidence_id = "EVD-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12].upper()
    return InvestigationEvidence(
        evidence_id=evidence_id,
        provider=result.source_layer,
        operation=result.match_type,
        landscape="QAS" if result.knowledge_type == "runtime_observation" else "KNOWLEDGE",
        system=None,
        object_type=result.knowledge_type,
        object_id=result.source_id,
        observation_type=result.knowledge_type,
        content=result.content,
        certainty=result.certainty,
        provenance=result.provenance,
    )
