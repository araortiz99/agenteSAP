"""Command-line entry point for the read-only SAP consultant."""

from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
import json
import os
import sys

from src.agent.router import run_agent
from src.document.file_input import load_document_file
from src.document.ingestion import ingest_document
from src.github.client import GitHubClient
from src.investigation.engine import investigate, render_investigation


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="agenteSAP consultant")
    parser.add_argument("request", nargs="?", help="Consultative request in natural language")
    parser.add_argument("--owner", default=os.getenv("GITHUB_OWNER", "araortiz99"))
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPO", "agenteSAP"))
    parser.add_argument("--ref", default=os.getenv("GITHUB_REF", "main"))
    parser.add_argument("--ticket", default=None)
    parser.add_argument("--max-results", type=int, default=8)
    parser.add_argument("--json", action="store_true")
    return parser


def _run_investigation(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="agenteSAP bounded SAP investigation")
    parser.add_argument("request", help="SAP investigation question")
    parser.add_argument("--owner", default=os.getenv("GITHUB_OWNER", "araortiz99"))
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPO", "agenteSAP"))
    parser.add_argument("--ref", default=os.getenv("GITHUB_REF", "main"))
    parser.add_argument("--max-steps", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.max_steps < 1:
        parser.error("--max-steps debe ser mayor que cero")

    client = GitHubClient(args.owner, args.repo, token=os.getenv("GITHUB_TOKEN"))
    result = investigate(
        client,
        args.request,
        ref=args.ref,
        max_steps=args.max_steps,
    )
    if args.json:
        print(json.dumps(result.as_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_investigation(result), end="")
    return 0


def _run_file_ingestion(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="agenteSAP bounded local document ingestion")
    parser.add_argument("path", help="Local text document path")
    parser.add_argument("--max-bytes", type=int, default=2_000_000)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.max_bytes < 1:
        parser.error("--max-bytes debe ser mayor que cero")

    source = load_document_file(args.path, max_bytes=args.max_bytes)
    result = ingest_document(source)

    payload = {
        "document_id": source.document_id,
        "filename": source.filename,
        "file_type": source.file_type,
        "media_type": source.media_type,
        "size": source.size,
        "content_hash": source.content_hash,
        "chunks": len(result.chunks),
        "records": len(result.records),
        "evidence": [asdict(item) for item in result.evidence],
        "entities": [asdict(item) for item in result.entities],
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Document: {payload['document_id']}")
        print(f"File: {payload['filename']}")
        print(f"Chunks: {payload['chunks']}")
        print(f"Evidence: {len(payload['evidence'])}")
        print(f"Entities: {len(result.entities)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    if raw and raw[0] == "investigate":
        return _run_investigation(raw[1:])
    if raw and raw[0] == "ingest-file":
        return _run_file_ingestion(raw[1:])

    parser = _build_parser()
    args = parser.parse_args(raw)
    if not args.request:
        parser.error("request es obligatorio")
    if args.max_results < 1:
        parser.error("--max-results debe ser mayor que cero")

    github = GitHubClient(args.owner, args.repo, token=os.getenv("GITHUB_TOKEN"))
    response = run_agent(
        github,
        args.request,
        ref=args.ref,
        ticket_id=args.ticket,
        max_results=args.max_results,
    )

    if args.json:
        if not is_dataclass(response):
            raise TypeError("Agent response is not serializable")
        print(json.dumps(asdict(response), ensure_ascii=False, indent=2))
    elif hasattr(response.result, "answer"):
        print(response.result.answer)
    else:
        print(response.result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
