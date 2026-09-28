"""Convenience entry point for the local AgenteSAP workbench.

Usage:
    python -m src.app
"""

from src.app.server import main


if __name__ == "__main__":
    raise SystemExit(main())
