"""Controlled collector for official SAP Help sources."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ALLOWED_HOSTS = {"help.sap.com"}
MAX_BYTES = 2_000_000
USER_AGENT = "agenteSAP-sap-help-ingestor/0.1"


class SAPSourceError(RuntimeError):
    """Raised when an SAP source cannot be safely retrieved."""


@dataclass(frozen=True)
class RetrievedSource:
    url: str
    content_type: str
    content: str


def _validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise SAPSourceError("Only official HTTPS SAP Help sources are allowed")


def collect_source(url: str, timeout: int = 20) -> RetrievedSource:
    """Retrieve an official SAP Help page with bounded size and no credentials."""
    _validate_url(url)
    request = Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
    try:
        with urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get_content_type()
            raw = response.read(MAX_BYTES + 1)
    except Exception as exc:  # pragma: no cover - network-specific errors
        raise SAPSourceError(f"Unable to retrieve SAP source: {exc}") from exc

    if len(raw) > MAX_BYTES:
        raise SAPSourceError("SAP source exceeds the configured size limit")

    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SAPSourceError("SAP source is not UTF-8 text") from exc

    return RetrievedSource(url=url, content_type=content_type, content=content)
