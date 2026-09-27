"""Minimal read-only GitHub API client for agenteSAP.

The MVP intentionally supports only repository reads.
Authentication is supplied through the GITHUB_TOKEN environment variable.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request


class GitHubAPIError(RuntimeError):
    """Raised when the GitHub API cannot fulfill a read request."""


class GitHubClient:
    def __init__(
        self,
        owner: str,
        repo: str,
        token: str | None = None,
        api_version: str = "2026-03-10",
    ) -> None:
        self.owner = owner
        self.repo = repo
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.api_version = api_version

    def _request(self, path: str) -> object:
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/{path.lstrip('/')}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": self.api_version,
            "User-Agent": "agenteSAP/0.1",
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = urllib.request.Request(url, headers=headers, method="GET")

        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise GitHubAPIError(
                f"GitHub API returned HTTP {exc.code} for {path}"
            ) from exc
        except urllib.error.URLError as exc:
            raise GitHubAPIError(f"GitHub API unavailable: {exc.reason}") from exc

    def get_repository(self) -> dict:
        return self._request("")  # type: ignore[return-value]

    def get_tree(self, ref: str = "main") -> list[dict]:
        encoded_ref = urllib.parse.quote(ref, safe="")
        data = self._request(f"git/trees/{encoded_ref}?recursive=1")
        return data.get("tree", [])  # type: ignore[union-attr]

    def get_file(self, path: str, ref: str = "main") -> str:
        encoded_path = urllib.parse.quote(path, safe="/")
        encoded_ref = urllib.parse.quote(ref, safe="")
        data = self._request(f"contents/{encoded_path}?ref={encoded_ref}")

        if not isinstance(data, dict) or data.get("type") != "file":
            raise GitHubAPIError(f"Repository path is not a file: {path}")

        import base64

        return base64.b64decode(data["content"]).decode("utf-8")
