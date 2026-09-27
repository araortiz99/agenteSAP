"""CLI for explicit promotion of validated SAP candidates."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.sap.promotion import promote_candidate
from src.sap.registry import SourceRegistry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Promote one SAP Standard candidate after validation."
    )
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("knowledge/sap-standard/source-registry.json"),
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path("knowledge/sap-standard/mm"),
    )
    args = parser.parse_args(argv)

    result = promote_candidate(
        candidate_path=args.candidate,
        destination_dir=args.destination,
        registry=SourceRegistry(args.registry),
    )
    print(f"source_id={result.source_id}")
    print(f"output={result.output_path}")
    print(f"status={result.status}")
    print(f"certainty={result.certainty}")
    print(f"checksum_sha256={result.checksum_sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
