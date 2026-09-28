"""Minimal read-only GitHub API client for agenteSAP.

The MVP intentionally supports only repository reads.
Authentication is supplied through the GITHUB_TOKEN environment variable.
"""

from __future__ import annotations

import base64
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
        # A single agent execution performs several retrieval passes over the
        # same ref. Keep an in-memory cache so repeated searches do not repeat
        # identical GitHub API calls. The cache is scoped to this client
        # instance and therefore never becomes persistent agent memory.
        self._repository_cache: dict[str, dict] = {}
        self._tree_cache: dict[str, list[dict]] = {}
        self._file_cache: dict[tuple[str, str], str] = {}

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

    def get_repository(self, ref: str = "") -> dict:
        cache_key = ref
        if cache_key in self._repository_cache:
            return self._repository_cache[cache_key]

        data = self._request("")
        repository = data  # type: ignore[assignment]
        self._repository_cache[cache_key] = repository
        return repository

    def get_tree(self, ref: str = "main") -> list[dict]:
        if ref in self._tree_cache:
            return self._tree_cache[ref]

        encoded_ref = urllib.parse.quote(ref, safe="")
        data = self._request(f"git/trees/{encoded_ref}?recursive=1")
        tree = data.get("tree", [])  # type: ignore[union-attr]
        self._tree_cache[ref] = tree
        return tree

    def get_file(self, path: str, ref: str = "main") -> str:
        cache_key = (ref, path)
        if cache_key in self._file_cache:
            return self._file_cache[cache_key]

        encoded_path = urllib.parse.quote(path, safe="/")
        encoded_ref = urllib.parse.quote(ref, safe="")
        data = self._request(f"contents/{encoded_path}?ref={encoded_ref}")

        if not isinstance(data, dict) or data.get("type") != "file":
            raise GitHubAPIError(f"Repository path is not a file: {path}")

        content = base64.b64decode(data["content"]).decode("utf-8")
        self._file_cache[cache_key] = content
        return content
