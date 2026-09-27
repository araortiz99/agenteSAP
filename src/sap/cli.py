"""Command-line interface for controlled SAP Help ingestion."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from src.sap.ingestion import ingest_source
from src.sap.registry import SourceRegistry


DEFAULT_REGISTRY = Path("knowledge/sap-standard/source-registry.json")
DEFAULT_STAGING = Path("staging/sap-standard")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest an official SAP Help source into staging.")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING)
    parser.add_argument("--url", help="Override the registered URL only for controlled local testing.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    registry = SourceRegistry(args.registry)
    source = registry.get(args.source_id)

    url = args.url or source.url
    if args.url and args.url != source.url:
        print(
            "ERROR: URL override differs from the registered source. "
            "Update the source registry first.",
            file=sys.stderr,
        )
        return 2

    result = ingest_source(
        source_id=source.source_id,
        url=url,
        product=source.product,
        module=source.module,
        release=source.release,
        language=source.language,
        output_dir=args.staging_dir,
    )
    print(f"source_id={result.source_id}")
    print(f"output={result.output_path}")
    print(f"checksum_sha256={result.metadata.checksum_sha256}")
    print(f"status={result.metadata.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
