import re
from dataclasses import dataclass
from src.document.provenance import DocumentRecord

@dataclass(frozen=True)
class SapEntity:
    entity_type: str
    value: str
    record_id: str
    position: int

PATTERNS={
    "TRANSACTION": re.compile(r"\b[A-Z]{2,4}\d{2,4}\b"),
    "TABLE": re.compile(r"\b(?:MARA|MARC|MARD|MBEW|EKKO|EKPO|BKPF|BSEG|ACDOCA)\b"),
    "Z_PROGRAM": re.compile(r"\bZ[A-Z0-9_]{4,}\b"),
    "MOVEMENT": re.compile(r"\b(?:101|102|201|261|301|551|552)\b"),
}

def extract_sap_entities(record: DocumentRecord, max_entities: int = 64) -> tuple[SapEntity, ...]:
    if max_entities < 1: raise ValueError("max_entities must be greater than zero")
    found=[]
    for kind, pattern in PATTERNS.items():
        for match in pattern.finditer(record.content):
            found.append(SapEntity(kind, match.group(0), record.record_id, match.start()))
            if len(found)>=max_entities: return tuple(found)
    return tuple(found)
