"""Minimal read-only GitHub API client for agenteSAP.

The MVP intentionally supports only repository reads.
Authentication is supplied through the GITHUB_TOKEN environment variable.
"""

from __future__ import annotations

import base64
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import json
import os
import urllib.error
import urllib.parse
import urllib.request


@dataclass(frozen=True)
class GitHubRateLimit:
    """Rate-limit metadata returned by the GitHub API."""

    limit: int | None = None
    remaining: int | None = None
    reset_epoch: int | None = None
    retry_after: int | None = None


class GitHubAPIError(RuntimeError):
    """Raised when the GitHub API cannot fulfill a read request."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        rate_limit: GitHubRateLimit | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.rate_limit = rate_limit or GitHubRateLimit()


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
        # Scoped to one client lifetime. The local Workbench reuses one client
        # across requests, so repeated consultations reuse already-read content.
        self._repository_cache: dict[str, dict] = {}
        self._tree_cache: dict[str, list[dict]] = {}
        self._file_cache: dict[tuple[str, str], str] = {}
        self._last_rate_limit = GitHubRateLimit()

    @property
    def authenticated(self) -> bool:
        return bool(self.token)

    @property
    def last_rate_limit(self) -> GitHubRateLimit:
        return self._last_rate_limit

    def _rate_limit_from_headers(self, headers) -> GitHubRateLimit:
        def integer(name: str) -> int | None:
            value = headers.get(name)
            try:
                return int(value) if value is not None else None
            except (TypeError, ValueError):
                return None

        return GitHubRateLimit(
            limit=integer("X-RateLimit-Limit"),
            remaining=integer("X-RateLimit-Remaining"),
            reset_epoch=integer("X-RateLimit-Reset"),
            retry_after=integer("Retry-After"),
        )

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
                self._last_rate_limit = self._rate_limit_from_headers(response.headers)
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            rate_limit = self._rate_limit_from_headers(exc.headers)
            self._last_rate_limit = rate_limit

            if exc.code in {403, 429}:
                if rate_limit.remaining == 0:
                    reset = rate_limit.reset_epoch
                    reset_text = (
                        f" UTC epoch {reset}" if reset is not None else " at the reset time"
                    )
                    message = (
                        "GitHub API rate limit exhausted. "
                        f"Retry after the reset{reset_text}."
                    )
                elif rate_limit.retry_after is not None:
                    message = (
                        "GitHub API secondary rate limit reached. "
                        f"Retry after {rate_limit.retry_after} seconds."
                    )
                else:
                    message = (
                        "GitHub API returned a rate-limit/forbidden response. "
                        "Wait before retrying."
                    )
            elif exc.code == 401:
                message = (
                    "GitHub authentication failed (HTTP 401). "
                    "Check GITHUB_TOKEN."
                )
            elif exc.code == 404:
                message = (
                    f"GitHub resource not found or not accessible: {path}. "
                    "For private repositories, verify GITHUB_TOKEN access."
                )
            else:
                message = f"GitHub API returned HTTP {exc.code} for {path}"

            raise GitHubAPIError(
                message,
                status_code=exc.code,
                rate_limit=rate_limit,
            ) from exc
        except urllib.error.URLError as exc:
            raise GitHubAPIError(
                f"GitHub API unavailable: {exc.reason}"
            ) from exc

    def get_repository(self, ref: str = "") -> dict:
        if ref in self._repository_cache:
            return self._repository_cache[ref]
        data = self._request("")
        repository = data  # type: ignore[assignment]
        self._repository_cache[ref] = repository
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

    def get_files(
        self,
        paths: list[str],
        ref: str = "main",
        *,
        max_workers: int = 1,
    ) -> dict[str, str]:
        """Fetch repository files with bounded concurrency; serial by default to limit API pressure."""
        if max_workers < 1:
            raise ValueError("max_workers must be greater than zero")

        unique_paths = list(dict.fromkeys(paths))
        if not unique_paths:
            return {}

        cached = {
            path: self._file_cache[(ref, path)]
            for path in unique_paths
            if (ref, path) in self._file_cache
        }
        pending = [path for path in unique_paths if path not in cached]
        if not pending:
            return cached

        workers = min(max_workers, len(pending))
        if workers == 1:
            for path in pending:
                cached[path] = self.get_file(path, ref=ref)
            return {path: cached[path] for path in unique_paths}

        with ThreadPoolExecutor(max_workers=workers) as executor:
            fetched = executor.map(
                lambda path: (path, self.get_file(path, ref=ref)),
                pending,
            )
            for path, content in fetched:
                cached[path] = content

        return {path: cached[path] for path in unique_paths}
