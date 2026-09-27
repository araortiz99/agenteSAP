"""Source registry for controlled SAP Standard ingestion."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class SAPSource:
    source_id: str
    url: str
    product: str
    module: str
    release: str
    language: str = "en"
    status: str = "active"


class SourceRegistry:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> dict[str, SAPSource]:
        if not self.path.exists():
            return {}
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return {
            item["source_id"]: SAPSource(**item)
            for item in raw.get("sources", [])
        }

    def save(self, sources: dict[str, SAPSource]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "sources": [
                {
                    "source_id": s.source_id,
                    "url": s.url,
                    "product": s.product,
                    "module": s.module,
                    "release": s.release,
                    "language": s.language,
                    "status": s.status,
                }
                for s in sorted(sources.values(), key=lambda x: x.source_id)
            ]
        }
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def get(self, source_id: str) -> SAPSource:
        sources = self.load()
        try:
            return sources[source_id]
        except KeyError as exc:
            raise KeyError(f"Unknown SAP source_id: {source_id}") from exc
